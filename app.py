import streamlit as st
from PyPDF2 import PdfReader
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

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

skills_dict = {
    "Python": ["python", "py"],
    "JavaScript": ["javascript", "js"],
    "React.js": ["react", "reactjs", "react.js"],
    "Node.js": ["node", "nodejs", "node.js"],
    "SQL": ["sql", "structured query language"],
    "MongoDB": ["mongodb", "mongo"],
    "FastAPI": ["fastapi", "fast api"],
    "AWS": ["aws", "amazon web services"],
    "Docker": ["docker"],
    "Git": ["git", "version control"],
    "Machine Learning": ["machine learning", "ml"],
    "C++": ["c++", "cpp"],
}

# Dummy credentials with names and companies for demonstration purposes
candidates = [
    {
        "id": 1,
        "name": "Rohan Singh",
        "phone": 1234567890,
        "email": "rohan.singh@example.com",
        "skills": ["Python", "JavaScript"],
        "soft_skills": ["Communication", "Teamwork", "Problem-solving"],
        "experience": [
            {
                "company_name": "Tech Corp",
                "duration": "2 years",
                "description": "Worked on web application development using Python and JavaScript."
            }
        ],
        "education": [
            {
                "institution": "XYZ University",
                "degree": "B.Tech in Computer Science",
                "duration": "2018 - 2022"
            }
        ]
    },
    {
        "id": 2,
        "name": "Priya Verma",
        "phone": 9876543210,
        "email": "priya.verma@example.com",
        "skills": ["SQL", "Tableau", "Excel"],
        "soft_skills": ["Analytical Thinking", "Time Management", "Collaboration"],
        "experience": [
            {
                "company_name": "Data Insights Ltd.",
                "duration": "1.5 years",
                "description": "Analyzed large datasets and created dashboards to provide insights to business stakeholders."
            }
        ],
        "education": [
            {
                "institution": "ABC University",
                "degree": "M.Sc in Data Science",
                "duration": "2019 - 2021"
            }
        ]
    },
    {
        "id": 3,
        "name": "Vikram Patel",
        "phone": 1122334455,
        "email": "vikram.patel@example.com",
        "skills": ["Agile", "Product Management", "Stakeholder Management"],
        "soft_skills": ["Leadership", "Conflict Resolution", "Decision Making"],
        "experience": [
            {
                "company_name": "Innovate Tech",
                "duration": "3 years",
                "description": "Managed cross-functional teams, defined product vision, and aligned stakeholders."
            }
        ],
        "education": [
            {
                "institution": "LMN University",
                "degree": "MBA in Marketing",
                "duration": "2017 - 2019"
            }
        ]
    },
    {
        "id": 4,
        "name": "Sanya Mehta",
        "phone": 2233445566,
        "email": "sanya.mehta@example.com",
        "skills": ["Figma", "UX Design", "Prototyping"],
        "soft_skills": ["Creativity", "Empathy", "Attention to Detail"],
        "experience": [
            {
                "company_name": "Creative Designs",
                "duration": "2 years",
                "description": "Designed user interfaces and conducted usability testing to enhance user experience."
            }
        ],
        "education": [
            {
                "institution": "DEF University",
                "degree": "B.Des in UX Design",
                "duration": "2018 - 2022"
            }
        ]
    },
    {
        "id": 5,
        "name": "Ankit Kumar",
        "phone": 3344556677,
        "email": "ankit.kumar@example.com",
        "skills": ["React.js", "Node.js", "JavaScript"],
        "soft_skills": ["Adaptability", "Communication", "Critical Thinking"],
        "experience": [
            {
                "company_name": "Web Solutions Pvt. Ltd.",
                "duration": "1 year",
                "description": "Developed scalable web applications using React.js and Node.js."
            }
        ],
        "education": [
            {
                "institution": "GHI University",
                "degree": "B.Tech in Computer Science",
                "duration": "2018 - 2022"
            }
        ]
    }
]

users = {
    "": {
        "password": "",
        "name": "Rohan Singh",
        "company": "TechSolutions Inc."
    },
    "hr1@gmail.com": {
        "password": "password123",
        "name": "Rohan Singh",
        "company": "TechSolutions Inc."
    },
    "hr2@gmail.com": {
        "password": "passwordabc",
        "name": "Mandeep Kaur",
        "company": "Creative Solutions Ltd."
    },
}

jobs = [
    {
        "id": 1,
        "job_title": "Software Engineer",
        "job_description": (
            "Develop and maintain scalable web applications, collaborate with cross-functional teams, "
            "and ensure code quality through automated tests. Required skills: Python, JavaScript, React.js, "
            "Node.js, REST APIs, CI/CD, and problem-solving."
        ),
        "location": "2",
        "job_type": "Full-time",
        "salary": "$120,000 - $140,000 per year",
        "candidates_applied": [1, 2, 3]
    },
    {
        "id": 5,
        "job_title": "Data Analyst",
        "job_description": (
            "Analyze large datasets to generate actionable insights, create dashboards, and support decision-making "
            "processes. Required skills: SQL, Excel, Tableau, Python (Pandas, NumPy), data visualization, and statistical analysis."
        ),
        "location": "Remote",
        "job_type": "Contract",
        "salary": "$30 - $40 per hour",
        "candidates_applied": [2, 4, 5]
    },
    {
        "id": 3,
        "job_title": "Product Manager",
        "job_description": (
            "Define product vision, manage development cycles, and align stakeholders to achieve business goals. "
            "Required skills: Agile methodologies, stakeholder management, roadmapping, user research, and business strategy."
        ),
        "location": "New York, NY",
        "job_type": "Full-time",
        "salary": "$100,000 - $120,000 per year",
        "candidates_applied": [1, 3]
    },
    {
        "id": 4,
        "job_title": "UX Designer",
        "job_description": (
            "Design user-centric interfaces, conduct usability testing, and collaborate with developers to improve user experience. "
            "Required skills: Figma, Adobe XD, wireframing, prototyping, user research, and accessibility standards."
        ),
        "location": "Austin, TX",
        "job_type": "Full-time",
        "salary": "$85,000 - $100,000 per year",
        "candidates_applied": [1, 4, 5]
    },
]

def extract_text_from_pdf(uploaded_file):
    """
    Extract text from a PDF file provided as a file-like object.
    """
    text = ""
    pdf_reader = PdfReader(uploaded_file)  # Directly use the UploadedFile object
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def preprocess_text(text):
    """Preprocess text: tokenize, remove stopwords, and lemmatize."""
    # Normalize text to lowercase and remove non-alphanumeric characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text.lower())

    # Tokenize text
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    # Lemmatize tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    return lemmatized_tokens

def extract_skills(tokens, skills_dictionary):
    """Extracts matching skills from tokens based on a predefined skills dictionary."""
    extracted_skills = set()

    # Flatten the skills dictionary for matching
    skill_variations = {variation.lower(): skill for skill, variations in skills_dictionary.items() for variation in variations}

    # Match tokens against the dictionary
    for token in tokens:
        if token in skill_variations:
            extracted_skills.add(skill_variations[token])

    return list(extracted_skills)

def add_new_job(job_title, job_description, job_location, job_type, job_salary):
    # Create a dictionary with the job details
    job_data = {
        "job_title": job_title,
        "job_description": job_description,
        "location": job_location,
        "job_type": job_type,
        "salary": job_salary
    }
    
    # Add the job to the job_list
    jobs.append(job_data)
    
# Function to authenticate users
def authenticate(username, password):
    user = users.get(username)
    if user and user["password"] == password:
        return user  # Return user details if authentication is successful
    return None  # Return None if authentication fails

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Login"
if 'current_user' not in st.session_state:
    st.session_state.current_user = None  # Variable to store the logged-in user details

# Login page
if not st.session_state.logged_in:
    st.title("Login")
    username = st.text_input("Email")
    password = st.text_input("Password", type='password')
    
    if st.button("Login"):
        user = authenticate(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.current_user = user  # Store the logged-in user details
            st.success("Logged in successfully!")
            st.session_state.current_page = "Home"  # Redirect to Home
        else:
            st.error("Invalid username or password.")
else:
    # Header
    st.title("HireHive")

    # Navigation
    st.sidebar.subheader(f"Welcome, {st.session_state.current_user['name']}!")
    page = st.sidebar.radio("Navigation", ("Home", "Jobs", "Team Building"))

    # Update current page based on sidebar selection
    if page != st.session_state.current_page:
        st.session_state.current_page = page

    # Home Page
    if st.session_state.current_page == "Home":
        st.write("""
            HireHive is a candidate selection tool designed to streamline the recruitment process 
            by leveraging advanced skill set matching and automated social profile verification.
        """)
        st.header("Your Hiring Statistics")
        st.write("""
            Data analysis and visualization to gain a deeper understanding
        """)

        # Button for analysis
        if st.button("Analyze Data"):
            st.write("Analyzing data... (Logic to be implemented)")

    # Add new job Page
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
                # Here you can add code to store the job opening in a database or other storage
                st.success(f"Job '{job_title}' has been added successfully!")
                st.write("### Job Details:")
                st.write(f"**Title:** {job_title}")
                st.write(f"**Description:** {job_description}")
                st.write(f"**Location:** {job_location}")
                st.write(f"**Type:** {job_type}")
                st.write(f"**Salary:** ${job_salary:,}")

        st.header("All Active Jobs")
        for job in jobs:
            st.subheader(job["job_title"])
            st.write(f"**Description:** {job['job_description']}")
            st.write(f"**Location:** {job['location']}")
            st.write(f"**Job Type:** {job['job_type']}")
            st.write(f"**Salary:** {job['salary']}")

            # Button to upload resumes specific to each job
            st.write(f"### Upload Resumes for {job['job_title']}")

            uploaded_files = st.file_uploader(f"Choose resumes for {job['job_title']}", type=["pdf"], accept_multiple_files=True, key=f"resume_uploader_{job['job_title']}")

            # Show uploaded files for each job
            if uploaded_files:
                st.write(f"Uploaded {len(uploaded_files)} resume(s) for {job['job_title']}:")
                for file in uploaded_files:
                    st.write(f"- {file.name}")
                    
                    # Parse the PDF file
                    resume_text = extract_text_from_pdf(file)
                    tokens = preprocess_text(resume_text)
                    matched_skills = extract_skills(tokens, skills_dict)
                    st.write(f"API Response: {matched_skills}")
                
                st.success(f"Resumes uploaded and processed successfully for {job['job_title']}!")
            else:
                st.info(f"No resumes uploaded yet for {job['job_title']}.")
            st.write("---")

    # Team Building Page
    elif st.session_state.current_page == "Team Building":
        st.header("Build Balanced Teams")
        st.write("""
            Strategically select candidates from the resume pool to build balanced teams from scratch 
            by aligning complementary skills.
        """)

        # Form to gather product or use case requirements
        with st.form("requirement_form"):
            st.subheader("Project Requirements")
            team_size = st.number_input("Select Team Size", min_value=1, max_value=10, value=1)
            project_name = st.text_input("Project Name")
            skills_required = st.text_input("Required Skills (comma-separated)")
            use_case_description = st.text_area("Use Case Description")

            # Submit button for the form
            submitted = st.form_submit_button("Submit Requirements")

        if submitted:
            st.write("Requirements submitted successfully!")
            st.write(f"**Project Name:** {project_name}")
            st.write(f"**Required Skills:** {skills_required.split(',')}")
            st.write(f"**Use Case Description:** {use_case_description}")

            # Placeholder for team selection logic
            st.write("Searching for balanced teams... (Logic to be implemented)")