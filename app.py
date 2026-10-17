"""
AI Resume Analyzer - Flask Web Application
"""
import os
import sys
from flask import Flask, request, jsonify, render_template, send_from_directory

# Ensure local imports work cleanly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analyzer.parser import ResumeParser
from analyzer.ats_engine import ATSEngine
from analyzer.jd_matcher import JobMatcher
from analyzer.optimizer import BulletOptimizer
from analyzer.interview_gen import InterviewQuestionGenerator

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max upload limit

# Initialize core engines
parser = ResumeParser()
ats_engine = ATSEngine()
jd_matcher = JobMatcher()
bullet_optimizer = BulletOptimizer()
interview_gen = InterviewQuestionGenerator()


SAMPLE_DATA = {
    "fullstack": {
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
Location: Remote / San Francisco, CA
Company: ScaleUp Tech Corp

About the Role:
We are seeking a seasoned Senior Full-Stack Engineer to scale our next-generation cloud collaboration suite. You will design, build, and maintain mission-critical web applications and APIs used by millions globally.

Key Responsibilities:
• Architect, build, and deploy reliable, low-latency microservices using Node.js, TypeScript, and Go.
• Build delightful, responsive user interfaces using React, Next.js, and modern CSS/Tailwind.
• Optimize relational and NoSQL databases (PostgreSQL, Redis) for massive throughput and scale.
• Champion DevOps best practices using AWS, Docker, Kubernetes, and CI/CD pipelines.
• Collaborate with product managers and lead code reviews to mentor junior engineers.

Requirements:
• 5+ years of experience with React, TypeScript, Node.js, and SQL (PostgreSQL).
• Proven track record architecting distributed microservices and REST / GraphQL APIs.
• Strong hands-on experience with Docker, Kubernetes, and AWS cloud infrastructure.
• Deep understanding of CI/CD, automated testing (Jest, Cypress), and system design.
• Excellent communication skills and passion for mentoring peers.
"""
    },
    "ai_ml": {
        "title": "AI / Machine Learning Engineer",
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
        "job_description": """Position: Senior AI / Machine Learning Engineer
Company: DeepMatrix AI
Requirements:
• 3+ years experience developing production ML / Deep Learning applications.
• Mastery of Python, PyTorch, Hugging Face, and modern LLM architectures.
• Hands-on expertise building RAG pipelines, Vector Databases (Pinecone, Milvus), and LangChain.
• Experience with MLOps: Docker, Kubernetes, AWS SageMaker, and model quantization (LoRA/QLoRA).
• Strong computer science fundamentals and publications/projects in NLP or LLMs.
"""
    },
    "product_manager": {
        "title": "Technical Product Manager",
        "resume": """MARCUS CHEN
New York, NY | (555) 438-9921 | marcus.chen@pmlead.com | linkedin.com/in/marcus-chen-pm

PROFESSIONAL SUMMARY
Technical Product Manager with 5+ years of experience steering high-impact B2B SaaS products from concept to market leadership. Spearheaded product strategy for a fintech analytics dashboard, growing ARR from $1.2M to $8.5M in 24 months. Expert in Agile/Scrum, customer discovery, data analytics, and API ecosystem design.

SKILLS
• Product Strategy: Product Roadmapping, Go-To-Market (GTM), PRDs, Customer Discovery, OKRs, A/B Testing
• Analytics & Tools: SQL, Mixpanel, Amplitude, Google Analytics, Jira, Figma, Tableau
• Technical Foundation: REST APIs, System Architecture, Cloud Basics, Microservices Concepts
• Leadership: Cross-Functional Team Leadership, Stakeholder Management, Agile/Scrum Master

EXPERIENCE
Senior Product Manager | Veloce Financial Tech, New York, NY | 2021 – Present
• Spearheaded end-to-end launch of automated compliance reporting module, capturing 45 enterprise tier accounts and generating $3.2M net-new ARR.
• Defined product roadmap and led 2 cross-functional squads of 14 engineers and designers using Agile sprint cadences.
• Conducted 80+ customer interviews and leveraged SQL and Amplitude tracking to eliminate onboarding drop-off, increasing 30-day user retention by 24%.

Associate Product Manager | CloudStack Inc, Boston, MA | 2019 – 2021
• Managed developer API documentation portal and self-serve onboarding, accelerating developer integration velocity by 35%.
• Spearheaded weekly sprint planning, user story grooming, and QA acceptance testing across 4 product releases.

EDUCATION
• MBA, Technology Management | NYU Stern School of Business
• B.S. in Information Systems | Boston University
""",
        "job_description": """Position: Technical Product Manager
Company: Apex FinTech
Requirements:
• 4+ years of B2B SaaS product management experience.
• Strong technical background with ability to write technical PRDs and collaborate with engineers on APIs.
• Proven track record using SQL, Amplitude, Mixpanel, and data-driven decision making.
• Demonstrated success delivering revenue growth (ARR) and retention improvements.
• Exceptional stakeholder management and Agile / Scrum leadership.
"""
    }
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze_resume():
    try:
        resume_text = ""
        filename = ""

        # Check if file was uploaded
        if "file" in request.files and request.files["file"].filename != "":
            uploaded_file = request.files["file"]
            filename = uploaded_file.filename
            file_bytes = uploaded_file.read()
            resume_text = parser.extract_text_from_bytes(file_bytes, filename)
        else:
            # Check JSON payload
            data = request.get_json(silent=True) or request.form
            resume_text = data.get("resume_text", "")
            filename = data.get("filename", "resume.txt")

        if not resume_text or len(resume_text.strip()) < 15:
            return jsonify({
                "error": "The resume text is empty or too short. If you uploaded a scanned PDF, please upload a text-based PDF or copy-paste your resume text directly."
            }), 400

        # Get optional Job Description
        data = request.get_json(silent=True) or request.form
        job_description = data.get("job_description", "")

        # 1. Parse structure
        parsed = parser.parse(resume_text)

        # 2. Compute ATS scoring & diagnostics
        ats_result = ats_engine.evaluate(parsed)

        # 3. Match against Job Description (if supplied)
        jd_result = jd_matcher.match(resume_text, job_description)

        # 4. Generate Tailored Interview Questions
        interview_questions = interview_gen.generate(ats_result["detected_skills"], parsed["contact_info"]["name"])

        # Compile full response
        response = {
            "success": True,
            "filename": filename,
            "metadata": {
                "word_count": parsed["word_count"],
                "char_count": parsed["char_count"],
                "bullet_count": len(parsed["bullet_points"]),
            },
            "contact_info": parsed["contact_info"],
            "sections_detected": {k: bool(v.strip()) for k, v in parsed["sections"].items()},
            "bullet_points_sample": parsed["bullet_points"][:8],
            "ats_score": ats_result["score"],
            "ats_grade": ats_result["grade"],
            "tier_label": ats_result["tier_label"],
            "tier_color": ats_result["tier_color"],
            "total_detected_skills": ats_result["total_detected_skills"],
            "all_detected_skills_list": ats_result["all_detected_skills_list"],
            "breakdown": ats_result["breakdown"],
            "detected_skills": ats_result["detected_skills"],
            "strengths": ats_result["strengths"],
            "improvements": ats_result["improvements"],
            "weak_points": ats_result["weak_points"],
            "missing_domain_skills": ats_result["missing_domain_skills"],
            "job_match": jd_result,
            "interview_questions": interview_questions,
            "raw_text": parsed["cleaned_text"]
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/optimize-bullet", methods=["POST"])
def optimize_bullet():
    try:
        data = request.get_json(force=True)
        bullet = data.get("bullet", "").strip()
        role = data.get("role", "Software Engineer")
        api_key = data.get("api_key", None)
        api_provider = data.get("api_provider", "gemini")

        if not bullet:
            return jsonify({"error": "Please provide a bullet point to optimize."}), 400

        result = bullet_optimizer.optimize(bullet, role, api_key, api_provider)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/sample", methods=["POST", "GET"])
def get_sample():
    role_type = request.args.get("role") or (request.get_json(silent=True) or {}).get("role", "fullstack")
    sample = SAMPLE_DATA.get(role_type, SAMPLE_DATA["fullstack"])
    return jsonify({
        "success": True,
        "role": role_type,
        "title": sample["title"],
        "resume": sample["resume"],
        "job_description": sample["job_description"]
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "AI Resume Analyzer",
        "version": "2.4.0",
        "ready": True
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 AI Resume Analyzer running at: http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
