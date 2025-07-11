import streamlit as st
from fpdf import FPDF
import pdfplumber
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import tempfile
import os
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
import joblib

# SKILLS
SKILL_CATEGORIES = {
    "Programming": ["python", "java", "c++", "css", "html", "javascript", "typescript", "c#", "php", "ruby", "go", "rust", "kotlin", "swift"],
    "Data Science": ["machine learning", "data analysis", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras", "matplotlib", "seaborn", "plotly", "tableau", "power bi", "r", "sql", "mongodb", "postgresql", "mysql"],
    "Web Development": ["flask", "django", "react", "nodejs", "angular", "vue", "bootstrap", "tailwind", "next.js", "gatsby", "laravel", "spring", "asp.net"],
    "Cloud & DevOps": ["aws", "azure", "docker", "kubernetes", "git", "jenkins", "terraform", "ansible", "gitlab", "github", "bitbucket", "circleci", "travis", "heroku", "digitalocean"],
    "Mobile Development": ["android", "ios", "react native", "flutter", "xamarin", "cordova", "ionic"],
    "Database": ["sql", "nosql", "mongodb", "postgresql", "mysql", "redis", "elasticsearch", "cassandra", "oracle", "sqlite"],
    "Testing": ["selenium", "jest", "pytest", "junit", "cypress", "mocha", "jasmine", "testing", "automation", "unit testing"],
    "Project Management": ["agile", "scrum", "jira", "kanban", "waterfall", "project management", "leadership", "team lead"],
    "Soft Skills": ["communication", "leadership", "teamwork", "problem solving", "creativity", "adaptability", "time management", "critical thinking", "analytical", "presentation"]
}


def clean_text(text):
    text = text.lower()
    text = re.sub(r"https\S+ | www\S+", "", text)
    text = text.translate(str.maketrans('', '', re.sub(r'[^a-zA-Z\s]', '', text)))
    text = re.sub(r'\s+', ' ', text.strip())
    return text


def extract_pdf_text(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            return text if text.strip() else None
    except Exception as e:
        st.error(f"Error extracting PDF text: {str(e)}")
        return None


def highlight_keywords(text, keywords):
    for word in sorted(keywords, key=len, reverse=True):
        text = re.sub(fr"\b({re.escape(word)})\b", r"**\1**", text, flags=re.IGNORECASE)
    return text


def categorize_skills(text):
    skills_found = defaultdict(list)
    text_words = set(text.split())
    for category, skills in SKILL_CATEGORIES.items():
        for skill in skills:
            if skill in text_words:
                skills_found[category].append(skill)
    return skills_found


def generate_resume(user_info):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resume", ln=True, align="C")
    for key, value in user_info.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    pdf_path = "resume_generated.pdf"
    pdf.output(pdf_path)
    return pdf_path


st.set_page_config(page_title="Smart Resume Tool")

menu = ["Resume Analyser", "Resume Creator"]
choice = st.sidebar.selectbox("Choose an option:", menu)


if choice == "Resume Analyser":
    st.title("Smart Resume Analyser")
    st.write("Analyze your resume against job descriptions.")
    
    resume_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])
    jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])
    
    if st.button("Analyze"):
        if resume_file and jd_file:
            resume_text = extract_pdf_text(resume_file)
            jd_text = extract_pdf_text(jd_file)
            
            if resume_text and jd_text:
                resume_clean = clean_text(resume_text)
                jd_clean = clean_text(jd_text)
                
                vectorizer = TfidfVectorizer()
                vectors = vectorizer.fit_transform([resume_clean, jd_clean])
                score = round(cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100)
                
                resume_words = set(resume_clean.split())
                jd_words = set(jd_clean.split())
                missing = sorted(jd_words - resume_words)
                
                st.subheader(f"📊 Job Match Score: {score}%")
                st.subheader("🔍 Missing Keywords:")
                st.write(", ".join(missing) if missing else "None")
                
                st.subheader("📝 Job Description With Matched Highlights:")
                highlighted_jd = highlight_keywords(jd_text, resume_words)
                st.markdown(highlighted_jd)
                
                st.subheader("🔧 Categorized Skills Found In Resume:")
                skill_map = categorize_skills(resume_clean)
                for category, skills in skill_map.items():
                    st.markdown(f"**{category}**: {', '.join(skills)}")
        else:
            st.error("Please upload both Resume and Job Description PDFs.")


elif choice == "Resume Creator":
    st.title("Resume Creator")
    st.write("Fill out the information below to create your resume.")
    
    user_info = {}
    user_info['Full Name'] = st.text_input("Full Name")
    user_info['Email'] = st.text_input("Email")
    user_info['Phone Number'] = st.text_input("Phone Number")
    user_info['Address'] = st.text_area("Address")
    user_info['Education'] = st.text_area("Education")
    user_info['Work Experience'] = st.text_area("Work Experience")
    user_info['Skills'] = st.text_area("Skills")
    user_info['Projects'] = st.text_area("Projects")
    
    if st.button("Generate Resume"):
        pdf_path = generate_resume(user_info)
        with open(pdf_path, "rb") as f:
            st.download_button("Download Resume as PDF", f, file_name="resume_generated.pdf", mime="application/pdf")

