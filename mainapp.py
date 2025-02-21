import streamlit as st
import os
from ranker import compute_similarity_sbert
from resume_parser import extract_text 

def rank_resumes(job_description, resume_files):
    scores = []
    for file in resume_files:
        file_name = os.path.basename(file.name)
        text = extract_text(file)
        score = compute_similarity_sbert(job_description, text)
        scores.append((file_name, score, file)) 
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores

st.title("AI-Powered Resume Screening & Ranking")

uploaded_files = st.file_uploader("Upload Resumes (PDF/DOCX)", accept_multiple_files=True)\
job_desc = st.text_area("Enter Job Description:")

if st.button("Process"):
    if job_desc and uploaded_files:
        ranked_resumes = rank_resumes(job_desc, uploaded_files)
        st.subheader("📜 Ranked Resumes")
        for rank, (file_name, score, file) in enumerate(ranked_resumes, start=1):
            with st.expander(f"#{rank}: {file_name} (Score: {score:.2f})"):
                st.download_button(
                    label="📥 Download Resume",
                    data=file.getvalue(),
                    file_name=file_name,
                    mime="application/octet-stream"
                )
    else:
        st.warning("Please upload resumes and enter a job description.")
