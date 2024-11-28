import regex as re
import pdfminer
from io import StringIO, BytesIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

def open_pdf_file(uploaded_file):
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = BytesIO(uploaded_file.read())
    for page in PDFPage.get_pages(infile, set()):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()

    result = []
    for line in text.split('\n'):
        line2 = line.strip()
        if line2:
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
    emails = []
    pattern = re.compile(r'\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}')
    for line in document:
        matches = pattern.findall(line)
        for mat in matches:
            if len(mat) > 0:
                emails.append(mat)

    if not emails:
        return "Unknown"
    
    return emails

def get_phone_no(document):
    mob_num_regex = r'''(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)
                        [-\.\s]*\d{3}[-\.\s]??\d{4}|\d{5}[-\.\s]??\d{4})'''
    pattern = re.compile(mob_num_regex)
    matches = []
    for line in document:
        match = pattern.findall(line)
        for mat in match:
            if len(mat) > 9:
                matches.append(mat)

    return (matches)

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

