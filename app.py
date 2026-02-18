import streamlit as st
from utils import extract_text_from_pdf, preprocess_text, calculate_similarity
from datetime import datetime
# Near the top of app.py, after imports
try:
    from utils import nlp  # or however you expose it
    if nlp is None:
        st.warning("⚠️ spaCy English model could not be loaded. Preprocessing will be limited. Run: python -m spacy download en_core_web_sm")
except:
    st.error("spaCy import/preprocessing issue – check terminal for errors.")
# ────────────────────────────────────────────────
# JOB ROLE DATABASE
# ────────────────────────────────────────────────
job_roles = {
    "Data Scientist": "machine learning data analysis python pandas numpy deep learning statistics sklearn",
    "Machine Learning Engineer": "machine learning model deployment tensorflow pytorch api docker cloud python",
    "Frontend Developer": "html css javascript react ui responsive design web development",
    "Backend Developer": "python django flask sql api server authentication database",
    "AI Research Intern": "artificial intelligence neural networks deep learning nlp transformers research",
    "Data Analyst": "excel sql tableau power bi dashboards reporting statistics data visualization"
}

# ────────────────────────────────────────────────
# SKILL GAP FUNCTION
# ────────────────────────────────────────────────
def analyze_professional_gap(resume_text, job_text):
    resume_words = set(resume_text.lower().split())
    job_words = set(job_text.lower().split())

    important_skills = [
        "python", "machine", "learning", "sql", "data",
        "analysis", "django", "flask", "react",
        "tensorflow", "pytorch", "nlp",
        "statistics", "api", "cloud",
        "excel", "power", "bi", "tableau"
    ]

    missing = [
        skill for skill in important_skills
        if skill in job_words and skill not in resume_words
    ]
    return missing

# ────────────────────────────────────────────────
# PROFESSIONAL STYLING
# ────────────────────────────────────────────────
def add_custom_style():
    st.markdown("""
    <style>
    /* ── Base ── */
    .stApp {
        background-color: #f8fafc;      /* slate-50 - clean & modern */
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #0f172a;                 /* slate-900 */
    }

    /* Headings */
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 600;
        font-style: normal !important;
    }
    h1 {
        text-align: center;
        font-size: 2.8rem;
        margin: 1.5rem 0 2rem;
    }

    /* Button */
    .stButton > button {
        width: 100%;
        background-color: #2563eb;      /* blue-600 - trustworthy */
        color: white;
        font-size: 1.1rem;
        font-weight: 500;
        border-radius: 0.75rem;
        padding: 0.75rem 1.5rem;
        border: none;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #1d4ed8;      /* blue-700 */
        box-shadow: 0 4px 12px rgba(37,99,235,0.25);
    }

    /* Text area */
    .stTextArea textarea {
        background-color: white;
        border: 1px solid #cbd5e1;
        border-radius: 0.5rem;
        color: #1e293b;
        font-size: 1rem;
        padding: 0.75rem;
    }

    /* Cards / result boxes */
    .result-card {
        background: white;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

add_custom_style()

# ────────────────────────────────────────────────
# HEADER
# ────────────────────────────────────────────────
st.markdown("<h1>AI Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("---")

# ────────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────────
with st.sidebar:
    st.title("About")
    st.info("""
    This tool compares your resume against a job description using semantic similarity (TF-IDF + Cosine).  
    It highlights match strength, suggests roles, and identifies skill gaps.
    """)
    st.markdown("**Developed by Siddhi Grover**")
    st.caption("For educational & personal use. Results are indicative — always tailor resumes manually.")

# ────────────────────────────────────────────────
# INPUT SECTION ── side by side
# ────────────────────────────────────────────────
col1, col2 = st.columns([1, 1.3])

with col1:
    st.subheader("Upload Resume")
    st.caption("PDF only • Max ~5 MB")
    resume_file = st.file_uploader(" ", type="pdf", label_visibility="collapsed")

with col2:
    st.subheader("Job Description")
    job_desc = st.text_area(
        "Paste the full job posting here…",
        height=240,
        label_visibility="collapsed",
        placeholder="Senior Data Analyst\n• 5+ years experience with SQL, Python, Tableau...\n..."
    )

# ────────────────────────────────────────────────
# ANALYZE BUTTON
# ────────────────────────────────────────────────
if st.button("Analyze Resume", type="primary"):

    if not resume_file or not job_desc.strip():
        st.error("Please upload a PDF resume and paste a job description.")
    else:
        with st.spinner("Processing resume and job description..."):

            # ── Extract & Preprocess ──
            resume_raw = extract_text_from_pdf(resume_file)
            resume_clean = preprocess_text(resume_raw)
            job_clean   = preprocess_text(job_desc)

            # ── Job Description Match Score ──
            match_score = calculate_similarity(resume_clean, job_clean)

            # ── Color & Label Logic ──
            if match_score >= 75:
                color = "#10b981"      # emerald-500
                label = "Strong Match"
                severity = "success"
            elif match_score >= 50:
                color = "#f59e0b"      # amber-500
                label = "Moderate Match"
                severity = "warning"
            else:
                color = "#ef4444"      # red-500
                label = "Significant Gaps"
                severity = "error"

            # ── Display Score Card ──
            st.markdown(f"""
            <div class="result-card" style="background:{color}; color:white; text-align:center; padding:2rem; border-radius:1rem;">
                <div style="font-size:2.4rem; font-weight:700;">{round(match_score, 1)}%</div>
                <div style="font-size:1.4rem; margin-top:0.5rem;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

            st.progress(int(match_score), text=f"Compatibility: {int(match_score)}%")

            # ── Role Recommendations ──
            st.markdown("### Recommended Job Roles")

            role_scores = {}
            for role, desc in job_roles.items():
                role_clean = preprocess_text(desc)
                score = calculate_similarity(resume_clean, role_clean)
                role_scores[role] = score

            top_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)[:3]

            for i, (role, score) in enumerate(top_roles, 1):
                st.markdown(f"""
                <div class="result-card">
                    **{i}. {role}** — {round(score, 1)}% alignment
                </div>
                """, unsafe_allow_html=True)

            # ── Career Insight ──
            best_role, best_score = top_roles[0]

            with st.expander("Career Insight & Next Steps", expanded=True):
                st.markdown(f"""
                Your resume shows the **closest alignment** with **{best_role}** roles ({round(best_score, 1)}%).

                **Recommendations to strengthen this direction:**
                - Build 2–3 high-quality, domain-specific projects
                - Quantify achievements (%, time saved, scale, revenue impact…)
                - Incorporate industry-standard keywords naturally
                - Customize resume for each application (tailoring increases callback rates significantly)
                """)

            # ── Skill Gap Analysis ──
            with st.expander("Skill Gap Analysis", expanded=True):
                missing = analyze_professional_gap(resume_clean, job_clean)

                if missing:
                    st.markdown("**Key competencies not strongly reflected:**")
                    for s in missing:
                        st.markdown(f"- **{s.title()}**")

                    st.info("""
                    **Improvement suggestions:**
                    • Add concrete project examples using these technologies  
                    • Include measurable results (accuracy, speed, scale)  
                    • Create a dedicated **Technical Skills** section  
                    • Mention specific tools, libraries & versions
                    """)
                else:
                    st.success("""
                    Strong technical keyword alignment detected.

                    Focus next on:
                    • Adding more quantifiable achievements
                    • Writing stronger impact statements
                    """)

            st.caption("This analysis uses keyword & semantic similarity. ATS systems and recruiters may weigh factors differently.")

            # ── Report Download ──
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            report = f"""AI Resume Analysis Report
─────────────────────────────
Generated: {now}

Job Match Score: {round(match_score, 1)}%  —  {label}

Top Role Matches:
"""
            for i, (r, s) in enumerate(top_roles, 1):
                report += f"{i}. {r:<22} {round(s, 1)}%\n"

            report += "\nSkill Gap Analysis:\n"
            if missing:
                report += "Missing / weak areas:\n" + "\n".join(f"- {s}" for s in missing)
                report += "\n\nRecommendation: Add projects & quantify usage of these skills.\n"
            else:
                report += "Good keyword coverage.\nRecommendation: Emphasize impact & results.\n"

            st.download_button(
                "📄 Download Report (.txt)",
                report,
                file_name=f"resume_analysis_{now.replace(' ','_').replace(':','-')}.txt",
                mime="text/plain",
                use_container_width=True
            )