import streamlit as st

# Dummy credentials with names and companies for demonstration purposes
users = {
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
                # Here you can add code to store the job opening in a database or other storage
                st.success(f"Job '{job_title}' has been added successfully!")
                st.write("### Job Details:")
                st.write(f"**Title:** {job_title}")
                st.write(f"**Description:** {job_description}")
                st.write(f"**Location:** {job_location}")
                st.write(f"**Type:** {job_type}")
                st.write(f"**Salary:** ${job_salary:,}")

        st.header("All Active Jobs")
        # API call to get all active jobs

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