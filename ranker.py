from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load SBERT model once (efficient for multiple calls)
model = SentenceTransformer("all-MiniLM-L6-v2")  # ✅ Small & efficient

def compute_similarity_sbert(resume_texts, job_description):
    """Computes similarity scores using SBERT + Cosine Similarity"""
    all_texts = [job_description] + resume_texts  # Combine all resumes with job description
    embeddings = model.encode(all_texts, convert_to_tensor=True)

    job_embedding = embeddings[0].unsqueeze(0)  # Extract job description embedding
    resume_embeddings = embeddings[1:]  # Extract resume embeddings

    # Compute cosine similarity
    scores = cosine_similarity(job_embedding, resume_embeddings)[0]

    # Rank resumes based on similarity
    ranked_resumes = sorted(zip(resume_texts, scores), key=lambda x: x[1], reverse=True)

    return ranked_resumes
