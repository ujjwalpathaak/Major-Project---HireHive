from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from transformers import AutoModel, AutoTokenizer
import torch
import torch.nn.functional as F

nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

st_model = SentenceTransformer('all-MiniLM-L6-v2')

model_name = 'jjzha/jobbert-base-cased'
model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def get_bert_embeddings(texts):
    print(f"Generating BERT embeddings for {len(texts)} texts...")
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors='pt', max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    print(f"BERT embeddings generated with shape: {embeddings.shape}")
    return embeddings

def preprocess_text(text):
    tokens = text.split()
    tokens = [word.lower() for word in tokens if word.lower() not in stop_words]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

def get_sentence_transformer_embeddings(text):
    print(f"Generating Sentence Transformer embeddings for the input...")
    embeddings = st_model.encode(text)
    print(f"Sentence Transformer embeddings generated with shape: {embeddings.shape}")
    return embeddings

def get_score(resume_skills, resume_text, jd_text, jd_skills):
    print("Calculating similarity score...")
    jd_text = preprocess_text(jd_text)
    resume_text = preprocess_text(resume_text)

    # TF-IDF similarity
    vectorizer = TfidfVectorizer().fit_transform([jd_text, resume_text])
    vectors = vectorizer.toarray()
    job_vector, resume_vector = vectors[0], vectors[1]
    tfidf_similarity = cosine_similarity([job_vector], [resume_vector])[0][0]
    print(f"TF-IDF similarity score: {tfidf_similarity:.4f}")

    # Sentence Transformer similarity
    resume_embeddings_st = get_sentence_transformer_embeddings(resume_skills)
    jd_embeddings_st = get_sentence_transformer_embeddings(jd_skills)
    skill_similarity_matrix_st = cosine_similarity(resume_embeddings_st, jd_embeddings_st)
    print("Sentence Transformer skill similarity matrix calculated.")

    # BERT similarity
    resume_embeddings_bert = get_bert_embeddings(resume_skills)
    jd_embeddings_bert = get_bert_embeddings(jd_skills)
    skill_similarity_matrix_bert = cosine_similarity(resume_embeddings_bert, jd_embeddings_bert)
    print("BERT skill similarity matrix calculated.")

    st_similarity_threshold = 0.3
    bert_similarity_threshold = 0.5

    matched_skills = []

    # Matching skills
    for i, resume_skill in enumerate(resume_skills):
        for j, jd_skill in enumerate(jd_skills):
            st_similarity = skill_similarity_matrix_st[i][j]
            bert_similarity = skill_similarity_matrix_bert[i][j]

            if st_similarity >= st_similarity_threshold or bert_similarity >= bert_similarity_threshold:
                matched_skills.append((resume_skill, jd_skill, st_similarity, bert_similarity))

    print(f"Total number of matched skills: {len(matched_skills)}")

    filtered_st_similarities = [sim[2] for sim in matched_skills if sim[2] >= st_similarity_threshold]
    filtered_bert_similarities = [sim[3] for sim in matched_skills if sim[3] >= bert_similarity_threshold]

    if filtered_st_similarities:
        print(f"Average Sentence Transformer similarity: {sum(filtered_st_similarities) / len(filtered_st_similarities):.4f}")
    else:
        print("No Sentence Transformer similarities above threshold.")

    if filtered_bert_similarities:
        print(f"Average BERT similarity: {sum(filtered_bert_similarities) / len(filtered_bert_similarities):.4f}")
    else:
        print("No BERT similarities above threshold.")

    semantic_similarity = (sum(filtered_st_similarities) / len(filtered_st_similarities)) if filtered_st_similarities else 0
    bert_similarity_avg = (sum(filtered_bert_similarities) / len(filtered_bert_similarities)) if filtered_bert_similarities else 0

    final_similarity = (
        0.6 * semantic_similarity +
        0.4 * bert_similarity_avg
    )

    print(f"Final similarity score: {final_similarity:.4f}")
    return final_similarity