from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
model = SentenceTransformer("all-MiniLM-L6-v2")
def compute_similarity_sbert(resume_texts, job_description):
    """Computes similarity scores using SBERT + Cosine Similarity"""
    all_texts = [job_description] + resume_texts
    embeddings = model.encode(all_texts, convert_to_tensor=True)
    job_embedding = embeddings[0].unsqueeze(0)
    resume_embeddings = embeddings[1:]
    scores = cosine_similarity(job_embedding, resume_embeddings)[0]
    ranked_resumes = sorted(zip(resume_texts, scores), key=lambda x: x[1], reverse=True)
    return ranked_resumes
