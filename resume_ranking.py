from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from transformers import BertTokenizer, BertModel
from transformers import RobertaTokenizer, RobertaModel
import torch

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

st_model = SentenceTransformer('all-MiniLM-L6-v2')

nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained('bert-base-uncased')

roberta_tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
roberta_model = RobertaModel.from_pretrained('roberta-base')

def get_bert_embeddings(texts):
    """
    Get BERT embeddings for a list of texts.
    """
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors='pt', max_length=512)

    with torch.no_grad():
        outputs = bert_model(**inputs)

    embeddings = outputs.last_hidden_state[:, 0, :]

    return embeddings


def get_roberta_embeddings(texts):
    """
    Get RoBERTa embeddings for a list of texts.
    """
    inputs = roberta_tokenizer(texts, padding=True, truncation=True, return_tensors='pt', max_length=512)

    with torch.no_grad():
        outputs = roberta_model(**inputs)

    embeddings = outputs.last_hidden_state[:, 0, :]
    return embeddings

def get_score(resume_skills, resume_text, jd_text, jd_skills):
    # print(resume_skills)
    # print(jd_skills)
    resume_skills = ['ML', 'rest api', 'HTML', 'css', 'cpp', 'SQL', 'tensorflow', 'javascript']
    jd_skills = ['machine learning', 'robotics', 'pytorch', 'c++', 'docker', 'GitHub', 'API', 'js']
    vectorizer = TfidfVectorizer().fit_transform([jd_text, resume_text])
    vectors = vectorizer.toarray()
    job_vector, resume_vector = vectors[0], vectors[1]
    tfidf_similarity = cosine_similarity([job_vector], [resume_vector])[0][0]
    print(f"TF-IDF Similarity between JD and Resume: {round(tfidf_similarity, 2)}")

    resume_embeddings_st = st_model.encode(list(resume_skills))
    jd_embeddings_st = st_model.encode(list(jd_skills))
    skill_similarity_matrix_st = cosine_similarity(resume_embeddings_st, jd_embeddings_st)
    print(skill_similarity_matrix_st)

    resume_embeddings_bert = get_bert_embeddings(list(resume_skills))
    jd_embeddings_bert = get_bert_embeddings(list(jd_skills))
    skill_similarity_matrix_bert = cosine_similarity(resume_embeddings_bert.numpy(), jd_embeddings_bert.numpy())
    print(skill_similarity_matrix_bert)

    resume_embeddings_roberta = get_roberta_embeddings(list(resume_skills))
    jd_embeddings_roberta = get_roberta_embeddings(list(jd_skills))
    skill_similarity_matrix_roberta = cosine_similarity(resume_embeddings_roberta.numpy(), jd_embeddings_roberta.numpy())
    print(skill_similarity_matrix_roberta)

    threshold = max(0.2, skill_similarity_matrix_st.mean() * 0.8)
    print(threshold)

    matched_skills = []

    for i, resume_skill in enumerate(resume_skills):
        for j, jd_skill in enumerate(jd_skills):
            st_similarity = skill_similarity_matrix_st[i][j]
            bert_similarity = skill_similarity_matrix_bert[i][j]
            roberta_similarity = skill_similarity_matrix_roberta[i][j]
            if st_similarity > threshold or bert_similarity > threshold:
                matched_skills.append((resume_skill, jd_skill, st_similarity, bert_similarity, roberta_similarity))

    print("Matched Skills based on Sentence Transformers and BERT:", matched_skills)

    semantic_similarity = sum(sim[2] for sim in matched_skills) / len(matched_skills) if matched_skills else 0

    final_similarity = (
        0.34 * semantic_similarity +
        0.33 * sum(sim[3] for sim in matched_skills) / len(matched_skills) if matched_skills else 0 +
        0.33 * sum(sim[4] for sim in matched_skills) / len(matched_skills) if matched_skills else 0
    )
    
    return final_similarity