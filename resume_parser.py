import regex as re
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

# -------- UTILS --------
from utils import extract_skills

def open_pdf_file(uploaded_file):
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    # Use the uploaded_file directly as it is already file-like
    infile = uploaded_file
    for page in PDFPage.get_pages(infile):
        interpreter.process_page(page)
    converter.close()
    text = output.getvalue()
    output.close()

    result = []
    for line in text.split('\n'):
        line2 = line.strip()
        if line2 != '':
            result.append(line2)
    return result

def remove_punctuations(line):
    return re.sub(r'(\.|\,)', '', line)

def preprocess_document(document):
    for index, line in enumerate(document):
        line = line.lower()
        line = remove_punctuations(line)

        line = line.split(' ')
        while '' in line:
            line.remove('')

        while ' '  in line:
            line.remove(' ')


        document[index] = ' '.join(line)
    return (document)

def get_email(document):
    """
    Extract the first email address from a given text document.
    """
    pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

    if isinstance(document, str):
        document = document.splitlines()

    for line in document:
        match = pattern.search(line)
        if match:
            return match.group()
    
    return None

def get_phone_no(document):
    """
    Extract the first phone number from a given text document.
    """
    # Updated regex to match different phone formats
    mob_num_regex = r'(\+91[-.\s]??\d{10}|\d{10}|\(\d{3}\)[-.\s]??\d{3}[-.\s]??\d{4}|\d{3}[-.\s]??\d{3}[-.\s]??\d{4})'
    pattern = re.compile(mob_num_regex)

    # Split the document into lines
    lines = document.split('\n')
    for line in lines:
        match = pattern.search(line)  # Find the first match in the line
        if match:
            return match.group()  # Return the first matched phone number

    return None  # Return None if no phone number is found

def get_education(document):
    education_terms = [
        "bachelor", "masters", "science", "college", "university", "engineering"
    ]
    education = []

    for line in document:
        for word in line.split(' '):
            if len(word) > 2 and word.lower() in education_terms:
                if line not in education:
                    education.append(line)

    return education

def get_experience(document):
    pattern1 = re.compile(r'(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(tember)?|oct(ober)?|nov(ember)?|dec(ember)?)(\s|\S)(\d{2,4}).*(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(tember)?|oct(ober)?|nov(ember)?|dec(ember)?)(\s|\S)(\d{2,4})')
    pattern2 = re.compile(r'(\d{2}(.|..)\d{4}).{1,4}(\d{2}(.|..)\d{4})')
    pattern3 = re.compile(r'(\d{2}(.|..)\d{4}).{1,4}(present)')
    pattern4 = re.compile(r'(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(tember)?|oct(ober)?|nov(ember)?|dec(ember)?)(\s|\S)(\d{2,4}).*(present)')

    company_pattern = re.compile(r'(\b[A-Z][a-zA-Z\s]*\b)')

    patterns = [pattern1, pattern2, pattern3, pattern4]
    experience = []
    current_experience = {}

    for index, line in enumerate(document):
        for pattern in patterns:
            exp = pattern.findall(line)
            if exp:
                company_match = company_pattern.search(line)
                if company_match:
                    company_name = company_match.group(1)
                else:
                    company_name = "Unknown Company"

                current_experience = {
                    'position': line.strip(),
                    'company': company_name,
                    'start_date': exp[0][0] if exp[0][0] else "Unknown",
                    'end_date': exp[0][1] if exp[0][1] else "Present"
                }

                experience.append(current_experience)

    return experience

