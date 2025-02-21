from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load SBERT model
model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_similarity_sbert(job_description, resume_texts):
    """Computes similarity scores using SBERT + Cosine Similarity and returns full decimal percentages."""
    if not resume_texts or not all(isinstance(text, str) for text in resume_texts):
        raise ValueError("resume_texts must be a list of non-empty strings.")

    if not isinstance(job_description, str) or job_description.strip() == "":
        raise ValueError("job_description must be a non-empty string.")

    # Encode job description and resumes
    all_texts = [job_description] + resume_texts
    embeddings = model.encode(all_texts, convert_to_numpy=True)

    job_embedding = embeddings[0].reshape(1, -1)  # Ensure 2D shape
    resume_embeddings = embeddings[1:]

    # Compute cosine similarity (values between 0 and 1)
    scores = cosine_similarity(job_embedding, resume_embeddings)[0]

    # Convert scores to percentages with full decimal precision
    scores_percentage = [score * 100 for score in scores]  # No rounding applied

    # Pair resumes with scores and sort them
    ranked_resumes = sorted(zip(resume_texts, scores_percentage), key=lambda x: x[1], reverse=True)

    return ranked_resumes
