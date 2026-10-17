"""
ATS Scoring Engine: Evaluates resume content against industry ATS standards,
metrics density, action verb strength, formatting, and structural completeness.
Includes robust case-insensitive skill extraction, weak points audit, and skill gap detection.
"""
import re
from typing import Dict, Any, List, Set, Tuple


class ATSEngine:
    def __init__(self):
        # High impact action verbs
        self.strong_action_verbs = {
            "architected", "spearheaded", "engineered", "orchestrated", "optimized",
            "automated", "streamlined", "accelerated", "pioneered", "refactored",
            "deployed", "developed", "designed", "implemented", "revamped",
            "formulated", "executed", "maximized", "integrated", "transformed",
            "delivered", "centralized", "benchmarked", "migrated", "mentored",
            "built", "established", "headed", "solved", "reduced", "increased"
        }

        # Weak or passive phrases to avoid
        self.weak_phrases = [
            "responsible for", "duties included", "helped with", "assisted in",
            "worked on", "participated in", "handled", "was tasked with",
            "familiar with", "involved in", "contributed to"
        ]

        # Vague buzzwords / clichés
        self.buzzwords = [
            "hard worker", "team player", "go-getter", "detail-oriented",
            "self-starter", "think outside the box", "results-driven",
            "dynamic", "motivated", "fast learner", "people person", "synergy"
        ]

        # Standard technical & soft skills definitions:
        # Format: (Canonical Display Name, Category, Regex Pattern)
        self.skill_definitions: List[Tuple[str, str, str]] = [
            # --- Programming Languages ---
            ("Python", "Programming Languages", r"\bpython(?:3)?\b"),
            ("Java", "Programming Languages", r"\bjava\b(?!\s*script)"),
            ("C", "Programming Languages", r"(?:\b(?:languages?|programming|skills?|technologies|tools?|stack)[:\s][^\n.]*?\b[Cc]\b(?![+#])|(?<![\w+#])\b[Cc]\b(?=\s*[,/|&]\s*(?:C\+\+|C#|Java|Python|SQL|Assembly|R|Rust))|(?:\b(?:C\+\+|C#|Java|Python|SQL|Assembly|R|Rust)\s*[,/|&]\s*)\b[Cc]\b(?![+#])|\b[Cc]\s+(?:programming|language)\b|\bproficient\s+in\s+[Cc]\b)"),
            ("C++", "Programming Languages", r"(?<![\w+#])c\+\+(?![a-zA-Z0-9_#])"),
            ("C#", "Programming Languages", r"(?<![\w+#])c#(?![\w#+])|\bc\s*sharp\b"),
            ("JavaScript", "Programming Languages", r"\b(?:javascript|js)\b"),
            ("TypeScript", "Programming Languages", r"\b(?:typescript|ts)\b"),
            ("SQL", "Programming Languages", r"\bsql\b"),
            ("Go / Golang", "Programming Languages", r"\bgolang\b|(?<![\w])\bgo\b(?=\s+language|\s+programming|\s*[,/|]\s*(?:Rust|Python|Java|C\+\+|Docker|Kubernetes))"),
            ("Rust", "Programming Languages", r"\brust\b"),
            ("Ruby", "Programming Languages", r"\bruby\b"),
            ("PHP", "Programming Languages", r"\bphp\b"),
            ("Swift", "Programming Languages", r"\bswift\b"),
            ("Kotlin", "Programming Languages", r"\bkotlin\b"),

            # --- Web & Frontend ---
            ("HTML", "Web & Frontend", r"\bhtml(?:5)?\b"),
            ("CSS", "Web & Frontend", r"\bcss(?:3)?\b"),
            ("React", "Web & Frontend", r"\breact(?:\.js)?\b"),
            ("Next.js", "Web & Frontend", r"\bnext(?:\.js)?\b"),
            ("Vue.js", "Web & Frontend", r"\bvue(?:\.js)?\b"),
            ("Angular", "Web & Frontend", r"\bangular(?:\.js)?\b"),
            ("Tailwind CSS", "Web & Frontend", r"\btailwind(?:\s*css)?\b"),
            ("Bootstrap", "Web & Frontend", r"\bbootstrap\b"),
            ("Redux", "Web & Frontend", r"\bredux(?:\s*toolkit)?\b"),
            ("Sass", "Web & Frontend", r"\bsass\b|\bscss\b"),
            ("Webpack", "Web & Frontend", r"\bwebpack\b"),
            ("Vite", "Web & Frontend", r"\bvite\b"),

            # --- Backend & APIs ---
            ("Node.js", "Backend & APIs", r"\bnode(?:\.js)?\b"),
            ("Express.js", "Backend & APIs", r"\bexpress(?:\.js)?\b"),
            ("Flask", "Backend & APIs", r"\bflask\b"),
            ("Django", "Backend & APIs", r"\bdjango\b"),
            ("FastAPI", "Backend & APIs", r"\bfastapi\b"),
            ("Spring Boot", "Backend & APIs", r"\bspring(?:\s*boot)?\b"),
            ("REST API", "Backend & APIs", r"\brest(?:ful)?\s*api[s]?\b|\brest\s*api[s]?\b"),
            ("GraphQL", "Backend & APIs", r"\bgraphql\b"),
            ("Microservices", "Backend & APIs", r"\bmicroservices?\b"),

            # --- Databases & Storage ---
            ("PostgreSQL", "Databases", r"\bpostgres(?:ql)?\b"),
            ("MySQL", "Databases", r"\bmysql\b"),
            ("MongoDB", "Databases", r"\bmongo(?:db)?\b"),
            ("Redis", "Databases", r"\bredis\b"),
            ("SQLite", "Databases", r"\bsqlite\b"),
            ("Elasticsearch", "Databases", r"\belasticsearch\b"),
            ("Firebase", "Databases", r"\bfirebase\b"),
            ("Supabase", "Databases", r"\bsupabase\b"),
            ("Cassandra", "Databases", r"\bcassandra\b"),
            ("DynamoDB", "Databases", r"\bdynamodb\b"),

            # --- Cloud, DevOps & Tools ---
            ("Git", "Cloud, DevOps & Tools", r"\bgit\b(?!\s*(?:hub|lab))"),
            ("GitHub", "Cloud, DevOps & Tools", r"\bgithub\b"),
            ("GitLab", "Cloud, DevOps & Tools", r"\bgitlab\b"),
            ("Docker", "Cloud, DevOps & Tools", r"\bdocker\b"),
            ("Kubernetes", "Cloud, DevOps & Tools", r"\bkubernetes\b|\bk8s\b"),
            ("AWS", "Cloud, DevOps & Tools", r"\baws\b|\bamazon\s+web\s+services\b"),
            ("Azure", "Cloud, DevOps & Tools", r"\bazure\b"),
            ("GCP", "Cloud, DevOps & Tools", r"\bgcp\b|\bgoogle\s+cloud\b"),
            ("CI/CD", "Cloud, DevOps & Tools", r"\bci\s*/\s*cd\b|\bcontinuous\s+integration\b"),
            ("Linux", "Cloud, DevOps & Tools", r"\blinux\b"),
            ("Terraform", "Cloud, DevOps & Tools", r"\bterraform\b"),
            ("Jenkins", "Cloud, DevOps & Tools", r"\bjenkins\b"),
            ("Nginx", "Cloud, DevOps & Tools", r"\bnginx\b"),

            # --- AI, ML & Data Science ---
            ("Machine Learning", "AI & Data Science", r"\b(?:machine\s+learning|\bml\b(?=\s*[/&|,\s]+(?:ai|dl|nlp|data)|\s+(?:engineer|model|algorithm|pipeline)))\b"),
            ("Deep Learning", "AI & Data Science", r"\bdeep\s+learning\b"),
            ("Artificial Intelligence (AI)", "AI & Data Science", r"\b(?:artificial\s+intelligence|\bai\b(?=\s*[/&|,\s]+(?:ml|dl|nlp|data)|\s+(?:engineer|specialist|model|solution|research)))\b"),
            ("Pandas", "AI & Data Science", r"\bpandas\b"),
            ("NumPy", "AI & Data Science", r"\bnumpy\b"),
            ("PyTorch", "AI & Data Science", r"\bpytorch\b"),
            ("TensorFlow", "AI & Data Science", r"\btensorflow\b"),
            ("Scikit-learn", "AI & Data Science", r"\bscikit[\s-]learn\b|\bsklearn\b"),
            ("NLP", "AI & Data Science", r"\bnlp\b|\bnatural\s+language\s+processing\b"),
            ("LLMs / Generative AI", "AI & Data Science", r"\bllms?\b|\blarge\s+language\s+models?\b|\bgenerative\s+ai\b|\bgenai\b"),
            ("RAG", "AI & Data Science", r"\brag\b|\bretrieval[\s-]augmented\s+generation\b"),
            ("OpenCV", "AI & Data Science", r"\bopencv\b"),
            ("LangChain", "AI & Data Science", r"\blangchain\b"),
            ("Hugging Face", "AI & Data Science", r"\bhugging\s*face\b"),
            ("Data Analysis", "AI & Data Science", r"\bdata\s+analysis\b|\bdata\s+analytics\b"),

            # --- Core Computer Science ---
            ("Data Structures & Algorithms (DSA)", "Core Computer Science", r"\b(?:dsa|data\s+structures?(?:\s+and\s+algorithms?)?)\b"),
            ("System Design", "Core Computer Science", r"\bsystem\s+design\b|\bdistributed\s+systems\b"),
            ("OOP", "Core Computer Science", r"\boop\b|\bobject[\s-]oriented(?:\s+programming)?\b"),
            ("DBMS", "Core Computer Science", r"\bdbms\b|\bdatabase\s+management(?:\s+systems?)?\b"),

            # --- Soft Skills ---
            ("Communication", "Soft Skills", r"\bcommunications?\b|\bverbal\s+communication\b|\bwritten\s+communication\b"),
            ("Teamwork", "Soft Skills", r"\bteamwork\b|\bteam\s+player\b|\bcollaboration\b|\bcollaborative\b"),
            ("Problem-Solving", "Soft Skills", r"\bproblem[\s-]solving\b|\bproblem\s+solver\b"),
            ("Leadership", "Soft Skills", r"\bleadership\b|\bteam\s+lead(?:er)?\b|\bmentoring\b|\bmentorship\b"),
            ("Time Management", "Soft Skills", r"\btime\s+management\b|\bprioritization\b|\bmultitasking\b"),
            ("Analytical Thinking", "Soft Skills", r"\banalytical\s+thinking\b|\banalytical\s+skills?\b|\bcritical\s+thinking\b"),
            ("Agile / Scrum", "Soft Skills", r"\bagile\b|\bscrum\b")
        ]

        # Expected core industry benchmarks by domain (2026 Standards)
        self.domain_benchmarks = {
            "Full-Stack / Web": [
                ("TypeScript", "Web & Frontend", "HIGH", "Industry-standard for type-safe frontend & Node applications."),
                ("Docker", "Cloud, DevOps & Tools", "HIGH", "Mandatory for containerized deployment in 85% of tech roles."),
                ("CI/CD", "Cloud, DevOps & Tools", "HIGH", "Demonstrates experience with modern automated deployment pipelines."),
                ("PostgreSQL", "Databases", "HIGH", "Most popular relational database required in enterprise stacks."),
                ("Redis", "Databases", "MEDIUM", "Essential for high-throughput caching and session management."),
                ("Git / GitHub", "Cloud, DevOps & Tools", "HIGH", "Version control and collaborative software development.")
            ],
            "Backend": [
                ("Docker", "Cloud, DevOps & Tools", "HIGH", "Standard requirement for containerization and microservices."),
                ("CI/CD", "Cloud, DevOps & Tools", "HIGH", "Automated deployment and continuous integration experience."),
                ("PostgreSQL", "Databases", "HIGH", "Primary relational database engine in top tech companies."),
                ("Redis", "Databases", "MEDIUM", "Demonstrates distributed caching and performance tuning."),
                ("Microservices", "Backend & APIs", "MEDIUM", "Shows architecture scalability understanding."),
                ("Git / GitHub", "Cloud, DevOps & Tools", "HIGH", "Version control and team code collaboration.")
            ],
            "AI / Machine Learning": [
                ("PyTorch", "AI & Data Science", "HIGH", "Dominant deep learning framework for model development."),
                ("RAG / LLMs", "AI & Data Science", "HIGH", "Core 2026 requirement for modern generative AI pipelines."),
                ("Docker", "Cloud, DevOps & Tools", "HIGH", "Essential for packaging and serving machine learning models."),
                ("Pandas", "AI & Data Science", "HIGH", "Universal data manipulation and analysis tool."),
                ("Git / GitHub", "Cloud, DevOps & Tools", "HIGH", "Collaborative experiment tracking and code versioning.")
            ]
        }

    def evaluate(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates comprehensive ATS Score, dimensional diagnostics, weak points, and missing skills."""
        cleaned_text = parsed_data["cleaned_text"]
        bullets = parsed_data["bullet_points"]
        word_count = parsed_data["word_count"]
        contact = parsed_data["contact_info"]
        sections = parsed_data["sections"]

        # 1. Contact & Identity Score (10 pts)
        contact_score, contact_feedback = self._eval_contact(contact)

        # 2. Section Structure Score (15 pts)
        structure_score, structure_feedback = self._eval_structure(sections)

        # 3. Action Verb Strength (25 pts)
        action_score, action_feedback, found_strong, found_weak = self._eval_action_verbs(cleaned_text.lower(), bullets)

        # 4. Quantifiable Impact & Metrics (25 pts)
        impact_score, impact_feedback, num_metrics = self._eval_impact_metrics(cleaned_text.lower(), bullets)

        # 5. Technical & Soft Skills Extraction (15 pts)
        skills_score, skills_feedback, detected_skills, total_skills_count, all_skills_list = self._eval_skills(cleaned_text)

        # 6. ATS Formatting & Conciseness (10 pts)
        format_score, format_feedback, found_buzzwords = self._eval_formatting(word_count, cleaned_text.lower(), bullets)

        # Total ATS Score (0 - 100)
        total_score = round(
            contact_score + structure_score + action_score +
            impact_score + skills_score + format_score
        )
        total_score = max(5, min(100, total_score))

        # Letter grade and tier description
        grade, tier_label, tier_color = self._get_grade_info(total_score)

        # Compile strengths and general recommendations
        strengths, improvements = self._compile_recommendations(
            contact_feedback, structure_feedback, action_feedback,
            impact_feedback, skills_feedback, format_feedback, total_score
        )

        # Detailed Weak Points Audit (Kamzoriyan)
        weak_points = self._audit_weak_points(
            contact, sections, num_metrics, found_weak, found_strong,
            word_count, found_buzzwords, detected_skills, total_skills_count, total_score
        )

        # Missing Industry Skills Audit (Domain Skill Gaps)
        missing_domain_skills = self._audit_missing_domain_skills(detected_skills, cleaned_text)

        return {
            "score": total_score,
            "grade": grade,
            "tier_label": tier_label,
            "tier_color": tier_color,
            "total_detected_skills": total_skills_count,
            "all_detected_skills_list": all_skills_list,
            "detected_skills": detected_skills,
            "breakdown": {
                "impact_and_metrics": {
                    "score": round(impact_score),
                    "max": 25,
                    "percentage": round((impact_score / 25) * 100),
                    "title": "Measurable Impact & Metrics",
                    "feedback": impact_feedback
                },
                "action_verbs": {
                    "score": round(action_score),
                    "max": 25,
                    "percentage": round((action_score / 25) * 100),
                    "title": "Action Verbs & Phrasing",
                    "feedback": action_feedback
                },
                "structure_sections": {
                    "score": round(structure_score),
                    "max": 15,
                    "percentage": round((structure_score / 15) * 100),
                    "title": "Structural Completeness",
                    "feedback": structure_feedback
                },
                "skills_breadth": {
                    "score": round(skills_score),
                    "max": 15,
                    "percentage": round((skills_score / 15) * 100),
                    "title": "Technical Skills Depth",
                    "feedback": skills_feedback
                },
                "contact_hygiene": {
                    "score": round(contact_score),
                    "max": 10,
                    "percentage": round((contact_score / 10) * 100),
                    "title": "Contact Details & Links",
                    "feedback": contact_feedback
                },
                "ats_formatting": {
                    "score": round(format_score),
                    "max": 10,
                    "percentage": round((format_score / 10) * 100),
                    "title": "ATS Readability & Length",
                    "feedback": format_feedback
                }
            },
            "strengths": strengths,
            "improvements": improvements,
            "weak_points": weak_points,
            "missing_domain_skills": missing_domain_skills
        }

    def _eval_contact(self, contact: Dict[str, Any]):
        score = 0
        feedback = []

        if contact.get("email"):
            score += 3
        else:
            feedback.append("Missing professional email address.")

        if contact.get("phone"):
            score += 2
        else:
            feedback.append("Missing phone number.")

        if contact.get("linkedin"):
            score += 3
            feedback.append("LinkedIn profile link detected.")
        else:
            feedback.append("Consider adding a clean LinkedIn profile URL.")

        if contact.get("github") or contact.get("portfolio"):
            score += 2
            feedback.append("Portfolio / GitHub link detected.")
        else:
            feedback.append("Adding a GitHub or personal portfolio boosts recruiter engagement.")

        return min(10, score), feedback

    def _eval_structure(self, sections: Dict[str, str]):
        score = 0
        feedback = []

        crucial = [
            ("experience", 4, "Work Experience section detected."),
            ("skills", 4, "Skills section detected."),
            ("education", 3, "Education section detected."),
            ("projects", 2, "Projects section detected."),
            ("summary", 2, "Professional Summary detected.")
        ]

        for sec_name, weight, msg in crucial:
            if sections.get(sec_name) and len(sections[sec_name]) > 30:
                score += weight
            else:
                feedback.append(f"Missing or brief '{sec_name.capitalize()}' section.")

        return min(15, score), feedback

    def _eval_action_verbs(self, text: str, bullets: List[str]):
        found_strong = set()
        for verb in self.strong_action_verbs:
            if re.search(r"\b" + verb + r"\b", text):
                found_strong.add(verb)

        found_weak = set()
        for phrase in self.weak_phrases:
            if phrase in text:
                found_weak.add(phrase)

        # Score based on variety and density of strong verbs
        verb_count = len(found_strong)
        if verb_count >= 8:
            base_score = 25
        elif verb_count >= 5:
            base_score = 20
        elif verb_count >= 3:
            base_score = 14
        elif verb_count >= 1:
            base_score = 8
        else:
            base_score = 4

        # Penalty for passive phrases
        penalty = min(8, len(found_weak) * 2)
        score = max(4, base_score - penalty)

        feedback = []
        if verb_count >= 6:
            feedback.append(f"Excellent use of {verb_count} powerful action verbs (e.g., {', '.join(list(found_strong)[:4])}).")
        else:
            feedback.append(f"Only {verb_count} high-impact action verbs detected. Replace passive words with verbs like 'Spearheaded', 'Architected', 'Automated'.")

        if found_weak:
            feedback.append(f"Passive phrases found: {', '.join(list(found_weak)[:3])}. Reframe with direct action verbs.")

        return min(25, score), feedback, list(found_strong), list(found_weak)

    def _eval_impact_metrics(self, text: str, bullets: List[str]):
        metric_matches = re.findall(
            r"(\b\d+(\.\d+)?%|\$\d+[\d,]*(\.\d+)?|\b\d+x\b|\b\d{1,3}(,\d{3})+|\b\d+\+?\s*(users|clients|customers|requests|queries|seconds|minutes|hours|qps|ms|gb|tb|million|billion|k\b))",
            text, re.IGNORECASE
        )

        num_metrics = len(metric_matches)

        if num_metrics >= 6:
            score = 25
            feedback = [f"Strong quantifiable impact! Found {num_metrics} metrics with numbers, percentages, or scale."]
        elif num_metrics >= 3:
            score = 19
            feedback = [f"Decent metrics found ({num_metrics}). Aim to quantify 2-3 more achievements using the Google XYZ formula."]
        elif num_metrics >= 1:
            score = 12
            feedback = ["Few quantifiable metrics found. Add specific metrics (e.g., 'reduced latency by 35%', 'handled 50k+ daily users')."]
        else:
            score = 5
            feedback = ["CRITICAL: No measurable metrics found. Top ATS scores require percentages, dollars, or performance numbers to prove impact."]

        return min(25, score), feedback, num_metrics

    def _eval_skills(self, text: str):
        """Accurately extracts technical and soft skills using case-insensitive regex patterns."""
        detected_by_cat: Dict[str, List[str]] = {}
        all_unique_skills: Set[str] = set()

        for skill_name, category, pattern in self.skill_definitions:
            if re.search(pattern, text, re.IGNORECASE):
                if category not in detected_by_cat:
                    detected_by_cat[category] = []
                detected_by_cat[category].append(skill_name)
                all_unique_skills.add(skill_name)

        unique_count = len(all_unique_skills)
        if unique_count >= 12:
            score = 15
        elif unique_count >= 8:
            score = 13
        elif unique_count >= 5:
            score = 10
        elif unique_count >= 2:
            score = 7
        elif unique_count >= 1:
            score = 5
        else:
            score = 2

        if unique_count > 0:
            feedback = [f"Detected {unique_count} technical and soft skills across {len(detected_by_cat)} categories."]
        else:
            feedback = ["CRITICAL: 0 recognized skills detected. Make sure your resume includes standard technical keywords (e.g. Python, SQL, Git)."]

        return min(15, score), feedback, detected_by_cat, unique_count, sorted(list(all_unique_skills))

    def _eval_formatting(self, word_count: int, text: str, bullets: List[str]):
        score = 10
        feedback = []

        if 400 <= word_count <= 850:
            feedback.append(f"Optimal resume length ({word_count} words). Fits well on 1-2 pages.")
        elif word_count < 300:
            score -= 3
            feedback.append(f"Resume is on the shorter side ({word_count} words). Consider expanding work impact and projects.")
        elif word_count > 1000:
            score -= 2
            feedback.append(f"Resume is lengthy ({word_count} words). Try tightening descriptions to keep it under 850 words.")

        found_buzzwords = [bw for bw in self.buzzwords if bw in text]
        if found_buzzwords:
            score -= min(3, len(found_buzzwords))
            feedback.append(f"Avoid generic buzzwords like '{', '.join(found_buzzwords[:2])}'. Show concrete accomplishments instead.")

        return max(3, min(10, score)), feedback, found_buzzwords

    def _audit_weak_points(self, contact, sections, num_metrics, found_weak, found_strong,
                           word_count, found_buzzwords, detected_skills, total_skills_count, total_score) -> List[Dict[str, Any]]:
        """Deep audit that identifies exact weak points (Kamzoriyan), severity, and concrete fixes."""
        weak_points = []

        # Weak Point 0: Zero or very low skills detected
        if total_skills_count == 0:
            weak_points.append({
                "severity": "CRITICAL",
                "severity_label": "Critical Vulnerability",
                "color": "#ef4444",
                "category": "Technical Skills",
                "title": "Zero Recognized Technical Skills Detected",
                "issue": "Your resume does not contain recognizable industry skill keywords (e.g., Python, Java, SQL, HTML, Git). ATS algorithms will immediately reject this resume for technical roles.",
                "impact": "-15 to -20 Points ATS Loss",
                "how_to_fix": "Add a dedicated 'TECHNICAL SKILLS' section listing your Languages (Python, Java, C++), Web Tools (HTML, CSS, React), Databases (SQL, MongoDB), and Tools (Git, GitHub).",
                "example": "TECHNICAL SKILLS:\n• Languages: Python, Java, SQL, C++\n• Web & Frameworks: HTML, CSS, JavaScript, React\n• Tools & Cloud: Git, GitHub, Docker"
            })
        elif total_skills_count < 4:
            weak_points.append({
                "severity": "MODERATE",
                "severity_label": "Needs Improvement",
                "color": "#f59e0b",
                "category": "Technical Skills",
                "title": f"Low Number of Skills ({total_skills_count} Skills Detected)",
                "issue": f"Only {total_skills_count} skills were identified. Competitive resumes typically showcase 8 to 15 relevant technical and soft skills.",
                "impact": "-8 Points ATS Loss",
                "how_to_fix": "Expand your skills list to include companion technologies, libraries (e.g. Pandas, NumPy), version control (Git), and soft skills (Communication, Teamwork).",
                "example": "Add frameworks and core tools you utilized in your projects."
            })

        # Weak Point 1: Metrics & Numbers Absence
        if num_metrics == 0:
            weak_points.append({
                "severity": "CRITICAL",
                "severity_label": "Critical Vulnerability",
                "color": "#ef4444",
                "category": "Quantifiable Impact",
                "title": "Zero Measurable Numbers or Percentages Found",
                "issue": "Your bullet points only describe responsibilities rather than verified results. Over 75% of ATS screening tools and hiring managers reject resumes lacking numerical proof.",
                "impact": "-20 Points ATS Loss",
                "how_to_fix": "Rewrite at least 3 bullet points using Google's XYZ formula: 'Accomplished [X] as measured by [Y]%, by doing [Z]'. Add metrics like %, $, user scale, or time saved.",
                "example": "Change 'Worked on database queries' ➔ 'Optimized SQL queries and indexing, slashing p99 latency by 45% across 2M daily records.'"
            })
        elif num_metrics < 3:
            weak_points.append({
                "severity": "MODERATE",
                "severity_label": "Needs Improvement",
                "color": "#f59e0b",
                "category": "Quantifiable Impact",
                "title": "Low Density of Measurable Achievements",
                "issue": f"Only {num_metrics} quantified metrics detected across your entire resume. Top competitive tech resumes typically feature 5 to 8 quantifiable figures.",
                "impact": "-10 Points ATS Loss",
                "how_to_fix": "Quantify outcomes: How many users benefited? By what percentage did efficiency improve? How much latency or hosting cost was reduced?",
                "example": "Change 'Built frontend UI' ➔ 'Architected responsive UI component library, cutting page bundle size by 35% and accelerating load times by 1.6s.'"
            })

        # Weak Point 2: Passive Phrases & Weak Verbs
        if found_weak:
            weak_points.append({
                "severity": "MODERATE",
                "severity_label": "Weak Action Verbs",
                "color": "#f59e0b",
                "category": "Phrasing & Authority",
                "title": f"Passive Phrases Detected ({', '.join(found_weak[:3])})",
                "issue": f"Found phrases like '{', '.join(found_weak[:3])}'. These phrases make you sound like a passive participant rather than a proactive leader or builder.",
                "impact": "-8 Points ATS Loss",
                "how_to_fix": "Replace passive starters with high-impact past-tense action verbs: 'Spearheaded', 'Architected', 'Automated', 'Engineered', 'Orchestrated'.",
                "example": "Change 'Responsible for deploying servers' ➔ 'Automated zero-downtime CI/CD container deployments across AWS ECS using Docker.'"
            })

        # Weak Point 3: Missing Professional Links
        missing_links = []
        if not contact.get("linkedin"):
            missing_links.append("LinkedIn")
        if not contact.get("github") and not contact.get("portfolio"):
            missing_links.append("GitHub / Portfolio")

        if missing_links:
            weak_points.append({
                "severity": "MODERATE",
                "severity_label": "Missing Contact Assets",
                "color": "#f59e0b",
                "category": "Contact & Credibility",
                "title": f"Missing Essential Links ({', '.join(missing_links)})",
                "issue": f"No clean {', '.join(missing_links)} profile detected. Technical recruiters verify project proof via GitHub repositories and LinkedIn recommendations.",
                "impact": "-5 Points ATS Loss",
                "how_to_fix": "Add a clickable, clean link in your contact header (e.g., 'linkedin.com/in/yourname' and 'github.com/yourhandle').",
                "example": "Header Format: Name | Phone | Email | linkedin.com/in/dev | github.com/dev"
            })

        # Weak Point 4: Resume Word Count & Length
        if word_count < 350:
            weak_points.append({
                "severity": "CRITICAL",
                "severity_label": "Too Brief / Under-documented",
                "color": "#ef4444",
                "category": "Content Depth",
                "title": f"Resume is Too Short ({word_count} words)",
                "issue": "Your resume has fewer than 350 words. ATS engines flag overly brief resumes as lacking professional depth or technical experience.",
                "impact": "-12 Points ATS Loss",
                "how_to_fix": "Expand your Experience and Project sections. Add 3 to 4 detailed bullet points per role detailing technologies, architecture, and impact.",
                "example": "Ideal resume length for 1 to 5 years experience is between 450 and 850 words."
            })
        elif word_count > 1050:
            weak_points.append({
                "severity": "MINOR",
                "severity_label": "Too Verbose",
                "color": "#3b82f6",
                "category": "Formatting",
                "title": f"Resume is Verbose ({word_count} words)",
                "issue": "Resumes over 1,000 words risk losing recruiter attention within the initial 6-second scan.",
                "impact": "-4 Points ATS Loss",
                "how_to_fix": "Trim older experience descriptions and eliminate repetitive bullet points. Keep it strictly to 1 or 2 tight pages.",
                "example": "Target word count: 500 – 800 words."
            })

        # Weak Point 5: Generic Buzzwords & Fluff
        if found_buzzwords:
            weak_points.append({
                "severity": "MINOR",
                "severity_label": "Cliché Fluff",
                "color": "#3b82f6",
                "category": "Content Quality",
                "title": f"Generic Clichés Found ({', '.join(found_buzzwords[:3])})",
                "issue": f"Phrases like '{', '.join(found_buzzwords[:2])}' add no technical credibility. Recruiters look for concrete proof of skill rather than self-proclaimed soft traits.",
                "impact": "-3 Points ATS Loss",
                "how_to_fix": "Delete vague buzzwords and demonstrate soft skills through concrete team collaboration achievements.",
                "example": "Instead of 'team player', write: 'Mentored 4 junior engineers on clean architecture and participated in daily Agile sprint code reviews.'"
            })

        # Weak Point 6: Structural Gaps
        missing_sections = []
        for sec in ["experience", "projects", "skills", "education"]:
            if not sections.get(sec) or len(sections[sec]) < 20:
                missing_sections.append(sec.capitalize())

        if missing_sections:
            weak_points.append({
                "severity": "CRITICAL",
                "severity_label": "Missing Mandatory Section",
                "color": "#ef4444",
                "category": "Structural Integrity",
                "title": f"Missing Core Section ({', '.join(missing_sections)})",
                "issue": f"Could not detect a clear '{', '.join(missing_sections)}' section. ATS parsers categorize candidates by section headers.",
                "impact": "-15 Points ATS Loss",
                "how_to_fix": f"Add standard capitalized section headings: '{', '.join(missing_sections)}'. Avoid non-standard names.",
                "example": "Use standard headers: 'WORK EXPERIENCE', 'TECHNICAL SKILLS', 'EDUCATION', 'PROJECTS'."
            })

        # If no major weak points found
        if not weak_points:
            weak_points.append({
                "severity": "MINOR",
                "severity_label": "Polished",
                "color": "#10b981",
                "category": "Overall Quality",
                "title": "No Critical Structural Flaws Found!",
                "issue": "Your resume satisfies core formatting, metrics, and verb standards.",
                "impact": "Top 10% ATS Candidate",
                "how_to_fix": "Focus on customizing your skills to match specific target Job Descriptions for maximum interview callbacks.",
                "example": "Ensure 80%+ keyword alignment with each job posting."
            })

        return weak_points

    def _audit_missing_domain_skills(self, detected_skills: Dict[str, List[str]], text: str) -> List[Dict[str, Any]]:
        """Identifies expected industry-standard skills (2026 Standards) missing from candidate's profile."""
        missing = []

        # Determine primary domain
        has_frontend = "Web & Frontend" in detected_skills
        has_backend = "Backend & APIs" in detected_skills or "Programming Languages" in detected_skills
        has_ai = "AI & Data Science" in detected_skills

        selected_benchmark_key = "Full-Stack / Web"
        if has_ai and not has_frontend:
            selected_benchmark_key = "AI / Machine Learning"
        elif has_backend and not has_frontend:
            selected_benchmark_key = "Backend"

        benchmarks = self.domain_benchmarks.get(selected_benchmark_key, self.domain_benchmarks["Full-Stack / Web"])

        all_detected_lower = set()
        for cat, sk_list in detected_skills.items():
            for sk in sk_list:
                all_detected_lower.add(sk.lower())

        for skill_name, category, importance, reason in benchmarks:
            # Check if skill or related keyword is in text
            skill_tokens = skill_name.lower().replace("(", " ").replace(")", " ").replace("/", " ").split()
            found = any(token in text.lower() or token in all_detected_lower for token in skill_tokens if len(token) > 2)

            if not found:
                missing.append({
                    "skill": skill_name,
                    "category": category,
                    "importance": importance,
                    "reason": reason,
                    "suggested_placement": f"Add under '{category}' in Skills section or reference in your project bullet points."
                })

        return missing

    def _get_grade_info(self, score: int):
        if score >= 90:
            return "A+", "Top 5% - Interview Ready", "#10b981"
        elif score >= 80:
            return "A", "Competitive - Highly Ranked", "#3b82f6"
        elif score >= 70:
            return "B+", "Good Candidate - Minor Fixes", "#6366f1"
        elif score >= 60:
            return "B", "Average - Needs Optimization", "#f59e0b"
        elif score >= 50:
            return "C", "Below Average - High ATS Risk", "#f97316"
        else:
            return "D", "Needs Major Overhaul", "#ef4444"

    def _compile_recommendations(self, contact_f, struct_f, action_f, impact_f, skills_f, format_f, total_score):
        strengths = []
        improvements = []

        all_feedback = contact_f + struct_f + action_f + impact_f + skills_f + format_f
        for item in all_feedback:
            if any(pos in item.lower() for pos in ["excellent", "strong", "detected", "optimal", "good"]):
                strengths.append(item)
            else:
                improvements.append(item)

        if not strengths:
            strengths.append("Found clear structure and valid text encoding.")
        if not improvements:
            improvements.append("Resume is in top shape! Tailor keywords per specific job description.")

        return strengths[:4], improvements[:5]
