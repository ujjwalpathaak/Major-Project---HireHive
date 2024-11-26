import random
from itertools import permutations, combinations

# Sample candidates with skills and soft skills
candidates = [
    {
        "id": 1,
        "name": "Rohan Singh",
        "skills": ["Python", "JavaScript", "SQL", "React.js", "Angular"],
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
        "skills": ["Agile", "Angular", "Product Management", "Stakeholder Management", "Scrum"],
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
        "skills": ["AWS", "Docker", "Node.js", "Kubernetes", "Linux"],
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
        "skills": ["Java", "Spring Boot", "Hibernate", "MySQL", "Angular"],
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
        "skills": ["PHP", "Laravel", "Node.js", "MySQL", "REST APIs"],
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
        "skills": ["React.js", "TypeScript", "Redux", "GraphQL", "UX Design"],
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
        "skills": ["Data Visualization", "Power BI", "Tableau", "Excel", "Angular"],
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
        "skills": ["Big Data", "Hadoop", "Spark", "NoSQL", "UX Design"],
        "soft_skills": ["Analytical Thinking", "Time Management", "Proactiveness"]
    },
    {
        "id": 20,
        "name": "Ritika Sharma",
        "skills": ["IoT", "Embedded Systems", "C", "Arduino", "Node.js"],
        "soft_skills": ["Attention to Detail", "Focus", "Critical Thinking"]
    }
]


def some_complementarity_function(c1, c2):
    # Ensure skills are sets for the intersection operation
    skills_c1 = set(c1['skills'])  # Convert to set if it's a list
    skills_c2 = set(c2['skills'])  # Convert to set if it's a list

    common_skills = len(skills_c1.intersection(skills_c2))
    total_skills = len(skills_c1.union(skills_c2))

    # Complementarity score: higher the common skills, higher the complementarity
    score = common_skills / total_skills  # You can adjust this logic as needed
    return score

def calculate_complementarity(c1, c2, c3):
    # Calculate complementarity scores for pairs
    score_1_2 = some_complementarity_function(c1, c2)
    score_1_3 = some_complementarity_function(c1, c3)
    score_2_3 = some_complementarity_function(c2, c3)

    # Combine the scores (average in this case)
    total_score = (score_1_2 + score_1_3 + score_2_3) / 3
    return total_score

# Function to filter candidates based on required skills (at least one skill should match)
def filter_candidates(candidates, required_skills):
    filtered = [cand for cand in candidates if any(skill in cand['skills'] for skill in required_skills)]
    # print(f"Filtered Candidates (at least one required skill): {[cand['name'] for cand in filtered]}")
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
    
    # Step 2: Generate all possible candidate triplets
    candidate_triplets = []
    for c1, c2, c3 in combinations(filtered_candidates, 3):
        score = calculate_complementarity(c1, c2, c3)  # Now correctly passes 3 candidates
        candidate_triplets.append((c1, c2, c3, score))
    
    print(f"Total Candidate Pairs Generated: {len(candidate_triplets)}")
    
    # Step 3: Sort pairs by complementarity score
    candidate_triplets.sort(key=lambda x: x[3], reverse=True)
    
    # Debugging output
    print(f"Top 5 Candidate Teams (by score):")
    for pair in candidate_triplets[:5]:
        print(f"Team: {pair[0]['name']} - {pair[1]['name']} - {pair[2]['name']}, Score: {pair[3]}")
    
    return candidate_triplets[:5]
    
    # # Step 4: Form teams by choosing candidates whose combined skills cover all required skills
    # teams = []
    # remaining_candidates = list(filtered_candidates)
    # used_candidates = set()  # Track already assigned candidates
    
    # while len(teams) < num_teams:
    #     team = []
    #     team_skills = set()
        
    #     while len(team) < team_size and remaining_candidates:
    #         best_pair = None
    #         for c1, c2, score in candidate_triplets:
    #             if c1 in remaining_candidates and c2 in remaining_candidates:
    #                 if c1 not in used_candidates and c2 not in used_candidates:
    #                     team.append(c1)
    #                     team.append(c2)
    #                     team_skills.update(c1['skills'])
    #                     team_skills.update(c2['skills'])
    #                     used_candidates.add(c1)
    #                     used_candidates.add(c2)
    #                     remaining_candidates.remove(c1)
    #                     remaining_candidates.remove(c2)
    #                     best_pair = (c1, c2)
    #                     break
    #         if not best_pair:  # In case no valid pair is found
    #             break
        
    #     # Check if the team covers all required skills
    #     if team_skills.issuperset(required_skills) and len(team) == team_size:
    #         teams.append(team)
    #     else:
    #         # If not all required skills are covered, continue the loop
    #         for member in team:
    #             used_candidates.remove(member)
    #             remaining_candidates.add(member)
    #         team.clear()

    # return teams


team_size = 3  # Size of each team
num_teams = 1  # Number of teams to form
project_name = "E-commerce App Development"
required_skills = ['Angular', "Node.js", "UX Design"]  # Adjusted to match available skills
use_case_description = "Building an e-commerce platform with a user-friendly interface and robust back-end."

try:
    print( type(required_skills))
    teams = generate_teams(candidates, team_size, num_teams, required_skills)
    print(teams)
    # print(f"\nGenerated Teams for Project: {project_name} ({use_case_description})")
    # for idx, team in enumerate(teams, 1):
    #     print(f"\nTeam {idx}:")
    #     for member in team:
    #         print(f"- {member['name']} (Skills: {', '.join(member['skills'])})")
except ValueError as e:
    print(e)