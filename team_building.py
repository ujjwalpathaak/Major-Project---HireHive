import random
from itertools import permutations

# Sample candidates with skills and soft skills
candidates = [
    {
        "id": 1,
        "name": "Rohan Singh",
        "skills": ["Python", "JavaScript", "SQL", "React.js"],
        "soft_skills": ["Communication", "Teamwork", "Problem-solving"]
    },
    {
        "id": 2,
        "name": "Priya Verma",
        "skills": ["SQL", "Tableau", "Excel", "Data Analysis"],
        "soft_skills": ["Analytical Thinking", "Time Management", "Collaboration"]
    },
    {
        "id": 3,
        "name": "Vikram Patel",
        "skills": ["Agile", "Product Management", "Stakeholder Management", "Scrum"],
        "soft_skills": ["Leadership", "Conflict Resolution", "Decision Making"]
    },
    {
        "id": 4,
        "name": "Sanya Mehta",
        "skills": ["Figma", "UX Design", "Prototyping", "Graphic Design"],
        "soft_skills": ["Creativity", "Empathy", "Attention to Detail"]
    },
    {
        "id": 5,
        "name": "Ankit Kumar",
        "skills": ["React.js", "Node.js", "JavaScript", "MongoDB"],
        "soft_skills": ["Adaptability", "Communication", "Critical Thinking"]
    },
    {
        "id": 6,
        "name": "Megha Sharma",
        "skills": ["Python", "Machine Learning", "TensorFlow", "Pandas"],
        "soft_skills": ["Curiosity", "Problem-solving", "Teamwork"]
    },
    {
        "id": 7,
        "name": "Rajesh Gupta",
        "skills": ["AWS", "Docker", "Kubernetes", "Linux"],
        "soft_skills": ["Time Management", "Collaboration", "Proactiveness"]
    },
    {
        "id": 8,
        "name": "Aarti Joshi",
        "skills": ["HTML", "CSS", "Bootstrap", "WordPress"],
        "soft_skills": ["Creativity", "Attention to Detail", "Adaptability"]
    },
    {
        "id": 9,
        "name": "Nikhil Rao",
        "skills": ["Java", "Spring Boot", "Hibernate", "MySQL"],
        "soft_skills": ["Teamwork", "Critical Thinking", "Leadership"]
    },
    {
        "id": 10,
        "name": "Pooja Das",
        "skills": ["SEO", "Content Writing", "Digital Marketing", "Google Analytics"],
        "soft_skills": ["Creativity", "Communication", "Data-driven Decision Making"]
    },
    {
        "id": 11,
        "name": "Abhay Singh",
        "skills": ["PHP", "Laravel", "MySQL", "REST APIs"],
        "soft_skills": ["Problem-solving", "Adaptability", "Time Management"]
    },
    {
        "id": 12,
        "name": "Kriti Tiwari",
        "skills": ["Python", "Django", "PostgreSQL", "Flask"],
        "soft_skills": ["Communication", "Critical Thinking", "Teamwork"]
    },
    {
        "id": 13,
        "name": "Mohit Kumar",
        "skills": ["C++", "Data Structures", "Algorithms", "Competitive Programming"],
        "soft_skills": ["Focus", "Perseverance", "Analytical Thinking"]
    },
    {
        "id": 14,
        "name": "Ishita Sen",
        "skills": ["React.js", "TypeScript", "Redux", "GraphQL"],
        "soft_skills": ["Creativity", "Collaboration", "Problem-solving"]
    },
    {
        "id": 15,
        "name": "Varun Sinha",
        "skills": ["DevOps", "Jenkins", "Terraform", "CI/CD"],
        "soft_skills": ["Proactiveness", "Leadership", "Adaptability"]
    },
    {
        "id": 16,
        "name": "Swati Mehta",
        "skills": ["Data Visualization", "Power BI", "Tableau", "Excel"],
        "soft_skills": ["Analytical Thinking", "Attention to Detail", "Problem-solving"]
    },
    {
        "id": 17,
        "name": "Yash Jain",
        "skills": ["Angular", "JavaScript", "Bootstrap", "REST APIs"],
        "soft_skills": ["Adaptability", "Creativity", "Collaboration"]
    },
    {
        "id": 18,
        "name": "Ananya Roy",
        "skills": ["Blockchain", "Solidity", "Smart Contracts", "Cryptography"],
        "soft_skills": ["Curiosity", "Attention to Detail", "Problem-solving"]
    },
    {
        "id": 19,
        "name": "Harshit Aggarwal",
        "skills": ["Big Data", "Hadoop", "Spark", "NoSQL"],
        "soft_skills": ["Analytical Thinking", "Time Management", "Proactiveness"]
    },
    {
        "id": 20,
        "name": "Ritika Sharma",
        "skills": ["IoT", "Embedded Systems", "C", "Arduino"],
        "soft_skills": ["Attention to Detail", "Focus", "Critical Thinking"]
    }
]


# Function to calculate the complementarity score between two candidates
def calculate_complementarity(cand1, cand2):
    # Technical skill complementarity
    common_tech_skills = len(set(cand1['skills']).intersection(cand2['skills']))
    
    # Soft skill complementarity
    complementary_soft_skills = len(set(cand1['soft_skills']).symmetric_difference(set(cand2['soft_skills'])))
    
    # Debugging output
    print(f"Comparing {cand1['name']} and {cand2['name']} -> Common Tech Skills: {common_tech_skills}, Complementary Soft Skills: {complementary_soft_skills}")
    
    # Return the total complementarity score (consider both skills equally)
    return common_tech_skills + complementary_soft_skills

# Function to filter candidates based on required skills
def filter_candidates(candidates, required_skills):
    filtered = [cand for cand in candidates if all(skill in cand['skills'] for skill in required_skills)]
    print(f"Filtered Candidates (required skills: {required_skills}): {[cand['name'] for cand in filtered]}")
    return filtered

# Function to generate teams based on filtered candidates
def generate_teams(candidates, team_size, num_teams, required_skills):
    # Step 1: Filter candidates based on required skills
    filtered_candidates = filter_candidates(candidates, required_skills)
    
    # Debugging output
    print(f"Number of Filtered Candidates: {len(filtered_candidates)}")
    
    # Check if enough candidates are available
    if len(filtered_candidates) < team_size * num_teams:
        raise ValueError("Not enough candidates to form the required number of teams.")
    
    # Step 2: Generate all possible candidate pairs
    candidate_pairs = []
    for c1, c2 in permutations(filtered_candidates, 2):
        score = calculate_complementarity(c1, c2)
        candidate_pairs.append((c1, c2, score))
    
    print(f"Total Candidate Pairs Generated: {len(candidate_pairs)}")
    
    # Step 3: Sort pairs by complementarity score
    candidate_pairs.sort(key=lambda x: x[2], reverse=True)
    
    # Debugging output
    print(f"Top 5 Candidate Pairs (by score):")
    for pair in candidate_pairs[:5]:
        print(f"Pair: {pair[0]['name']} - {pair[1]['name']}, Score: {pair[2]}")
    
    # Step 4: Form teams by choosing pairs with high complementarity scores
    teams = []
    remaining_candidates = set(filtered_candidates)  # Track remaining candidates
    used_candidates = set()  # Track already assigned candidates
    
    while len(teams) < num_teams:
        team = []
        while len(team) < team_size and remaining_candidates:
            best_pair = None
            for c1, c2, score in candidate_pairs:
                if c1 in remaining_candidates and c2 in remaining_candidates:
                    if c1 not in used_candidates and c2 not in used_candidates:
                        team.append(c1)
                        team.append(c2)
                        used_candidates.add(c1)
                        used_candidates.add(c2)
                        remaining_candidates.remove(c1)
                        remaining_candidates.remove(c2)
                        best_pair = (c1, c2)
                        break
            if not best_pair:  # In case no valid pair is found
                break
        if len(team) == team_size:
            teams.append(team)
    
    return teams

# Example usage
team_size = 3  # Size of each team
num_teams = 1  # Number of teams to form
project_name = "E-commerce App Development"
required_skills = ["Angular", "Node.js", "UX Design"]  # Adjusted to match available skills
use_case_description = "Building an e-commerce platform with a user-friendly interface and robust back-end."

try:
    teams = generate_teams(candidates, team_size, num_teams, required_skills)

    # Output the teams formed
    print(f"Project: {project_name}")
    print(f"Use Case: {use_case_description}")
    for i, team in enumerate(teams):
        print(f"Team {i+1}: {[member['name'] for member in team]}")
except ValueError as e:
    print(e)