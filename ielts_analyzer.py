import re
import PyPDF2
import spacy
from pathlib import Path
from typing import List, Dict
from utils import calculate_band_score, generate_visualizations

# Initialize spaCy
nlp = spacy.load("en_core_web_sm")


class IELTS_Analyzer:
    def __init__(self, pdf_path: str, answer_key_path: str):
        self.pdf_path = Path(pdf_path)
        self.answer_key_path = Path(answer_key_path)
        self.questions = []
        self.answer_key = {}
        self.user_answers = {}
        self.scores = {"Reading": {}, "Listening": {}}
        self.times = []

    def extract_text_from_pdf(self) -> str:
        """Extract text from the provided PDF file."""
        try:
            with open(self.pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted
                if not text:
                    raise ValueError("No text extracted from PDF")
                return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {e}")

    def extract_questions(self, text: str) -> List[Dict]:
        """Extract questions using regex and NLP."""
        question_pattern = r"(?:\d+\.\s+|\d+\s+)(.*?)(?=\n\d+\.\s+|\n\d+\s+|$)"
        questions = []
        matches = re.finditer(question_pattern, text, re.DOTALL)

        for i, match in enumerate(matches, 1):
            question_text = match.group(1).strip()
            doc = nlp(question_text)
            question_type = self._determine_question_type(doc)
            questions.append({
                "number": i,
                "text": question_text,
                "type": question_type
            })
        if not questions:
            raise ValueError("No questions extracted from PDF")
        self.questions = questions
        return questions

    def _determine_question_type(self, doc) -> str:
        """Determine question type using NLP."""
        text_lower = doc.text.lower()
        if any(token.text.lower() in ["who", "what", "where", "when", "why", "how"] for token in doc):
            return "WH_Question"
        elif any(word in text_lower for word in ["true", "false", "not given"]):
            return "True_False_Not_Given"
        elif "choose" in text_lower or "select" in text_lower:
            return "Multiple_Choice"
        return "Short_Answer"

    def load_answer_key(self) -> Dict:
        """Load answer key from JSON file."""
        try:
            with open(self.answer_key_path, "r") as file:
                self.answer_key = json.load(file)
                # Convert keys to integers
                self.answer_key = {int(k): v for k, v in self.answer_key.items()}
            if not self.answer_key:
                raise ValueError("Empty answer key")
            return self.answer_key
        except Exception as e:
            raise Exception(f"Error loading answer key: {e}")

    def mark_answers(self, section: str) -> Dict:
        """Mark user answers and calculate raw score."""
        correct = 0
        total = len(self.answer_key)
        results = {}
        self.times = [0.1] * len(self.user_answers)  # Simulate timing for Streamlit

        for q_num, user_answer in self.user_answers.items():
            q_num = int(q_num)
            correct_answer = str(self.answer_key.get(q_num, "")).lower().strip()
            is_correct = user_answer.lower().strip() == correct_answer
            if is_correct:
                correct += 1
            results[q_num] = {
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct
            }
        self.scores[section]["raw"] = correct
        self.scores[section]["total"] = total
        self.scores[section]["band"] = calculate_band_score(correct, total)
        return results

    def generate_visualizations(self, section: str, results: Dict) -> None:
        """Generate performance visualizations."""
        generate_visualizations(section, results, self.times)