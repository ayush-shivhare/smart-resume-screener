# Streamlit UI app
import streamlit as st
import requests
import json

st.set_page_config(page_title="Smart Resume Screener", page_icon="🧠", layout="centered")
st.title("🧠 Smart Resume Screener")
st.caption("Powered by FastAPI + Sentence Transformers + spaCy")

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000/screen"

with st.form("resume_form"):
    resume_file = st.file_uploader("📄 Upload Resume (.pdf or .txt)", type=["pdf", "txt"])
    job_desc = st.text_area("💼 Paste Job Description Here")
    submitted = st.form_submit_button("🚀 Analyze Fit")

    if submitted:
        if not resume_file or not job_desc.strip():
            st.error("Please upload a resume and paste a job description.")
        else:
            with st.spinner("Analyzing resume..."):
                files = {"resume": resume_file}
                data = {"jd": job_desc}
                try:
                    res = requests.post(API_URL, files=files, data=data)
                    if res.status_code == 200:
                        result = res.json()
                        st.success(f"✅ Match Score: {result['score']:.2f}/10")
                        st.write("**Extracted Skills:**", ", ".join(result["skills_found"]))
                    else:
                        st.error(f"Error: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"Request failed: {e}")
