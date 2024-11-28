import re
import nltk
import pdfplumber
from nltk.corpus import stopwords


nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# -------- API --------
from api import skills_dict_list

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
    Parse text from a PDF file.
    """
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        text = preprocess_text(text)
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

# def extract_skills(text):
#     """
#     Extract skills from text considering exact matches, synonyms, and substring matching.
#     """
#     text = text.lower()
#     text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
#     matched_skills = set()

#     # Iterate through each dictionary in the list
#     for skills_dict in skills_dict_list:
#         # Ignore the '_id' field and focus on the rest
#         for skill, synonyms in skills_dict.items():
#             if skill == '_id':  # Skip the '_id' field
#                 continue
            
#             # Check if the skill itself is in the text
#             if skill in text:
#                 matched_skills.add(skill)
            
#             # Check if any synonym is in the text
#             for synonym in synonyms:
#                 if synonym in text:
#                     matched_skills.add(skill)
#                     break  # Stop checking synonyms for this skill
            
#             # Check if the skill appears as part of any word in the text
#             for word in text.split():
#                 if skill in word:
#                     matched_skills.add(skill)
#                     break  # Stop checking words for this skill

#     return matched_skills


def extract_skills(text):
    """
    Extract skills from text considering exact matches and synonyms, but not substring matching.
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)  # Remove special characters
    matched_skills = set()

    # Iterate through each dictionary in the list
    for skills_dict in skills_dict_list:
        # Ignore the '_id' field and focus on the rest
        for skill, synonyms in skills_dict.items():
            if skill == '_id':  # Skip the '_id' field
                continue
            
            # Check if the skill itself is in the text
            if skill in text.split():  # Exact match with word splitting
                matched_skills.add(skill)
            
            # Check if any synonym is in the text
            for synonym in synonyms:
                if synonym in text:
                    matched_skills.add(skill)
                    break  # Stop checking synonyms for this skill

    return matched_skills