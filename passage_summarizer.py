import spacy
import nltk
from nltk.tokenize import sent_tokenize

try:
    nlp = spacy.load("en_core_web_sm")
    nltk.download('punkt', quiet=True)
except OSError:
    print("Download spaCy model: python -m spacy download en_core_web_sm")
    raise

def summarize_passage(text, ratio=0.3):
    doc = nlp(text)
    sentences = sent_tokenize(text)
    # Simplified: Take top sentences (your existing logic)
    summary_len = max(1, int(len(sentences) * ratio))
    return ' '.join(sentences[:summary_len])  # Replace with your actual logic