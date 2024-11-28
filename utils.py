import re
import nltk
import pdfplumber
from nltk.corpus import stopwords


nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# -------- API --------
from data import synonym_lookup

def fix_spacing(text):
    """
    Fix common spacing issues in text.
    """
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    text = re.sub(r"(\|)", r" \1 ", text)
    text = re.sub(r"(:)", r" \1 ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def preprocess_text(text):
    """
    Preprocess text by removing stopwords, performing synonym replacement, and fixing spacing.
    """
    text = " ".join([word for word in text.split() if word not in stop_words])
    text = fix_spacing(text)
    return text

def parse_pdf(file_path):
    """
    Parse text from a PDF file, handling spacing issues.
    """
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text(x_tolerance=2, y_tolerance=1)
            if page_text:
                text += page_text + "\n"
        text = preprocess_text(text)
    return text

def extract_skills(document):
    skills = []

    synonym_lookup_flat = {}
    for skill, synonyms in synonym_lookup.items():
        for synonym in synonyms:
            synonym_lookup_flat[synonym.lower()] = skill

    for line in document:
        words = line.split()

        for word in words:
            word_lower = word.lower()
            if word_lower in synonym_lookup_flat and synonym_lookup_flat[word_lower] not in skills:
                skills.append(synonym_lookup_flat[word_lower])

        word_pairs = [' '.join(pair) for pair in zip(words[:-1], words[1:])]
        for pair in word_pairs:
            pair_lower = pair.lower()
            if pair_lower in synonym_lookup_flat and synonym_lookup_flat[pair_lower] not in skills:
                skills.append(synonym_lookup_flat[pair_lower])

    return skills