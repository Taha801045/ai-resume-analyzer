"""
Job Description Matcher: Compares resume content against a specific job posting
to calculate Match %, Skill Gap Analysis, and Missing Keyword recommendations.
"""
import re
from typing import Dict, Any, List, Set


class JobMatcher:
    def __init__(self):
        # Comprehensive list of industry keywords & technologies to scan for in JD and resume
        self.tech_vocabulary = {
            # Languages
            "python", "java", "c", "c++", "c#", "javascript", "typescript", "golang", "go",
            "rust", "ruby", "php", "swift", "kotlin", "scala", "sql", "r", "html", "html5", "css", "css3",
            # Frameworks & Libs
            "react", "react.js", "next.js", "vue", "vue.js", "angular", "node.js", "express",
            "django", "flask", "fastapi", "spring boot", "asp.net", "laravel", "rails",
            "tailwind", "tailwind css", "bootstrap", "redux", "graphql", "rest api", "restful api", "grpc",
            # Cloud & DevOps
            "aws", "amazon web services", "azure", "gcp", "google cloud", "docker",
            "kubernetes", "ci/cd", "terraform", "ansible", "jenkins", "linux", "nginx",
            "git", "github", "gitlab", "cloudformation", "serverless", "microservices",
            # Data & AI
            "postgresql", "postgres", "mysql", "mongodb", "redis", "elasticsearch", "kafka",
            "rabbitmq", "machine learning", "deep learning", "nlp", "llm", "rag",
            "pytorch", "tensorflow", "scikit-learn", "pandas", "numpy", "power bi", "tableau",
            "artificial intelligence", "opencv", "langchain", "hugging face", "dsa",
            "data structures", "algorithms",
            # Concepts & Practices
            "agile", "scrum", "system design", "distributed systems", "tdd", "unit testing",
            "code review", "devops", "security", "oauth", "jwt", "scalability", "performance",
            "communication", "teamwork", "problem-solving", "leadership", "time management"
        }

    def match(self, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """Calculates Job Match %, matched skills, and genuinely missing keywords."""
        if not jd_text or len(jd_text.strip()) < 20:
            return {
                "has_jd": False,
                "match_percentage": 0,
                "total_jd_skills_found": 0,
                "matched_keywords": [],
                "missing_keywords": [],
                "message": "Paste a Job Description above to compare required skills with your resume and see genuinely missing skills.",
                "recommendations": ["Paste a target Job Description to unlock customized Keyword Match & Skill Gap analysis."]
            }

        resume_clean = resume_text.lower()
        jd_clean = jd_text.lower()

        # Extract terms present in JD and Resume
        jd_keywords = self._extract_terms(jd_clean)
        resume_keywords = self._extract_terms(resume_clean)

        if not jd_keywords:
            jd_keywords = self._extract_fallback_words(jd_clean)

        # Calculate intersections and differences
        # Matched = in both JD and Resume
        # Missing = in JD but NOT in Resume
        matched = jd_keywords.intersection(resume_keywords)
        missing = jd_keywords.difference(resume_keywords)

        total_jd_terms = len(jd_keywords)
        match_rate = round((len(matched) / total_jd_terms * 100)) if total_jd_terms > 0 else 0
        match_rate = max(0, min(100, match_rate))

        # Recommendations
        recommendations = []
        if match_rate >= 80:
            recommendations.append(f"Outstanding match ({match_rate}%)! Your resume closely reflects the required tech stack.")
        elif match_rate >= 60:
            recommendations.append(f"Strong match ({match_rate}%). Adding a few missing skills below can push your resume to top candidate status.")
        else:
            recommendations.append(f"Match rate is {match_rate}%. Integrate genuinely missing core skills to pass automated ATS screening filters.")

        missing_list = sorted(list(missing), key=lambda x: len(x), reverse=False)
        matched_list = sorted(list(matched), key=lambda x: len(x), reverse=False)

        if missing_list:
            top_missing = missing_list[:6]
            recommendations.append(f"Keywords to incorporate naturally: {', '.join([self._format_skill_name(k) for k in top_missing])}.")
        else:
            recommendations.append("All key skills from this job description were found in your resume!")

        return {
            "has_jd": True,
            "match_percentage": match_rate,
            "total_jd_skills_found": total_jd_terms,
            "matched_keywords": [self._format_skill_name(k) for k in matched_list],
            "missing_keywords": [self._format_skill_name(k) for k in missing_list],
            "recommendations": recommendations,
        }

    def _extract_terms(self, text: str) -> Set[str]:
        found = set()
        for term in self.tech_vocabulary:
            if term == "c":
                pattern = r"(?:\b(?:languages?|programming|skills?|tools?)[:\s][^\n.]*?\b[Cc]\b(?![+#])|(?<![\w+#])\b[Cc]\b(?=\s*[,/|&]\s*(?:C\+\+|C#|Java|Python|SQL))|(?:\b(?:C\+\+|C#|Java|Python|SQL)[,/|&]\s*)\b[Cc]\b(?![+#])|\b[Cc]\s+(?:programming|language)\b)"
            elif term == "c++":
                pattern = r"(?<![\w+#])c\+\+(?![a-zA-Z0-9_#])"
            elif term == "c#":
                pattern = r"(?<![\w+#])c#(?![\w#+])|\bc\s*sharp\b"
            elif term == "git":
                pattern = r"\bgit\b(?!\s*(?:hub|lab))"
            elif term == "dsa":
                pattern = r"\b(?:dsa|data\s+structures?(?:\s+and\s+algorithms?)?)\b"
            elif term == "html":
                pattern = r"\bhtml(?:5)?\b"
            elif term == "css":
                pattern = r"\bcss(?:3)?\b"
            else:
                pattern = r"(?<![a-zA-Z0-9_])" + re.escape(term) + r"(?![a-zA-Z0-9_])"

            if re.search(pattern, text, re.IGNORECASE):
                # Canonical normalization
                normalized = term
                if term in ["html5", "html"]:
                    normalized = "html"
                elif term in ["css3", "css"]:
                    normalized = "css"
                elif term in ["postgres", "postgresql"]:
                    normalized = "postgresql"
                elif term in ["nodejs", "node.js"]:
                    normalized = "node.js"
                found.add(normalized)
        return found

    def _format_skill_name(self, skill: str) -> str:
        special_names = {
            "sql": "SQL", "html": "HTML", "css": "CSS", "dsa": "DSA",
            "nlp": "NLP", "llm": "LLM", "rag": "RAG", "ci/cd": "CI/CD",
            "aws": "AWS", "gcp": "GCP", "c++": "C++", "c#": "C#", "c": "C",
            "rest api": "REST API", "restful api": "REST API",
            "opencv": "OpenCV", "numpy": "NumPy", "pandas": "Pandas",
            "pytorch": "PyTorch", "tensorflow": "TensorFlow", "mongodb": "MongoDB",
            "mysql": "MySQL", "postgresql": "PostgreSQL", "github": "GitHub",
            "gitlab": "GitLab", "javascript": "JavaScript", "typescript": "TypeScript"
        }
        return special_names.get(skill.lower(), skill.title())

    def _extract_fallback_words(self, text: str) -> Set[str]:
        words = re.findall(r"\b[a-z]{3,15}\b", text)
        stopwords = {
            "the", "and", "for", "with", "you", "that", "this", "will", "are", "have",
            "from", "your", "our", "work", "team", "role", "years", "experience",
            "looking", "must", "able", "requirements", "responsibilities", "about"
        }
        return set(w for w in words if w not in stopwords)[:12]
