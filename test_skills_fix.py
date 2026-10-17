"""
Verification Test Script for AI Resume Analyzer Skill Detection
"""
import sys
import os

# Ensure local analyzer import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analyzer.parser import ResumeParser
from analyzer.ats_engine import ATSEngine
from analyzer.jd_matcher import JobMatcher

parser = ResumeParser()
engine = ATSEngine()
matcher = JobMatcher()

print("=" * 60)
print("TEST 1: Required Skills Detection & Case-Insensitivity")
print("=" * 60)

test_resume = """
ALEXANDER SMITH
alex@example.com | (555) 019-2834 | linkedin.com/in/alex-smith | github.com/alex-dev

TECHNICAL SKILLS:
• Languages: PYTHON, Java, C, C++, SQL, JavaScript, HTML, CSS
• Frameworks & Tools: Flask, Django, Git, GitHub, Pandas, NumPy
• Core Computer Science: Data Structures and Algorithms (DSA), System Design
• AI & Data: Machine Learning, Artificial Intelligence

SOFT SKILLS:
Demonstrated strong communication, teamwork, problem-solving, leadership, time management, and analytical thinking across cross-functional teams.

EXPERIENCE:
Software Engineer | Tech Corp | 2022 - Present
• Engineered web services using Python, Flask, and PostgreSQL, reducing latency by 35%.
• Architected responsive UI using HTML, CSS, and JavaScript.
"""

parsed = parser.parse(test_resume)
result = engine.evaluate(parsed)

detected_skills = result["detected_skills"]
total_skills = result["total_detected_skills"]
all_skills = result["all_detected_skills_list"]

print(f"Total Detected Skills: {total_skills}")
for cat, skills in detected_skills.items():
    print(f"  [{cat}]: {', '.join(skills)}")

# Required technical checks
required_tech = [
    "Python", "Java", "C", "C++", "SQL", "HTML", "CSS", "JavaScript",
    "Flask", "Django", "Git", "GitHub", "Data Structures & Algorithms (DSA)",
    "Machine Learning", "Artificial Intelligence (AI)", "Pandas", "NumPy"
]

# Required soft checks
required_soft = [
    "Communication", "Teamwork", "Problem-Solving", "Leadership",
    "Time Management", "Analytical Thinking"
]

all_found = True
for req in required_tech + required_soft:
    if req in all_skills:
        print(f"  [OK] Found: {req}")
    else:
        print(f"  [X] MISSING: {req}")
        all_found = False

assert all_found, "Some required skills were not detected!"
print("\n>>> TEST 1 PASSED: All 23 required technical and soft skills detected cleanly!")

print("\n" + "=" * 60)
print("TEST 2: Accurate Boundary Matching (No False Positives)")
print("=" * 60)
# Testing resume with NO 'C' language, but words containing letter 'c'
negative_c_resume = """
John Doe | john@doe.com
EXPERIENCE:
Accomplished critical architectural changes. Section (c) of report. 
Vitamin C supplements. Worked on C++ and C# systems.
"""
neg_parsed = parser.parse(negative_c_resume)
neg_result = engine.evaluate(neg_parsed)
neg_skills = neg_result["all_detected_skills_list"]

print("Detected in negative C resume:", neg_skills)
assert "C" not in neg_skills, "False positive! Letter 'c' was matched as C language."
assert "C++" in neg_skills, "C++ should be detected."
assert "C#" in neg_skills, "C# should be detected."
print(">>> TEST 2 PASSED: 'C' was NOT falsely detected inside words, bullets, or C++/C#!")

print("\n" + "=" * 60)
print("TEST 3: Job Description Matching (Genuine Missing Skills)")
print("=" * 60)
# Candidate has: Python, Java, SQL, HTML, CSS, Machine Learning
cand_resume = """
Skills: Python, Java, SQL, HTML, CSS, Machine Learning.
"""
# Job description requires: Python, SQL, Docker, Kubernetes, React
job_desc = """
Requirements:
Must have experience with Python, SQL, Docker, Kubernetes, and React.
"""
jd_result = matcher.match(cand_resume, job_desc)
print(f"Job Match %: {jd_result['match_percentage']}%")
print(f"Matched Skills: {jd_result['matched_keywords']}")
print(f"Missing Skills: {jd_result['missing_keywords']}")

assert "Python" in jd_result["matched_keywords"], "Python should be matched!"
assert "SQL" in jd_result["matched_keywords"], "SQL should be matched!"
assert "Docker" in jd_result["missing_keywords"], "Docker should be missing!"
assert "Kubernetes" in jd_result["missing_keywords"], "Kubernetes should be missing!"
assert "Python" not in jd_result["missing_keywords"], "Python should NEVER be marked as missing!"
assert "SQL" not in jd_result["missing_keywords"], "SQL should NEVER be marked as missing!"

print(">>> TEST 3 PASSED: Present skills are NOT marked missing; only genuine gaps (Docker, Kubernetes, React) are flagged!")

print("\n" + "=" * 60)
print("TEST 4: No Job Description Provided (Helpful Message)")
print("=" * 60)
no_jd_result = matcher.match(cand_resume, "")
print("has_jd:", no_jd_result["has_jd"])
print("missing_keywords:", no_jd_result["missing_keywords"])
assert not no_jd_result["has_jd"], "has_jd should be False when no JD is provided"
assert len(no_jd_result["missing_keywords"]) == 0, "Missing keywords should be empty when no JD is provided"
print(">>> TEST 4 PASSED: No confusing missing skills shown when no JD provided!")

print("\nALL VERIFICATION TESTS COMPLETED SUCCESSFULLY!")
