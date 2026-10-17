"""
AI Resume Analyzer & ATS Auditor - Pure Python Web Application
Framework: Streamlit & Python 3.11 NLP Engine
"""
import io
import streamlit as st
import pandas as pd
import altair as alt

from analyzer.parser import ResumeParser
from analyzer.ats_engine import ATSEngine
from analyzer.jd_matcher import JobMatcher
from analyzer.optimizer import BulletOptimizer
from analyzer.interview_gen import InterviewQuestionGenerator

# Page Configuration
st.set_page_config(
    page_title="ResuMetric AI - Resume Analyzer & ATS Auditor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for SaaS Aesthetic
st.markdown("""
<style>
    /* Global Styles */
    .main {
        background-color: #0b0f19;
    }
    .stMetric {
        background: rgba(30, 41, 59, 0.7);
        padding: 16px;
        border-radius: 12px;
        border: 1px solid rgba(51, 65, 85, 0.7);
    }
    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .badge-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .badge-matched {
        background-color: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-missing {
        background-color: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .badge-skill {
        background-color: rgba(99, 102, 241, 0.15);
        color: #a5b4fc;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize NLP Engines
@st.cache_resource
def get_engines():
    return (
        ResumeParser(),
        ATSEngine(),
        JobMatcher(),
        BulletOptimizer(),
        InterviewQuestionGenerator()
    )

parser, ats_engine, jd_matcher, bullet_optimizer, interview_gen = get_engines()

# Pre-loaded Realistic Sample Profiles
SAMPLE_PROFILES = {
    "Select a pre-loaded sample...": None,
    "💻 Senior Full-Stack Engineer": {
        "title": "Senior Full-Stack Engineer",
        "resume": """ALEXANDER RIVERA
San Francisco, CA | (555) 019-2834 | alex.rivera@devmail.com | linkedin.com/in/alex-rivera-dev | github.com/alexrivera-eng

PROFESSIONAL SUMMARY
Results-driven Senior Full-Stack Software Engineer with 6+ years of experience architecting high-concurrency web applications, microservices, and modern frontend platforms. Spearheaded migration of legacy monolithic systems into Dockerized cloud services on AWS, slashing latency by 45% and supporting 2.5M+ active users. Passionate about developer tooling, clean code, and test automation.

TECHNICAL SKILLS
• Languages: TypeScript, JavaScript (ES6+), Python, Go, SQL, HTML5, CSS3
• Frontend: React, Next.js, Redux Toolkit, Tailwind CSS, Webpack, Vite
• Backend: Node.js, Express.js, FastAPI, PostgreSQL, Redis, GraphQL, REST APIs
• Cloud & DevOps: AWS (EC2, S3, RDS, Lambda), Docker, Kubernetes, CI/CD, GitHub Actions, Terraform
• Practices: Microservices, System Design, Agile/Scrum, TDD, Unit Testing (Jest, PyTest), Code Reviews

WORK EXPERIENCE
Senior Full-Stack Engineer | Apex Cloud Solutions, San Francisco, CA | 2022 – Present
• Architected and deployed a multi-tenant SaaS analytics platform using React, Node.js, and PostgreSQL, increasing client onboarding speed by 60%.
• Optimized complex SQL aggregation queries and integrated Redis distributed caching, reducing p99 database response latency by 52% across 10M+ daily records.
• Spearheaded end-to-end CI/CD pipeline automation via GitHub Actions and Docker, reducing deployment cycle times from 4 hours to 12 minutes with zero downtime.
• Mentored 5 junior and mid-level software engineers on clean architecture, design patterns, and code review best practices.

Software Engineer | NexaTech Systems, Austin, TX | 2019 – 2022
• Engineered real-time collaboration canvas using Next.js, WebSockets, and Redis, serving over 350,000 monthly active users.
• Built automated regression test suites with Jest and Cypress, elevating total test coverage from 42% to 88% and cutting production bugs by 35%.
• Developed secure OAuth 2.0 and JWT authentication workflows complying with enterprise SOC2 and GDPR requirements.

PROJECTS
• CloudPulse - Distributed Microservices APM (github.com/alexrivera-eng/cloudpulse):
  Open-source monitoring tool tracking container health and request tracing with Go, Prometheus, and Grafana. Starred by 1,200+ developers.
• DevFlow - AI Markdown Resume Builder (devflow-resume.app):
  Interactive web application generating ATS-optimized PDF resumes using React and Python backend with 15k+ downloads.

EDUCATION & CERTIFICATIONS
• Bachelor of Science in Computer Science | University of Texas at Austin (2015 – 2019)
• AWS Certified Solutions Architect – Associate (2023)
""",
        "job_description": """Position: Senior Full-Stack Engineer
Company: ScaleUp Tech Corp
Requirements:
• 5+ years of experience with React, TypeScript, Node.js, and PostgreSQL.
• Proven track record architecting distributed microservices and REST/GraphQL APIs.
• Strong hands-on experience with Docker, Kubernetes, and AWS infrastructure.
• Experience with CI/CD automation, testing frameworks (Jest/PyTest), and system design.
• Passion for mentoring team members and clean software architecture.
"""
    },
    "🤖 AI / Machine Learning Specialist": {
        "title": "Machine Learning Engineer",
        "resume": """PRIYA SHARMA
Seattle, WA | (555) 782-9014 | priya.sharma@mlmail.org | linkedin.com/in/priya-sharma-ai | github.com/priyasharma-ml

SUMMARY
Innovator and AI/Machine Learning Engineer with 4+ years of specialized experience training, fine-tuning, and deploying Large Language Models (LLMs), RAG pipelines, and computer vision systems. Engineered production ML inference pipelines on AWS and GCP processing 15M+ daily requests with 99.9% uptime.

SKILLS
• ML & Deep Learning: PyTorch, TensorFlow, Hugging Face, Scikit-learn, LangChain, LlamaIndex, RAG, LoRA
• Languages: Python, C++, SQL, Bash
• Data & MLOps: Pandas, NumPy, OpenCV, MLflow, Docker, Kubernetes, Triton Inference Server, AWS SageMaker
• Databases: Pinecone, Milvus, ChromaDB, PostgreSQL, Redis

EXPERIENCE
Machine Learning Engineer | Cognition Labs, Seattle, WA | 2022 – Present
• Architected enterprise Retrieval-Augmented Generation (RAG) platform using LangChain, Pinecone, and Claude 3.5, cutting document hallucination rates by 42%.
• Fine-tuned Llama-3 8B models with LoRA/QLoRA on proprietary legal datasets, achieving a 94.2% accuracy score and outperforming base models by 28%.
• Optimized model serving using TensorRT-LLM and Triton, boosting inference throughput by 3.4x and reducing GPU hosting costs by $120,000 annually.

Data Scientist | DataWave Technologies, San Jose, CA | 2020 – 2022
• Built real-time fraud detection pipeline using XGBoost and PyTorch processing 5M daily transactions, preventing $1.8M in fraudulent charges.
• Implemented automated model retraining and drift detection pipelines with MLflow and Docker on AWS.

EDUCATION
• M.S. in Computer Science (Machine Learning Specialization) | University of Washington
• B.Tech in Computer Engineering | IIT Bombay
""",
        "job_description": """Position: Machine Learning Engineer
Company: DeepMatrix AI
Requirements:
• 3+ years experience developing production ML / Deep Learning applications.
• Mastery of Python, PyTorch, Hugging Face, and modern LLM architectures.
• Hands-on expertise building RAG pipelines, Vector Databases (Pinecone, Milvus), and LangChain.
• Experience with MLOps: Docker, Kubernetes, and AWS SageMaker.
"""
    }
}

# Sidebar Configuration
with st.sidebar:
    st.title("⚙️ ResuMetric Engine")
    st.caption("100% Pure Python ATS Auditor • Built for Interviews")

    st.markdown("---")
    st.subheader("⚡ 1-Click Interview Profiles")
    selected_sample_key = st.selectbox("Load Sample Candidate Profile", list(SAMPLE_PROFILES.keys()))

    st.markdown("---")
    st.subheader("🎯 Target Job Description")
    st.caption("Compare skills & calculate ATS match %")
    default_jd = ""
    if selected_sample_key and SAMPLE_PROFILES[selected_sample_key]:
        default_jd = SAMPLE_PROFILES[selected_sample_key]["job_description"]
    
    jd_input = st.text_area("Job Description Requirements", value=default_jd, height=180, placeholder="Paste target job requirements here...")

    st.markdown("---")
    st.subheader("🔑 AI Optimization Settings")
    api_key_input = st.text_input("Optional Gemini API Key", type="password", help="Leave blank to use the built-in High-Accuracy Local NLP Engine.")
    
    st.info("💡 **Interview Tip:** The built-in engine uses Google's XYZ formula & rule-based NLP to guarantee instant, 100% offline analysis without external API dependencies!")

# Header Area
col_logo, col_desc = st.columns([1, 6])
with col_desc:
    st.title("ResuMetric AI - Resume Analyzer & ATS Auditor")
    st.markdown("**Enterprise-grade Resume Evaluation • ATS Scoring • Skill Gap Analysis • Google XYZ Bullet Optimizer**")

st.markdown("---")

# Main Input Section
default_resume_text = ""
if selected_sample_key and SAMPLE_PROFILES[selected_sample_key]:
    default_resume_text = SAMPLE_PROFILES[selected_sample_key]["resume"]

col_upload, col_text = st.columns([1, 1])

with col_upload:
    st.subheader("📤 Upload Resume File")
    uploaded_file = st.file_uploader("Upload PDF, DOCX, or TXT file", type=["pdf", "docx", "txt"])

with col_text:
    st.subheader("📝 Or Paste Resume Text")
    resume_text_area = st.text_area("Resume Content", value=default_resume_text, height=140, placeholder="Paste plain resume text here...")

# Analysis Trigger
analyze_button = st.button("🚀 Analyze Resume with AI", type="primary", use_container_width=True)

# Processing Logic
resume_content = ""
filename = "Pasted Resume.txt"

if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.read()
        filename = uploaded_file.name
        resume_content = parser.extract_text_from_bytes(file_bytes, filename)
    except Exception as e:
        st.error(f"⚠️ {str(e)}")
        resume_content = ""
elif resume_text_area.strip():
    resume_content = resume_text_area.strip()

# Run Analysis
if (analyze_button or selected_sample_key != "Select a pre-loaded sample...") and len(resume_content) > 15:
    with st.spinner("Analyzing resume structure, ATS compliance, technical skills, and keywords..."):
        # 1. Parse Structure
        parsed = parser.parse(resume_content)

        # 2. ATS Score
        ats_result = ats_engine.evaluate(parsed)

        # 3. Job Description Match
        jd_result = jd_matcher.match(resume_content, jd_input)

        # 4. Tailored Interview Questions
        interview_qs = interview_gen.generate(ats_result["detected_skills"], parsed["contact_info"]["name"])

    st.success("✅ Analysis Completed Successfully!")

    # Top Executive Summary Metrics
    st.markdown("## 📊 Executive Summary & ATS Score")
    
    total_detected = ats_result.get("total_detected_skills", 0)
    has_jd = jd_result.get("has_jd", False)
    missing_jd_count = len(jd_result.get("missing_keywords", [])) if has_jd else 0
    num_weak = len(ats_result.get("weak_points", []))

    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    with m_col1:
        st.metric(
            label="Overall ATS Score",
            value=f"{ats_result['score']} / 100",
            delta=f"Grade {ats_result['grade']}"
        )
    with m_col2:
        st.metric(
            label="🎯 Detected Skills",
            value=f"{total_detected} Skills",
            delta="Extracted from resume",
            delta_color="normal"
        )
    with m_col3:
        if has_jd:
            st.metric(
                label="🧩 Missing JD Skills",
                value=f"{missing_jd_count} Skills",
                delta="Gaps vs Job Description",
                delta_color="inverse" if missing_jd_count > 0 else "normal"
            )
        else:
            st.metric(
                label="🧩 Missing JD Skills",
                value="No JD Provided",
                delta="Paste JD to compare",
                delta_color="off"
            )
    with m_col4:
        st.metric(
            label="⚠️ Weak Points",
            value=f"{num_weak} Issues",
            delta="Areas to improve" if num_weak > 0 else "Clean Resume",
            delta_color="inverse" if num_weak > 0 else "normal"
        )
    with m_col5:
        st.metric(
            label="Job Match Rate",
            value=f"{jd_result['match_percentage']}%" if has_jd else "N/A",
            delta=f"{len(jd_result['matched_keywords'])} Skills Matched" if has_jd else "Add JD for %"
        )

    # Detailed Tabs
    tab_overview, tab_missing_skills, tab_weaknesses, tab_job_match, tab_optimizer, tab_interview, tab_inspector = st.tabs([
        f"🎯 Detected Skills ({total_detected})",
        "🧩 Missing Skills & Gaps",
        f"⚠️ Weak Points ({num_weak})",
        "🎯 Job Description Match",
        "✍️ AI Bullet Optimizer (Google XYZ)",
        "🎙️ Tailored Interview Questions",
        "📄 Parsed Structure & Contact"
    ])

    # TAB 1: DETECTED SKILLS (CATEGORIZED)
    with tab_overview:
        st.subheader("🎯 Detected Skills Across Categories")
        st.caption(f"Successfully identified {total_detected} technical and soft skills from your resume.")

        if ats_result["detected_skills"]:
            cat_cols = st.columns(2)
            for idx, (category, skills) in enumerate(ats_result["detected_skills"].items()):
                with cat_cols[idx % 2]:
                    st.markdown(f"#### {category} ({len(skills)})")
                    badges_html = "".join([f"<span class='badge-pill badge-skill'>✓ {s}</span>" for s in skills])
                    st.markdown(badges_html, unsafe_allow_html=True)
                    st.markdown("")
        else:
            st.warning("⚠️ 0 recognized skills detected. Please add a dedicated 'TECHNICAL SKILLS' section with keywords like Python, SQL, Git, etc.")

        st.markdown("---")
        st.subheader("Dimensional Scoring Breakdown")
        c1, c2 = st.columns([1, 1])
        with c1:
            breakdown = ats_result["breakdown"]
            chart_data = []
            for key, item in breakdown.items():
                st.write(f"**{item['title']}**: `{item['score']} / {item['max']}` ({item['percentage']}%)")
                st.progress(item['percentage'] / 100)
                st.caption(item['feedback'][0] if item['feedback'] else "")
                chart_data.append({"Category": item['title'].split(' ')[0], "Score %": item['percentage']})

            df_chart = pd.DataFrame(chart_data)
            bar_chart = alt.Chart(df_chart).mark_bar(cornerRadius=6, color="#6366f1").encode(
                x=alt.X("Score %:Q", scale=alt.Scale(domain=[0, 100])),
                y=alt.Y("Category:N", sort="-x"),
                tooltip=["Category", "Score %"]
            ).properties(height=240)
            st.altair_chart(bar_chart, use_container_width=True)

        with c2:
            st.subheader("Key Strengths")
            for strength in ats_result["strengths"]:
                st.markdown(f"- **{strength}**")

            st.subheader("💡 Improvement Suggestions")
            for imp in ats_result["improvements"]:
                st.markdown(f"- {imp}")

    # TAB 2: MISSING SKILLS & GAPS
    with tab_missing_skills:
        st.subheader("🧩 Missing Skills & Technical Skill Gap Analysis")

        if has_jd:
            st.markdown("### Genuinely Missing Skills (Required by Job Description, Absent in Resume)")
            if jd_result.get("missing_keywords"):
                st.warning(f"⚠️ You are missing **{len(jd_result['missing_keywords'])}** skills requested in this Job Description:")
                badges_missing = "".join([f"<span class='badge-pill badge-missing'>+ {k}</span>" for k in jd_result["missing_keywords"]])
                st.markdown(badges_missing, unsafe_allow_html=True)
                
                st.markdown("#### 💡 How to Fix:")
                st.markdown("Incorporate these missing skills naturally into your **Work Experience bullet points** or **Skills section** to boost your match rate above 80%.")
            else:
                st.success("🎉 Outstanding! 100% of the skills requested in the Job Description were found in your resume.")
        else:
            st.info("ℹ️ **No Job Description provided yet.** Paste a target Job Description in the left sidebar to compare required skills against your resume and see genuinely missing skills.")

        st.markdown("---")
        st.markdown("### 💡 Recommended Industry Benchmark Skills (2026 Standards for Your Role)")
        st.caption("Based on your detected candidate profile, these are companion skills top tech firms commonly look for:")

        missing_benchmarks = ats_result.get("missing_domain_skills", [])
        if missing_benchmarks:
            for item in missing_benchmarks:
                priority_badge = "🔴 HIGH PRIORITY" if item["importance"] == "HIGH" else "🟡 MEDIUM PRIORITY"
                with st.expander(f"➕ {item['skill']} ({item['category']}) — {priority_badge}", expanded=True):
                    st.markdown(f"**Category:** `{item['category']}` • **Importance:** `{item['importance']}`")
                    st.markdown(f"**Why Recruiters Value It:** {item['reason']}")
                    st.info(f"**📍 Suggested Placement:** {item['suggested_placement']}")
        else:
            st.success("✅ Excellent! Your resume covers all core industry benchmark skills for your domain.")

    # TAB 3: WEAK POINTS & VULNERABILITIES (KAMZORIYAN)
    with tab_weaknesses:
        st.subheader("⚠️ Weak Points & Critical Vulnerabilities Audit (Kamzoriyan)")
        st.caption("AI-powered diagnostic of specific weak areas reducing your ATS score, with actionable fixes.")

        weak_list = ats_result.get("weak_points", [])
        if not weak_list:
            st.success("🎉 No major weak points found! Your resume passes standard ATS benchmarks.")
        else:
            for idx, wp in enumerate(weak_list):
                sev = wp.get("severity", "MODERATE")
                icon = "🔴" if sev == "CRITICAL" else ("🟡" if sev == "MODERATE" else "🔵")
                with st.expander(f"{icon} [{wp['severity_label']}] {wp['title']} — ({wp['impact']})", expanded=(idx < 2)):
                    st.markdown(f"**📍 Category:** `{wp['category']}` • **Severity Level:** `{sev}`")
                    st.error(f"**❌ Identified Weakness:** {wp['issue']}")
                    st.success(f"**💡 How to Fix This (Hal):** {wp['how_to_fix']}")
                    if wp.get("example"):
                        st.info(f"**📝 Concrete Before & After Example:**\n\n{wp['example']}")

            for key, item in breakdown.items():
                st.write(f"**{item['title']}**: `{item['score']} / {item['max']}` ({item['percentage']}%)")
                st.progress(item['percentage'] / 100)
                st.caption(item['feedback'][0] if item['feedback'] else "")
                chart_data.append({"Category": item['title'].split(' ')[0], "Score %": item['percentage']})

            # Altair Bar Chart
            df_chart = pd.DataFrame(chart_data)
            bar_chart = alt.Chart(df_chart).mark_bar(cornerRadius=6, color="#6366f1").encode(
                x=alt.X("Score %:Q", scale=alt.Scale(domain=[0, 100])),
                y=alt.Y("Category:N", sort="-x"),
                tooltip=["Category", "Score %"]
            ).properties(height=240)
            st.altair_chart(bar_chart, use_container_width=True)

        with c2:
            st.subheader("Key Strengths & High-Impact Recommendations")
            
            st.markdown("#### ✅ Top Strengths")
            for strength in ats_result["strengths"]:
                st.markdown(f"- **{strength}**")

            st.markdown("#### 💡 Next Steps for Improvement")
            for imp in ats_result["improvements"]:
                st.markdown(f"- {imp}")

            st.markdown("---")
            st.subheader("Detected Industry Skills Cloud")
            if ats_result["detected_skills"]:
                for category, skills in ats_result["detected_skills"].items():
                    st.markdown(f"**{category}:**")
                    badges_html = "".join([f"<span class='badge-pill badge-skill'>{s}</span>" for s in skills])
                    st.markdown(badges_html, unsafe_allow_html=True)
            else:
                st.caption("No standardized tech skills detected.")

    # TAB 4: JOB MATCH & SKILL GAP
    with tab_job_match:
        st.subheader("Target Job Keyword Alignment")
        if not jd_result["has_jd"]:
            st.warning("Paste a Job Description in the left sidebar to enable Job Match % and Skill Gap Analysis!")
        else:
            col_jd_stat, col_jd_reco = st.columns([1, 2])
            with col_jd_stat:
                st.metric("Keyword Match Rate", f"{jd_result['match_percentage']}%")
                st.caption(f"Scanned across {jd_result['total_jd_skills_found']} job keywords.")
            with col_jd_reco:
                for reco in jd_result["recommendations"]:
                    st.info(f"💡 {reco}")

            col_mat, col_mis = st.columns([1, 1])
            with col_mat:
                st.markdown("#### ✓ Matched Skills (Present in both)")
                if jd_result["matched_keywords"]:
                    badges_matched = "".join([f"<span class='badge-pill badge-matched'>✓ {k}</span>" for k in jd_result["matched_keywords"]])
                    st.markdown(badges_matched, unsafe_allow_html=True)
                else:
                    st.caption("None matched yet.")

            with col_mis:
                st.markdown("#### + Missing Keywords (Skill Gap)")
                if jd_result["missing_keywords"]:
                    badges_missing = "".join([f"<span class='badge-pill badge-missing'>+ {k}</span>" for k in jd_result["missing_keywords"]])
                    st.markdown(badges_missing, unsafe_allow_html=True)
                else:
                    st.caption("No critical missing skills detected!")

    # TAB 5: AI BULLET POINT OPTIMIZER
    with tab_optimizer:
        st.subheader("AI Bullet Point Rewriter")
        st.info("📌 **Google XYZ Formula:** *Accomplished [X] as measured by [Y], by doing [Z]*")

        sample_bullets = parsed["bullet_points"] if parsed["bullet_points"] else [
            "Worked on backend database queries and fixed application bugs.",
            "Responsible for frontend UI components and website performance.",
            "Helped team with deployment and unit testing."
        ]

        selected_bullet = st.selectbox("Select a bullet point from your resume to optimize:", sample_bullets)
        custom_bullet_text = st.text_input("Or write/edit bullet point here:", value=selected_bullet)

        if st.button("✨ Transform with Google XYZ Formula", type="secondary"):
            with st.spinner("Applying STAR & XYZ transformation..."):
                opt_res = bullet_optimizer.optimize(
                    custom_bullet_text,
                    role_context=parsed["contact_info"]["name"] or "Software Engineer",
                    api_key=api_key_input
                )

            st.write(f"**Engine Used:** `{opt_res['engine']}` • **Theme Detected:** `{opt_res['theme_detected']}`")

            for idx, variation in enumerate(opt_res["variations"]):
                with st.expander(f"Variation {idx+1}: {variation['title']} ({variation['tag']})", expanded=True):
                    st.markdown(f"**Optimized Statement:**\n> {variation['text']}")
                    st.caption(f"**Framework applied:** {variation['framework']}")

    # TAB 4: INTERVIEW QUESTIONS
    with tab_interview:
        st.subheader("Tailored Interview Questions Based on Resume Stack")
        st.caption("Questions technical interviewers and hiring managers are likely to ask based on your resume.")

        for idx, q in enumerate(interview_qs):
            with st.expander(f"Question {idx+1}: {q['category']} — \"{q['question']}\"", expanded=(idx==0)):
                st.markdown(f"**🎯 What Interviewers Are Looking For:**\n{q['what_they_test']}")
                st.success(f"**💡 Recommended STAR Strategy & Model Blueprint:**\n{q['star_guide']}")

    # TAB 5: PARSED STRUCTURE & CONTACT
    with tab_inspector:
        st.subheader("Parsed Contact Hygiene & Structural Analysis")
        c_info = parsed["contact_info"]

        col_c1, col_c2, col_c3, col_c4 = st.columns(4)
        col_c1.write(f"**Name:** {c_info['name']}")
        col_c2.write(f"**Email:** {c_info['email'] or '⚠️ Missing'}")
        col_c3.write(f"**Phone:** {c_info['phone'] or '⚠️ Missing'}")
        col_c4.write(f"**LinkedIn:** {c_info['linkedin'] or '⚠️ Missing'}")

        st.markdown("#### Detected Sections")
        sec_cols = st.columns(len(parsed["sections"]))
        for i, (sec, content) in enumerate(parsed["sections"].items()):
            if sec != "other":
                status = "✅" if content.strip() else "❌"
                st.write(f"{status} **{sec.capitalize()}**")

        st.markdown("#### Extracted Clean Text")
        st.text_area("Cleaned Text Output", parsed["cleaned_text"], height=200)

elif analyze_button and len(resume_content) <= 40:
    st.warning("Please upload a resume file or paste at least 40 characters of resume text to analyze.")
else:
    st.info("👆 Upload a resume above or select a sample candidate profile from the left sidebar to begin!")
