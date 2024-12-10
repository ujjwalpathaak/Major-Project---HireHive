from itertools import combinations
from utils import normalize_terms

def some_complementarity_function(c1, c2):
    tech_skills_c1 = set(c1['skills'])
    tech_skills_c2 = set(c2['skills'])

    unique_skills_c1 = len(tech_skills_c1 - tech_skills_c2)
    unique_skills_c2 = len(tech_skills_c2 - tech_skills_c1)

    total_unique_skills = unique_skills_c1 + unique_skills_c2

    total_tech_skills = len(tech_skills_c1.union(tech_skills_c2))

    score_tech = total_unique_skills / total_tech_skills if total_tech_skills > 0 else 0
    return score_tech

def calculate_complementarity(c1, c2, c3):
    score_1_2 = some_complementarity_function(c1, c2)
    score_1_3 = some_complementarity_function(c1, c3)
    score_2_3 = some_complementarity_function(c2, c3)

    total_score = (score_1_2 + score_1_3 + score_2_3) / 3
    return total_score

def filter_candidates(candidates, required_skills):
    print("Filtering candidates based on required skills...")
    filtered = [
        cand for cand in candidates 
        if any(skill in normalize_terms(cand['skills']) for skill in required_skills)
    ]
    print(f"Number of candidates after filtering: {len(filtered)}")
    return filtered

def generate_teams(candidates, team_size, num_teams, required_skills):
    print("Generating teams...")

    required_skills = normalize_terms(required_skills)
    
    filtered_candidates = filter_candidates(candidates, required_skills)
    if len(filtered_candidates) < team_size * num_teams:
        raise ValueError("Not enough candidates to form the required number of teams.")
    
    print(f"Number of filtered candidates: {len(filtered_candidates)}")

    candidate_triplets = []
    print("Calculating complementarity scores and skill coverage for candidate triplets...")

    for c1, c2, c3 in combinations(filtered_candidates, 3):
        complementarity_score = calculate_complementarity(c1, c2, c3)
        
        combined_skills = set(c1['skills']).union(c2['skills'], c3['skills'])
        covered_skills = combined_skills.intersection(required_skills)
        coverage_score = len(covered_skills)

        normalized_coverage_score = coverage_score / len(required_skills)
        single_score = ( normalized_coverage_score + complementarity_score ) / 2
        print(f"Team -> {complementarity_score}, {normalized_coverage_score}, {single_score}")
        candidate_triplets.append((c1, c2, c3, single_score))

    candidate_triplets.sort(key=lambda x: x[3], reverse=True)

    print(f"Total triplets generated: {len(candidate_triplets)}")

    return candidate_triplets[:5]

def parse_skills(input_text):
    skills = [skill.strip() for skill in input_text.split(",")]
    print(f"Parsed skills: {skills}")
    return skills