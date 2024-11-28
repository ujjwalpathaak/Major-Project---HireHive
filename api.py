import ssl
import streamlit as st
from bson import ObjectId
from pymongo import MongoClient

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
    
@st.cache_resource
def init_connection():
    return MongoClient("mongodb+srv://hirehive4:hirehive4@cluster0.iw9cj.mongodb.net/", tls=True, tlsAllowInvalidCertificates=True)

client = init_connection()
db = client.HireHive

jobs = db.jobs.find()
candidates = db.candidates.find()
users = db.users.find()

jobs_list = list(jobs)
candidates_list = list(candidates)
users_list = list(users)


def get_latest_jobs():
    jobs = db.jobs.find()
    jobs_list = list(jobs)
    return jobs_list

def get_job_rankings(job_title):
    """
    Retrieve rankings for a specific job, sorted by score in descending order.

    Parameters:
    - job_title: The title of the job.

    Returns:
    - A dictionary containing the job title and rankings or an error message.
    """
    job = db.jobs.find_one({"job_title": job_title})

    if not job:
        return {"error": "Job not found"}

    job_with_rankings = {
        "job_title": job["job_title"],
        "rankings": []
    }

    for ranking in job.get("rankings", []):
        candidate_id = ranking["candidate_id"]
        name = ranking["name"]

        candidate = db.candidates.find_one(
            {"_id": candidate_id}, 
            {"email": 1, "phone_no": 1, "skills": 1}
        )

        if candidate:
            job_with_rankings["rankings"].append({
                "candidate_id": candidate_id,
                "name": name,
                "score": ranking["score"],
                "candidate_info": candidate
            })

    # Sort rankings by score in descending order
    job_with_rankings["rankings"] = sorted(
        job_with_rankings["rankings"], 
        key=lambda x: x["score"], 
        reverse=True
    )

    return job_with_rankings

def add_new_job(job_title, job_description, job_location, job_type, job_salary, job_skills):
    job_data = {
        "job_title": job_title,
        "job_description": job_description,
        "location": job_location,
        "job_type": job_type,
        "salary": job_salary,
        "job_skills": job_skills
    }

    db.jobs.insert_one(job_data)
    st.session_state.jobs_list.append(job_data)

def add_new_candidate(name, email, phone_no, skills, score, job):
    candidate_data = {
        "job": job,
        "score": score
    }
    existing_candidate = db.candidates.find_one({"name": name})

    if existing_candidate:
        db.candidates.update_one(
            {"name": name},
            {"$push": {"job_scores": candidate_data}}
        )
        return existing_candidate["_id"]
    else:
        new_candidate_data = {
            "name": name,
            "email": email,
            "phone_no": phone_no,
            "skills": list(skills),
            "job_scores": [candidate_data]
        }
        result = db.candidates.insert_one(new_candidate_data)
        return result.inserted_id

def update_job_with_ranking(name, candidate_id, score, job_title):
    """
    Updates the job document with the candidate's ranking information, ensuring no duplicates.
    
    Parameters:
    - candidate_id: ObjectId of the candidate
    - score: Score of the candidate for the job
    - job_title: Title of the job
    """
    
    if not isinstance(candidate_id, ObjectId):
        candidate_id = ObjectId(candidate_id)

    existing = db.jobs.find_one(
        {
            "job_title": job_title,
            "rankings.candidate_id": candidate_id
        }
    )

    if not existing:
        ranking_data = {
            "candidate_id": candidate_id,
            "name": name,
            "score": score
        }
        
        db.jobs.update_one(
            {"job_title": job_title},
            {
                "$push": {
                    "rankings": {
                        "$each": [ranking_data],
                        "$sort": {"score": -1}
                    }
                }
            }
        )

def authenticate(email, password):
    for user in users_list:
        if user["email"] == email and user["password"] == password:
            return user
    
    return None