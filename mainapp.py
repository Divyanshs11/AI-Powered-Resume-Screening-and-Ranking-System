import streamlit as st
import os
from ranker import compute_similarity_sbert
from resume_parser import extract_text 

def rank_resumes(job_description, resume_files):
    """Processes and ranks resumes based on job description similarity."""
    extracted_texts = []
    file_names = []

    for file in resume_files:
        file_name = os.path.basename(file.name)
        text = extract_text(file)
        if not text or text == "No text extracted":
            st.error(f"⚠️ Could not extract text from: {file_name}")
            continue
        extracted_texts.append(text)
        file_names.append((file_name, file))  # Store file info for later use

    # Compute similarity only if we have valid resumes
    if extracted_texts:
        scores = compute_similarity_sbert(job_description, extracted_texts)
        ranked_resumes = [(file_names[idx][0], score, file_names[idx][1]) for idx, (text, score) in enumerate(scores)]
        return ranked_resumes
    else:
        return []  # Ensure empty return if no valid resumes

# Streamlit UI
st.title("📄 AI-Powered Resume Screening & Ranking")

uploaded_files = st.file_uploader("Upload Resumes (PDF/DOCX)", type=["pdf", "docx"], accept_multiple_files=True)
job_desc = st.text_area("Enter Job Description:")

if st.button("Process"):
    if job_desc.strip() and uploaded_files:
        ranked_resumes = rank_resumes(job_desc, uploaded_files)

        if ranked_resumes:
            st.subheader("📜 Ranked Resumes")
            for rank, (file_name, score, file) in enumerate(ranked_resumes, start=1):
                file.seek(0)  # Reset file pointer before reading
                file_data = file.read()

                with st.expander(f"#{rank}: {file_name} (Score: {score}%)"):
                    st.download_button(
                        label="📥 Download Resume",
                        data=file_data,
                        file_name=file_name,
                        mime="application/octet-stream"
                    )
        else:
            st.warning("No valid resumes to rank. Please check the uploaded files.")
    else:
        st.warning("Please upload resumes and enter a job description.")
