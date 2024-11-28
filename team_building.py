from PyPDF2 import PdfReader
from itertools import combinations
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from utils import normalize_terms

# def calculate_soft_skill_score(soft_skills):
#     score = 0
#     for skill in soft_skills:
#         if skill in complementary_soft_skills:
#             # Add score for each complementary skill
#             score += len(complementary_soft_skills[skill])
#     return score

def some_complementarity_function(c1, c2):
    # Extracting technical and soft skills from candidates
    tech_skills_c1 = set(c1['skills'])
    tech_skills_c2 = set(c2['skills'])
    
    # soft_skills_c1 = set(c1['soft_skills'])
    # soft_skills_c2 = set(c2['soft_skills'])

    # Calculating common and total technical skills
    common_tech_skills = len(tech_skills_c1.intersection(tech_skills_c2))
    total_tech_skills = len(tech_skills_c1.union(tech_skills_c2))

    # Calculating common and total soft skills
    # common_soft_skills = len(soft_skills_c1.intersection(soft_skills_c2))
    # total_soft_skills = len(soft_skills_c1.union(soft_skills_c2))

    # Calculating scores based on complementarity
    score_tech = common_tech_skills / total_tech_skills if total_tech_skills > 0 else 0
    # score_soft = common_soft_skills / total_soft_skills if total_soft_skills > 0 else 0

    # Combine scores (you can adjust the weights as needed)
    score = (score_tech) / 2
    # score = (score_tech + score_soft) / 2
    return score

def calculate_complementarity(c1, c2, c3):
    score_1_2 = some_complementarity_function(c1, c2)
    score_1_3 = some_complementarity_function(c1, c3)
    score_2_3 = some_complementarity_function(c2, c3)

    total_score = (score_1_2 + score_1_3 + score_2_3) / 3
    return total_score

def filter_candidates(candidates, required_skills):
    filtered = [cand for cand in candidates if any(skill in normalize_terms(cand['skills']) for skill in required_skills)]
    return filtered

# def has_diverse_soft_skills(team):
#     # Check if the team has diverse soft skills
#     unique_soft_skills = set()
    
#     for member in team:
#         unique_soft_skills.update(member['soft_skills'])
    
#     # If unique soft skills count is less than team size, they are not diverse enough
#     return len(unique_soft_skills) >= len(team)

def generate_teams(candidates, team_size, num_teams, required_skills):
    filtered_candidates = filter_candidates(candidates, normalize_terms(required_skills))
    
    print(f"Number of Filtered Candidates: {len(filtered_candidates)}")
    
    if len(filtered_candidates) < team_size * num_teams:
        raise ValueError("Not enough candidates to form the required number of teams.")
    
    candidate_triplets = []

    for c1, c2, c3 in combinations(filtered_candidates, 3):
        score = calculate_complementarity(c1, c2, c3)
        candidate_triplets.append((c1, c2, c3, score))

    candidate_triplets.sort(key=lambda x: x[3], reverse=True)
    
    teams = []
    
    while len(teams) < num_teams and candidate_triplets:
        best_team = None
        best_score = -1
        
        # for triplet in candidate_triplets:
        #     if has_diverse_soft_skills(triplet[:3]):
        #         team_tech_skills = set(triplet[0]['skills']).union(set(triplet[1]['skills']), set(triplet[2]['skills']))
                
        #         if len(team_tech_skills) >= len(required_skills) and all(skill in team_tech_skills for skill in required_skills):
        #             if triplet[3] > best_score:
        #                 best_team = triplet
        #                 best_score = triplet[3]
        for triplet in candidate_triplets:
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