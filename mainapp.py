import streamlit as st
import os
from resume_parser import extract_text
from DataPre import clean_text
from ranker import compute_similarity_sbert  # ✅ Updated function name

st.set_page_config(page_title="AI Resume Screening", page_icon="📄")

st.title("🔍 AI Resume Screening & Ranking System")
st.write("Upload resumes and a job description to rank the best matches.")

uploaded_resumes = st.file_uploader("Upload Resume(s)", type=["pdf", "docx"], accept_multiple_files=True)
job_description = st.text_area("Enter Job Description")

if st.button("Process"):
    if uploaded_resumes and job_description:
        resume_texts = [clean_text(extract_text(resume)) for resume in uploaded_resumes]
        ranked_resumes = compute_similarity_sbert(resume_texts, clean_text(job_description))

        st.subheader("🏆 Top Matching Resumes")
        for i, (resume_text, score) in enumerate(ranked_resumes, 1):
            st.write(f"**Rank {i}:** Resume Score: {round(score * 100, 2)}%")  # Higher score = Better match
    else:
        st.warning("Please upload resumes and provide a job description.")
