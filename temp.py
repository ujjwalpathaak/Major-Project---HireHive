from PyPDF2 import PdfReader
from itertools import combinations
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from utils import normalize_terms

def some_complementarity_function(c1, c2):
    tech_skills_c1 = set(c1['skills'])
    tech_skills_c2 = set(c2['skills'])

    common_tech_skills = len(tech_skills_c1.intersection(tech_skills_c2))
    total_tech_skills = len(tech_skills_c1.union(tech_skills_c2))

    score_tech = common_tech_skills / total_tech_skills if total_tech_skills > 0 else 0

    score = (score_tech) / 2
    print(f"Complementarity score between {c1['name']} and {c2['name']}: {score}")
    return score

def calculate_complementarity(c1, c2, c3):
    score_1_2 = some_complementarity_function(c1, c2)
    score_1_3 = some_complementarity_function(c1, c3)
    score_2_3 = some_complementarity_function(c2, c3)

    total_score = (score_1_2 + score_1_3 + score_2_3) / 3
    print(f"Total complementarity score for {c1['name']}, {c2['name']}, {c3['name']}: {total_score}")
    return total_score

def filter_candidates(candidates, required_skills):
    print("Filtering candidates based on required skills...")
    filtered = [cand for cand in candidates if any(skill in normalize_terms(cand['skills']) for skill in required_skills)]
    print(f"Number of candidates after filtering: {len(filtered)}")
    return filtered

def generate_teams(candidates, team_size, num_teams, required_skills):
    print("Generating teams...")
    filtered_candidates = filter_candidates(candidates, normalize_terms(required_skills))
    
    if len(filtered_candidates) < team_size * num_teams:
        raise ValueError("Not enough candidates to form the required number of teams.")
    
    print(f"Number of filtered candidates: {len(filtered_candidates)}")

    candidate_triplets = []
    print("Calculating complementarity scores for all candidate triplets...")

    for c1, c2, c3 in combinations(filtered_candidates, 3):
        score = calculate_complementarity(c1, c2, c3)
        candidate_triplets.append((c1, c2, c3, score))

    candidate_triplets.sort(key=lambda x: x[3], reverse=True)
    print("Triplets sorted by score.")

    teams = []
    print("Selecting best teams...")

    while len(teams) < num_teams and candidate_triplets:
        best_team = None
        best_score = -1

        for triplet in candidate_triplets:
            team_tech_skills = set(triplet[0]['skills']).union(set(triplet[1]['skills']), set(triplet[2]['skills']))
            
            if len(team_tech_skills) >= len(required_skills) and all(skill in team_tech_skills for skill in required_skills):
                if triplet[3] > best_score:
                    best_team = triplet
                    best_score = triplet[3]

        if best_team:
            print(f"Best team found: {best_team[0]['name']}, {best_team[1]['name']}, {best_team[2]['name']} with score {best_team[3]}")
            teams.append(best_team)
            candidate_triplets.remove(best_team)
        else:
            print("No more suitable teams found.")
            break

    print(f"Total teams generated: {len(teams)}")
    return candidate_triplets[:5]

def parse_skills(input_text):
    skills = [skill.strip() for skill in input_text.split(",")]
    print(f"Parsed skills: {skills}")
    return skills