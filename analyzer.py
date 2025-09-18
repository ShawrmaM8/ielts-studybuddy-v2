import re
import spacy
from typing import List, Dict, Tuple
from passage_utils import extract_pdf

nlp = spacy.load("en_core_web_sm")

class IELTSAnalyzer:
    def __init__(self):
        self.answer_key = {}  # {q_num: correct_ans}
        self.questions = []   # List of questions

    def extract_from_pdf(self, pdf_bytes: bytes) -> Tuple[List[str], Dict[str, str]]:
        """Extract questions & answer key from IELTS PDF."""
        text = extract_pdf(pdf_bytes)
        doc = nlp(text)

        # Regex: Questions like "1. What is..." or "Question 1:"
        q_pattern = r'(Question\s+\d+|[1-9]\d*\.\s+)(.*?)(?=\n[1-9]\d*\.|Question\s+\d+|\Z)'
        self.questions = [q[1].strip() for q in re.findall(q_pattern, text, re.DOTALL | re.IGNORECASE) if q[1].strip()]

        # Regex: Answer key like "1 A 2 B"
        key_pattern = r'Answer Key\s*:?\s*((?:\d+\s+[A-D]\s*)+)'
        key_match = re.search(key_pattern, text, re.IGNORECASE)
        if key_match:
            keys = re.findall(r'(\d+)\s+([A-D])', key_match.group(1))
            self.answer_key = {k: v for k, v in keys}

        return self.questions, self.answer_key

    def accept_responses(self, user_responses: Dict[str, str]) -> Dict[str, bool]:
        """Mark user answers."""
        marks = {}
        for q, user_ans in user_responses.items():
            correct = self.answer_key.get(q, '').upper() == user_ans.upper().strip()
            marks[q] = correct
        return marks

    def compute_band_score(self, marks: Dict[str, bool], section_type: str = 'reading') -> float:
        """Compute IELTS band score."""
        total_correct = sum(marks.values())
        max_qs = len(self.answer_key) or 1
        raw_score = (total_correct / max_qs) * 40  # Normalize to 40

        # Reading band table (IELTS official)
        band_table = {
            'reading': {0: 0, 13: 3, 15: 3.5, 18: 4, 23: 5, 27: 6, 30: 6.5, 33: 7, 35: 7.5, 37: 8, 39: 8.5, 40: 9},
            'listening': {0: 0, 13: 3, 16: 4, 23: 5, 27: 6, 30: 6.5, 32: 7, 35: 7.5, 37: 8, 39: 8.5, 40: 9}
        }
        thresholds = band_table[section_type]
        band = 0
        for score, b in sorted(thresholds.items()):
            if raw_score >= score:
                band = b
            else:
                break
        return round(band, 1)