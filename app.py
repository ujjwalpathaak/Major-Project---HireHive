import nltk
import io
import streamlit as st

nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# -------- API --------
from api import add_new_candidate, authenticate, add_new_job, get_latest_jobs
from api import jobs_list, candidates_list, get_job_rankings, update_job_with_ranking

# -------- TEAM BUILDING --------
from team_building import generate_teams, parse_skills

# -------- UTILS --------
from utils import extract_skills, parse_pdf

# -------- RESUME PARSER --------
from resume_parser import get_education, get_email, get_experience, get_phone_no, preprocess_document, open_pdf_file

# -------- RESUME RANKING --------
from resume_ranking import get_score

if 'jobs_list' not in st.session_state:
    st.session_state.jobs_list = jobs_list
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Login"
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Login page
if not st.session_state.logged_in:
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
    page = st.sidebar.radio("Navigation", ("Home", "Jobs", "Team Building", "Candidates"))

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
            uploaded_jd_file = st.file_uploader("Upload Job Description (JD) PDF", type="pdf")
            job_location = st.selectbox("Location", ["Noida", "Bangalore", "Hyderabad"])
            job_type = st.selectbox("Job Type", ["Full-Time", "Internship", "Contract"])
            job_salary = st.number_input("Salary (per year)", min_value=0, step=100000)

            submit_button = st.form_submit_button(label='Add Job Opening')
            

            if submit_button:
                file_content = uploaded_jd_file.read()
                file1 = io.BytesIO(file_content)
                file2 = io.BytesIO(file_content)
                job_description = parse_pdf(file1)
                parsed_text = open_pdf_file(file2)
                document = preprocess_document(parsed_text)
                job_skills = list(extract_skills(document))
                add_new_job(job_title, job_description, job_location, job_type, job_salary, job_skills)
                st.success(f"Job '{job_title}' has been added successfully!")
                st.write("### Job Details:")
                st.write(f"**Title:** {job_title}")
                st.write(f"**Description:** {job_description}")
                st.write(f"**Location:** {job_location}")
                st.write(f"**Type:** {job_type}")
                st.write(f"**Salary:** ${job_salary:,}")

        st.header("All Active Jobs")
        st.session_state.jobs_list = get_latest_jobs()
        for job in st.session_state.jobs_list:
            short_description = ' '.join(job['job_description'].split()[:40])
            st.subheader(job["job_title"])
            st.write(f"**Description:** {short_description}")
            st.write(f"**Location:** {job['location']}")
            st.write(f"**Job Type:** {job['job_type']}")
            st.write(f"**Salary:** {job['salary']}")
            st.write(f"**Required Skills:** {list(job['job_skills'])}")

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
            teams = generate_teams(candidates_list, 3, 1, parse_skills(skills_required))

            index = 1
            for team1, team2, team3, score in teams:
                st.write("---")
                st.subheader(f"Team {index}")

                st.write(f"**Candidates:** {team1['name']} - {team2['name']} - {team3['name']}")
                st.write(f"**Combined Skills:** {', '.join(team1['skills'] + team2['skills'] + team3['skills'])}")
                index = index + 1

    elif st.session_state.current_page == "Candidates":
        st.session_state.jobs_list = get_latest_jobs()
        for job in st.session_state.jobs_list:
            short_description = ' '.join(job['job_description'].split()[:40])
            st.subheader(job["job_title"])
            st.write(f"**Description:** {short_description}")
            st.write(f"**Location:** {job['location']}")
            st.write(f"**Job Type:** {job['job_type']}")
            st.write(f"**Salary:** {job['salary']}")

            st.write(f"### Upload Resumes for {job['job_title']}")

            uploaded_files = st.file_uploader(f"Choose resumes for {job['job_title']}", type=["pdf"], accept_multiple_files=True)

            if uploaded_files:
                st.write(f"Uploaded {len(uploaded_files)} resume(s) for {job['job_title']}:")
                for file in uploaded_files:
                    file_content = file.read()
                    file1 = io.BytesIO(file_content)
                    file2 = io.BytesIO(file_content)
                    st.write(f"- {file.name}")
                    parsed_text = open_pdf_file(file1)
                    resume_text = parse_pdf(file2)
                    email = get_email(parsed_text)
                    phone_no = get_phone_no(parsed_text)
                    document = preprocess_document(parsed_text)
                    education = get_education(document)
                    experience = get_experience(document)
                    skills = extract_skills(document)
                    score = get_score(skills, resume_text, job['job_description'], job['job_skills'])
                    candidates_id = add_new_candidate(file.name, email, phone_no, skills, score, job["job_title"])
                    update_job_with_ranking(file.name, candidates_id, score, job["job_title"])

                st.success(f"Resumes uploaded and processed successfully for {job['job_title']}!")
                st.session_state['uploaded_files'] = None

            data = get_job_rankings(job['job_title'])
            st.subheader('Candidate Rankings')
            for ranking in data['rankings']:
                st.write(f"**Resume**: {ranking['name']}")
                
                with st.expander("Candidate Information"):
                    st.write(f"**Phone Number**: {ranking['candidate_info']['phone_no']}")
                    st.write(f"**Skills**: {ranking['candidate_info']['skills']}")
                
                st.write("---")
                
            st.write("---")