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
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    
    # Remove non-alphanumeric characters except spaces
    text = re.sub(r"[^\w\s]", "", text)
    
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()
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
    text_lower = text.lower()
    
    for category, skills in SKILL_CATEGORIES.items():
        for skill in skills:
            # Handle compound skills (e.g., "machine learning", "next.js")
            if skill.lower() in text_lower:
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


# Futuristic UI Configuration
st.set_page_config(
    page_title="🚀 Smart Resume Tool", 
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for futuristic styling
st.markdown("""
<style>
/* Import futuristic font */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');

/* Main app styling */
.main {
    background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
    color: #00ff88;
}

/* Sidebar styling */
.css-1d391kg {
    background: linear-gradient(180deg, #0f3460 0%, #0c0c0c 100%);
    border-right: 2px solid #00ff88;
}

/* Title styling */
.main-title {
    font-family: 'Orbitron', monospace;
    font-size: 4rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(45deg, #00ff88, #00d4ff, #ff0080);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 30px rgba(0, 255, 136, 0.5);
    margin-bottom: 2rem;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 20px rgba(0, 255, 136, 0.5); }
    to { text-shadow: 0 0 40px rgba(0, 255, 136, 0.8), 0 0 60px rgba(0, 212, 255, 0.3); }
}

/* Subtitle styling */
.subtitle {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.5rem;
    text-align: center;
    color: #00d4ff;
    margin-bottom: 3rem;
    opacity: 0.8;
}

/* Card styling */
.stContainer > div {
    background: rgba(15, 52, 96, 0.1);
    border: 1px solid rgba(0, 255, 136, 0.3);
    border-radius: 15px;
    padding: 2rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0, 255, 136, 0.1);
}

/* Button styling */
.stButton > button {
    background: linear-gradient(45deg, #00ff88, #00d4ff);
    color: #0c0c0c;
    border: none;
    border-radius: 25px;
    padding: 0.75rem 2rem;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    font-size: 1.1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 255, 136, 0.3);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 255, 136, 0.5);
    background: linear-gradient(45deg, #00d4ff, #ff0080);
}

/* File uploader styling */
.stFileUploader {
    border: 2px dashed #00ff88;
    border-radius: 15px;
    padding: 2rem;
    background: rgba(0, 255, 136, 0.05);
    transition: all 0.3s ease;
}

.stFileUploader:hover {
    border-color: #00d4ff;
    background: rgba(0, 212, 255, 0.1);
    transform: scale(1.02);
}

/* Text input styling */
.stTextInput > div > div > input {
    background: rgba(15, 52, 96, 0.3);
    border: 1px solid #00ff88;
    border-radius: 10px;
    color: #00ff88;
    font-family: 'Rajdhani', sans-serif;
}

.stTextArea > div > div > textarea {
    background: rgba(15, 52, 96, 0.3);
    border: 1px solid #00ff88;
    border-radius: 10px;
    color: #00ff88;
    font-family: 'Rajdhani', sans-serif;
}

/* Success/Warning/Error styling */
.stSuccess {
    background: linear-gradient(90deg, rgba(0, 255, 136, 0.1), rgba(0, 255, 136, 0.05));
    border-left: 4px solid #00ff88;
    border-radius: 10px;
}

.stWarning {
    background: linear-gradient(90deg, rgba(255, 165, 0, 0.1), rgba(255, 165, 0, 0.05));
    border-left: 4px solid #ffa500;
    border-radius: 10px;
}

.stError {
    background: linear-gradient(90deg, rgba(255, 0, 128, 0.1), rgba(255, 0, 128, 0.05));
    border-left: 4px solid #ff0080;
    border-radius: 10px;
}

/* Metric styling */
.metric-container {
    background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 212, 255, 0.1));
    border: 1px solid rgba(0, 255, 136, 0.3);
    border-radius: 15px;
    padding: 1.5rem;
    text-align: center;
    margin: 1rem 0;
}

.metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 3rem;
    font-weight: 700;
    color: #00ff88;
    text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
}

/* Sidebar navigation */
.css-1lcbmhc .css-1v0mbdj {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    color: #00ff88;
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #00ff88, #00d4ff);
    border-radius: 10px;
}

/* Sidebar title */
.sidebar-title {
    font-family: 'Orbitron', monospace;
    font-size: 1.5rem;
    color: #00ff88;
    text-align: center;
    margin-bottom: 2rem;
    text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
}
</style>
""", unsafe_allow_html=True)

# Futuristic header
st.markdown('<h1 class="main-title">🤖 SMART RESUME AI 🚀</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Next-Generation Resume Analysis & Creation Platform</p>', unsafe_allow_html=True)

# Add some spacing
st.markdown("<br>", unsafe_allow_html=True)

# Sidebar with futuristic styling
with st.sidebar:
    st.markdown('<h2 class="sidebar-title">⚡ CONTROL PANEL</h2>', unsafe_allow_html=True)
    
    menu_options = {
        "🔬 Resume Analyser": "Resume Analyser",
        "🛠️ Resume Creator": "Resume Creator"
    }
    
    choice = st.selectbox(
        "🎯 Select Mission:",
        list(menu_options.keys()),
        index=0
    )
    
    # Add some futuristic info
    st.markdown("---")
    st.markdown("### 🌟 AI FEATURES")
    st.markdown("• Neural Network Analysis")
    st.markdown("• Quantum Keyword Matching")
    st.markdown("• Holographic Skill Detection")
    st.markdown("• Cyber Enhancement Engine")
    
    st.markdown("---")
    st.markdown("### 📊 SYSTEM STATUS")
    st.success("🟢 AI Systems Online")
    st.info("🔵 Quantum Processors Ready")
    st.warning("🟡 Neural Networks Active")

# Get the actual choice value
choice = menu_options[choice]


if choice == "Resume Analyser":
    # Futuristic section header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 212, 255, 0.1));
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
    ">
        <h2 style="
            font-family: 'Orbitron', monospace;
            color: #00ff88;
            font-size: 2.5rem;
            margin-bottom: 1rem;
            text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
        ">🔬 NEURAL RESUME ANALYSER</h2>
        <p style="
            font-family: 'Rajdhani', sans-serif;
            color: #00d4ff;
            font-size: 1.2rem;
            margin: 0;
        ">Quantum-powered analysis engine for optimal job matching</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 **UPLOAD RESUME**")
        resume_file = st.file_uploader(
            "Select your resume file", 
            type=["pdf"],
            help="Upload your resume in PDF format for AI analysis"
        )
        
    with col2:
        st.markdown("### 🎯 **UPLOAD JOB DESCRIPTION**")
        jd_file = st.file_uploader(
            "Select job description file", 
            type=["pdf"],
            help="Upload the job description to match against"
        )
    
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Centered analyze button with progress simulation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 INITIATE ANALYSIS", type="primary"):
            if resume_file and jd_file:
                # Add futuristic loading animation
                with st.spinner('🔄 Neural networks processing...'):
                    import time
                    time.sleep(1)  # Simulate processing time
                    
                    st.info("🧠 Extracting resume intelligence...")
                    resume_text = extract_pdf_text(resume_file)
                    
                    st.info("🎯 Analyzing job requirements...")
                    jd_text = extract_pdf_text(jd_file)
                    
                    if resume_text and jd_text:
                        resume_clean = clean_text(resume_text)
                        jd_clean = clean_text(jd_text)
                        
                        vectorizer = TfidfVectorizer()
                        vectors = vectorizer.fit_transform([resume_clean, jd_clean])
                        score = round(cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100)
                        
                        resume_words = set(resume_clean.split())
                        jd_words = set(jd_clean.split())
                        
                        # Filter out common stop words and short words
                        stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 
                                     'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 
                                     'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 
                                     'these', 'those', 'you', 'we', 'they', 'our', 'your', 'their', 'who', 'what', 
                                     'where', 'when', 'why', 'how', 'as', 'if', 'so', 'up', 'out', 'off', 'down', 
                                     'over', 'under', 'about', 'into', 'through', 'across', 'job', 'role', 'work', 
                                     'team', 'company', 'office', 'will', 'help', 'using', 'use', 'make', 'get', 
                                     'take', 'give', 'come', 'go', 'see', 'know', 'think', 'say', 'tell', 'want'}
                        
                        # Filter missing keywords to only include meaningful terms
                        missing = [word for word in sorted(jd_words - resume_words) 
                                  if word not in stop_words and len(word) > 2]
                        
                        # Display score with futuristic metrics
                        st.markdown("""
                        <div class="metric-container">
                            <h3 style="color: #00d4ff; font-family: 'Rajdhani', sans-serif; margin-bottom: 1rem;">⚡ COMPATIBILITY MATRIX</h3>
                            <div class="metric-value">{score}%</div>
                            <p style="color: #00ff88; font-family: 'Rajdhani', sans-serif; margin-top: 1rem;">Neural Match Confidence</p>
                        </div>
                        """.format(score=score), unsafe_allow_html=True)
                        
                        # Color-coded feedback with futuristic styling
                        if score >= 75:
                            st.success("🎉 **QUANTUM ALIGNMENT ACHIEVED** - Excellent compatibility detected!")
                        elif score >= 50:
                            st.warning("⚡ **NEURAL SYNC PARTIAL** - Good match with enhancement potential")
                        else:
                            st.error("🔧 **CALIBRATION REQUIRED** - Significant optimization needed")
                        
                        st.subheader("🔍 Missing Keywords:")
                        if missing:
                            # Display first 30 missing keywords as bullet points
                            missing_display = missing[:30]
                            for keyword in missing_display:
                                st.write(f"• {keyword}")
                            if len(missing) > 30:
                                st.write(f"... and {len(missing) - 30} more keywords")
                        else:
                            st.write("✅ No missing keywords found")
                        
                        st.subheader("📝 Job Description With Matched Highlights:")
                        highlighted_jd = highlight_keywords(jd_text, resume_words)
                        # Limit display length for better readability
                        if len(highlighted_jd) > 2000:
                            st.markdown(highlighted_jd[:2000] + "...")
                            st.info("Job description truncated for display. Full analysis complete.")
                        else:
                            st.markdown(highlighted_jd)
                        
                        st.subheader("🔧 Categorized Skills Found In Resume:")
                        skill_map = categorize_skills(resume_clean)
                        if skill_map:
                            for category, skills in skill_map.items():
                                if skills:
                                    st.write(f"**{category}:**")
                                    for skill in skills:
                                        st.write(f"  • {skill}")
                                    st.write("")  # Add spacing
                        else:
                            st.write("❌ No categorized skills detected")
                            st.info("💡 Consider adding more technical skills to your resume")
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
    
    # Optional: Add suggested keywords to enhance resume
    suggested_keywords = st.text_area("Additional Keywords/Skills (Optional)", 
                                     placeholder="Add any missing keywords or skills from job analysis...")
    if suggested_keywords:
        user_info['Additional Keywords'] = suggested_keywords
    
    if st.button("Generate Resume"):
        pdf_path = generate_resume(user_info)
        with open(pdf_path, "rb") as f:
            st.download_button("Download Resume as PDF", f, file_name="resume_generated.pdf", mime="application/pdf")

