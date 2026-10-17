# 📄 ResuMetric AI — Professional AI Resume Analyzer & ATS Auditor

> **An enterprise-grade, 100% Python-powered AI Resume Evaluation platform designed to showcase during tech and corporate interviews.**

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Flask](https://img.shields.io/badge/Backend-Flask-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![NLP Engine](https://img.shields.io/badge/NLP-Regex%20%7C%20Heuristics%20%7C%20LLM-008080)](https://github.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Overview & Problem Statement

Most resumes never reach human recruiters because Applicant Tracking Systems (ATS) reject up to **75% of applicants** due to formatting issues, missing keywords, passive voice, or a lack of quantifiable achievements.

**ResuMetric AI** solves this problem by functioning as a high-fidelity **ATS Auditor & Resume Coach**. It parses PDF, DOCX, and TXT resumes, benchmarks them against industry standards and specific Job Descriptions, audits weak points, identifies missing technical & soft skills, and rewrites weak resume bullet points using **Google's XYZ Formula**.

---

## ✨ Key Features

- **🔍 Multi-Format Text Extraction**:
  - Robust text parsing from PDF (`pypdf`), DOCX (`python-docx`), and plain text.
  - Automatically detects scanned/image-only PDFs and flags unparseable files with clear guidance.

- **🎯 Intelligent Skill Extraction (25+ Technologies & Soft Skills)**:
  - Strict regex boundary matching avoids false positives (e.g., distinguishing single-letter `C` from words like `CSS` or `Cloud`).
  - Detects technical skills: `Python`, `Java`, `C`, `C++`, `C#`, `SQL`, `HTML`, `CSS`, `JavaScript`, `TypeScript`, `Flask`, `Django`, `FastAPI`, `Git`, `GitHub`, `Docker`, `Kubernetes`, `Data Structures & Algorithms (DSA)`, `Machine Learning`, `Artificial Intelligence`, `Pandas`, `NumPy`, `AWS`, `Azure`, etc.
  - Detects key soft skills: `Communication`, `Teamwork`, `Problem-Solving`, `Leadership`, `Time Management`, `Analytical Thinking`.
  - Fully case-insensitive (`PYTHON`, `Python`, `python`).

- **🧩 Precision Missing Skills & JD Gap Analysis**:
  - Compares the candidate's extracted skills against the target Job Description (JD).
  - Pinpoints **Missing Technical Requirements** and **Missing Soft Skills**.
  - Intelligently differentiates between "No JD Provided" and "Skill Missing".

- **⚠️ Deep Weakness & Risk Detection**:
  - Audits 6 critical risk categories:
    1. Weak/Passive verbs (e.g., *assisted*, *helped*, *worked on*).
    2. Lack of quantifiable impact metrics (missing `%`, `$`, numbers, scale).
    3. Missing contact hygiene (missing LinkedIn or GitHub profiles).
    4. Sub-optimal word count (flagging too short <400 or too long >850 words).
    5. Fluff/Buzzwords (e.g., *go-getter*, *hardworking*, *guru*).
    6. Missing essential ATS structural sections (Experience, Skills, Education, Projects).

- **🚀 Google XYZ Bullet Point Rewriter**:
  - Automatically transforms passive descriptions into Google's acclaimed formula:
    > *"Accomplished [X] as measured by [Y], by doing [Z]"*
  - Works offline via algorithmic heuristics or connects with Google Gemini API for generative rewriting.

- **🎙️ Stack-Tailored Interview Question Generator**:
  - Analyzes the candidate's detected technical stack and generates customized technical, architectural, and behavioral (STAR) interview questions with model answer strategies.

- **⚡ Dual Interface Options**:
  - **Streamlit Web App**: 100% Pure Python UI with live metric cards, interactive charts, and tabs.
  - **Flask REST API Dashboard**: Modern glassmorphic dark-mode web application with SVG radial score gauge and Chart.js radar charts.

---

## 🏗️ System Architecture

```
                          ┌───────────────────────────────────────────┐
                          │          Resume File (PDF/DOCX/TXT)       │
                          └─────────────────────┬─────────────────────┘
                                                │
                                                ▼
                          ┌───────────────────────────────────────────┐
                          │         ResumeParser (pypdf/docx)         │
                          │   - Clean text extraction                 │
                          │   - Contact details (Email, Phone, Links) │
                          │   - Section classification                │
                          └─────────────────────┬─────────────────────┘
                                                │
                        ┌───────────────────────┴───────────────────────┐
                        ▼                                               ▼
           ┌─────────────────────────┐                     ┌─────────────────────────┐
           │     ATSEngine (NLP)     │                     │     JobMatcher (JD)     │
           │ - Action Verbs (25%)    │                     │ - Skill Intersection    │
           │ - Impact Metrics (25%)  │                     │ - Keyword Gap Analysis  │
           │ - Structure (15%)       │                     │ - Missing Tech & Soft   │
           │ - Skills Depth (15%)    │                     └─────────────────────────┘
           │ - Contact Hygiene (10%) │
           │ - Readability (10%)     │
           └────────────┬────────────┘
                        │
                        ▼
           ┌─────────────────────────────────────────────────────────┐
           │                  Actionable Modules                     │
           │ - Google XYZ Bullet Rewriter (optimizer.py)             │
           │ - Tailored Interview Generator (interview_gen.py)       │
           │ - In-Depth Weakness Audit Report                        │
           └─────────────────────────────────────────────────────────┘
```

---

## 📊 ATS Scoring Weights

| Dimension | Weight | Target Criteria |
| :--- | :---: | :--- |
| **Quantifiable Impact** | **25%** | Percentages (`%`), revenue/dollar figures (`$`), scale multipliers (`2x`), metrics |
| **Action Verb Strength** | **25%** | Active action verbs (*Architected, Automated, Spearheaded*) vs passive verbs |
| **Structural Completeness** | **15%** | Standard headings: Experience, Skills, Education, Projects, Summary |
| **Skill Depth & Breadth** | **15%** | Verified coverage across languages, frameworks, databases, and DevOps |
| **Contact Hygiene** | **10%** | Clean email, validated phone number, LinkedIn URL, and GitHub link |
| **Readability & Formatting** | **10%** | Optimal length (400–850 words) and absence of buzzwords/filler words |

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application

#### Option A: Streamlit UI (Pure Python — Recommended)
```bash
python run_streamlit.py
```
*Access in browser at: `http://localhost:8501`*

#### Option B: Flask Dashboard
```bash
python app.py
```
*Access in browser at: `http://127.0.0.1:5000`*

#### Option C: Windows Batch Launcher
Double-click `start.bat` to launch with an interactive CLI menu.

---

## 🧪 Running Automated Tests

A dedicated test suite is provided to verify skill extraction, negative boundary tests, and JD gap calculations:

```bash
python test_skills_fix.py
```

---

## 📂 Project Directory Structure

```
ai-resume-analyzer/
├── run_streamlit.py          # 1-click Streamlit pure-Python launcher
├── streamlit_app.py          # 100% Pure Python Web App (Streamlit)
├── app.py                    # Flask REST API & backend application
├── requirements.txt          # Python dependencies
├── .gitignore                # Git ignore rules
├── start.bat                 # Unified startup selector (Windows)
├── run_streamlit.bat         # Direct Streamlit batch launcher
├── run_flask.bat             # Direct Flask batch launcher
├── test_skills_fix.py        # Automated test suite for skill extraction
├── README.md                 # Complete documentation & interview guide
├── analyzer/
│   ├── __init__.py           # Package exports
│   ├── parser.py             # PDF, DOCX, TXT parser & entity extractor
│   ├── ats_engine.py         # 6-dimension weighted ATS engine & weak point auditor
│   ├── jd_matcher.py         # Job description skill gap & keyword matcher
│   ├── optimizer.py          # Google XYZ & STAR bullet point rewriter
│   └── interview_gen.py      # Resume-tailored interview question generator
├── static/
│   ├── css/
│   │   └── style.css         # Modern dark-mode styling & responsive layout
│   └── js/
│       └── app.js            # Client-side API interactions & UI animations
└── templates/
    └── index.html            # Flask HTML5 executive dashboard
```

---

## 💬 How to Explain This Project in Interviews

When an interviewer asks: **"Walk me through a project you've built recently."**

### 1. The 60-Second Elevator Pitch
> *"I designed and built **ResuMetric AI**, an end-to-end resume evaluation and ATS optimization platform in Python. It solves the black-box problem of applicant tracking systems by analyzing resumes across six weighted dimensions, detecting missing technical and soft skills against job descriptions, identifying structural weaknesses, and rewriting bullet points using Google's XYZ formula."*

### 2. Key Engineering Highlights to Mention
- **Zero-Latency Heuristics + LLM Hybrid**: Designed the core parsing and scoring algorithms using regex lookarounds and deterministic tokenization so it runs completely offline with 0ms external API dependency, while adding optional Google Gemini LLM support for generative re-writing.
- **Accurate Word Boundary Protection**: Solved ambiguous token collisions (such as the programming language `C` matching inside `CSS` or `Cloud`) using negative regex lookbehinds and lookaheads.
- **Full-Stack Flexibility**: Provided dual frontend implementations—a rapid data-centric UI built entirely in pure Python via Streamlit, and a decoupled REST API with Flask and responsive CSS/JavaScript.

---

## 📄 License
This project is licensed under the MIT License - feel free to use it for portfolio and demonstration purposes!
