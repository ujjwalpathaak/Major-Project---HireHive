import streamlit as st
from PyPDF2 import PdfReader
import re
import json
from bson import ObjectId
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from itertools import combinations
import nltk
from pymongo import MongoClient

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

@st.cache_resource
def init_connection():
    return MongoClient("mongodb+srv://hirehive4:hirehive4@cluster0.iw9cj.mongodb.net/", tls=True, tlsAllowInvalidCertificates=True)

client = init_connection()
db = client.HireHive

jobs = db.jobs.find()
candidates = db.candidates.find()
skills_dict = db.skills_dict.find()
users = db.users.find()

jobs_list = list(jobs)
candidates_list = list(candidates)
skills_dict_list = list(skills_dict)
users_list = list(users)

complementary_soft_skills = {
    'Communication': ['Teamwork', 'Empathy'],
    'Teamwork': ['Collaboration', 'Adaptability'],
    'Problem Solving': ['Critical Thinking', 'Creativity'],
    'Adaptability': ['Flexibility', 'Resilience'],
    'Empathy': ['Emotional Intelligence', 'Active Listening'],
}

def calculate_soft_skill_score(soft_skills):
    score = 0
    for skill in soft_skills:
        if skill in complementary_soft_skills:
            # Add score for each complementary skill
            score += len(complementary_soft_skills[skill])
    return score

def some_complementarity_function(c1, c2):
    # Extracting technical and soft skills from candidates
    tech_skills_c1 = set(c1['skills'])
    tech_skills_c2 = set(c2['skills'])
    
    soft_skills_c1 = set(c1['soft_skills'])
    soft_skills_c2 = set(c2['soft_skills'])

    # Calculating common and total technical skills
    common_tech_skills = len(tech_skills_c1.intersection(tech_skills_c2))
    total_tech_skills = len(tech_skills_c1.union(tech_skills_c2))

    # Calculating common and total soft skills
    common_soft_skills = len(soft_skills_c1.intersection(soft_skills_c2))
    total_soft_skills = len(soft_skills_c1.union(soft_skills_c2))

    # Calculating scores based on complementarity
    score_tech = common_tech_skills / total_tech_skills if total_tech_skills > 0 else 0
    score_soft = common_soft_skills / total_soft_skills if total_soft_skills > 0 else 0

    # Combine scores (you can adjust the weights as needed)
    score = (score_tech + score_soft) / 2
    return score

def calculate_complementarity(c1, c2, c3):
    # Calculate scores for all combinations of candidates
    score_1_2 = some_complementarity_function(c1, c2)
    score_1_3 = some_complementarity_function(c1, c3)
    score_2_3 = some_complementarity_function(c2, c3)

    # Average score for the triplet
    total_score = (score_1_2 + score_1_3 + score_2_3) / 3
    return total_score

def filter_candidates(candidates, required_skills):
    # Filter candidates based on required technical skills
    filtered = [cand for cand in candidates if any(skill in cand['skills'] for skill in required_skills)]
    return filtered

def has_diverse_soft_skills(team):
    # Check if the team has diverse soft skills
    unique_soft_skills = set()
    
    for member in team:
        unique_soft_skills.update(member['soft_skills'])
    
    # If unique soft skills count is less than team size, they are not diverse enough
    return len(unique_soft_skills) >= len(team)

def generate_teams(candidates, team_size, num_teams, required_skills):
    filtered_candidates = filter_candidates(candidates, required_skills)
    
    #print(f"Number of Filtered Candidates: {len(filtered_candidates)}")
    
    if len(filtered_candidates) < team_size * num_teams:
        raise ValueError("Not enough candidates to form the required number of teams.")
    
    candidate_triplets = []
    
    # Generate all combinations of candidate triplets
    for c1, c2, c3 in combinations(filtered_candidates, 3):
        score = calculate_complementarity(c1, c2, c3)
        candidate_triplets.append((c1, c2, c3, score))
    
    #print(f"Total Candidate Triplets Generated: {len(candidate_triplets)}")
    
    # Sort triplets by their complementarity score
    candidate_triplets.sort(key=lambda x: x[3], reverse=True)

    #print(f"Top 5 Candidate Teams (by score):")
    
    teams = []
    
    while len(teams) < num_teams and candidate_triplets:
        best_team = None
        best_score = -1
        
        for triplet in candidate_triplets:
            if has_diverse_soft_skills(triplet[:3]):
                team_tech_skills = set(triplet[0]['skills']).union(set(triplet[1]['skills']), set(triplet[2]['skills']))
                
                if len(team_tech_skills) >= len(required_skills) and all(skill in team_tech_skills for skill in required_skills):
                    if triplet[3] > best_score:
                        best_team = triplet
                        best_score = triplet[3]

        if best_team:
            teams.append(best_team)
            candidate_triplets.remove(best_team)  # Remove selected team from candidates
        else:
            break  # No valid teams can be formed anymore

    return candidate_triplets[:5]

def parse_skills(input_text):
    # Normalize spaces and handle multi-word skills
    skills = [skill.strip() for skill in input_text.split(",")]
    return skills

def extract_text_from_pdf(uploaded_file):
    """
    Extract text from a PDF file provided as a file-like object.
    """
    text = ""
    pdf_reader = PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def preprocess_text(text):
    """Preprocess text: tokenize, remove stopwords, and lemmatize."""
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text.lower())

    tokens = word_tokenize(text)

    stop_words = set(stopwords.words("english"))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    return lemmatized_tokens

def extract_skills(tokens, skills_dictionary):
    """Extracts matching skills from tokens based on a predefined skills dictionary."""
    extracted_skills = set()

    skill_variations = {variation.lower(): skill for skill, variations in skills_dictionary.items() for variation in variations}

    for token in tokens:
        if token in skill_variations:
            extracted_skills.add(skill_variations[token])

    return list(extracted_skills)

def add_new_job(job_title, job_description, job_location, job_type, job_salary):
    job_data = {
        "job_title": job_title,
        "job_description": job_description,
        "location": job_location,
        "job_type": job_type,
        "salary": job_salary
    }

    result = db.jobs.insert_one(job_data)
    
    jobs = db.jobs.find()

    #print(f"Job added with ID: {result.inserted_id}")
    
def authenticate(email, password):
    for user in users_list:
        if user["email"] == email and user["password"] == password:
            return user
    
    return None

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Login"
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Login page
if not st.session_state.logged_in:
# if not st.session_state.logged_in:
    st.title("Login")
    username = st.text_input("Email")
    password = st.text_input("Password", type='password')
    
    if st.button("Login"):
        user = authenticate(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.current_user = user
            st.success("Logged in successfully!")
            st.session_state.current_page = "Home"
        else:
            st.error("Invalid username or password.")
else:
    st.title("HireHive")

    st.sidebar.subheader(f"Welcome, {st.session_state.current_user['name']}!")
    page = st.sidebar.radio("Navigation", ("Home", "Jobs", "Team Building"))

    if page != st.session_state.current_page:
        st.session_state.current_page = page

    if st.session_state.current_page == "Home":
        st.write("""
            HireHive is a candidate selection tool designed to streamline the recruitment process 
            by leveraging advanced skill set matching and automated social profile verification.
        """)
        st.header("Your Hiring Statistics")
        st.write("""
            Data analysis and visualization to gain a deeper understanding
        """)

        if st.button("Analyze Data"):
            st.write("Analyzing data... (Logic to be implemented)")

    elif st.session_state.current_page == "Jobs":
        st.header("Add New Job Opening")
        with st.form(key='job_form'):
            job_title = st.text_input("Job Title")
            job_description = st.text_area("Job Description")
            job_location = st.selectbox("Location", ["Noida", "Bangalore", "Hyderabad"])
            job_type = st.selectbox("Job Type", ["Full-Time", "Internship", "Contract"])
            job_salary = st.number_input("Salary (per year)", min_value=0, step=100000)
            
            # Submit button
            submit_button = st.form_submit_button(label='Add Job Opening')

            if submit_button:
                add_new_job(job_title, job_description, job_location, job_type, job_salary)
                st.success(f"Job '{job_title}' has been added successfully!")
                st.write("### Job Details:")
                st.write(f"**Title:** {job_title}")
                st.write(f"**Description:** {job_description}")
                st.write(f"**Location:** {job_location}")
                st.write(f"**Type:** {job_type}")
                st.write(f"**Salary:** ${job_salary:,}")

        st.header("All Active Jobs")
        for job in jobs_list:
            st.subheader(job["job_title"])
            st.write(f"**Description:** {job['job_description']}")
            st.write(f"**Location:** {job['location']}")
            st.write(f"**Job Type:** {job['job_type']}")
            st.write(f"**Salary:** {job['salary']}")

            st.write(f"### Upload Resumes for {job['job_title']}")

            uploaded_files = st.file_uploader(f"Choose resumes for {job['job_title']}", type=["pdf"], accept_multiple_files=True, key=f"resume_uploader_{job['job_title']}")

            if uploaded_files:
                st.write(f"Uploaded {len(uploaded_files)} resume(s) for {job['job_title']}:")
                for file in uploaded_files:
                    st.write(f"- {file.name}")

                    resume_text = extract_text_from_pdf(file)
                    tokens = preprocess_text(resume_text)
                    matched_skills = extract_skills(tokens, skills_dict)
                    st.write(f"API Response: {matched_skills}")
                
                st.success(f"Resumes uploaded and processed successfully for {job['job_title']}!")
            else:
                st.info(f"No resumes uploaded yet for {job['job_title']}.")
            st.write("---")

    elif st.session_state.current_page == "Team Building":
        st.header("Build Balanced Teams")
        st.write("""
            Strategically select candidates from the resume pool to build balanced teams from scratch 
            by aligning complementary skills.
        """)

        with st.form("requirement_form"):
            st.subheader("Project Requirements")
            skills_required = st.text_input("Required Skills (comma-separated)")

            submitted = st.form_submit_button("Submit Requirements")

        if submitted:
            st.write("Requirements submitted successfully!")
            st.write(f"**Required Skills:** {skills_required.split(',')}")

            st.write("Searching for balanced teams...")
            #print(candidates_list, 3, 1, skills_required.split(','))
            print(skills_required.split(','))
            teams = generate_teams(candidates_list, 3, 1, parse_skills(skills_required))


            #print(teams)
            index = 1
            for team1, team2, team3, score in teams:
                st.write("---")
                st.subheader(f"Team {index} - {score * 100:.2f}%")

                st.write(f"**Candidates:** {team1['name']} - {team2['name']} - {team3['name']}")
                st.write(f"**Combined Skills:** {', '.join(team1['skills'] + team2['skills'] + team3['skills'])}")
                st.write(f"**Combined Soft Skills:** {', '.join(team1['soft_skills'] + team2['soft_skills'] + team3['soft_skills'])}")

                st.write(f"**Score:** {score:.2f}")
                index = index + 1