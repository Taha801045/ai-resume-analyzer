"""
Resume Parser Module: Extracts text, metadata, sections, and entities from PDF, DOCX, and TXT files.
"""
import io
import re
from typing import Dict, Any, List

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    import docx
except ImportError:
    docx = None


class ResumeParser:
    def __init__(self):
        # Section header patterns
        self.section_patterns = {
            "summary": re.compile(r"^(summary|professional summary|executive summary|about me|profile|objective)\b", re.IGNORECASE),
            "experience": re.compile(r"^(experience|work experience|employment history|work history|professional experience)\b", re.IGNORECASE),
            "education": re.compile(r"^(education|academic background|qualifications|academics)\b", re.IGNORECASE),
            "skills": re.compile(r"^(skills|technical skills|skills & expertise|core competencies|technologies)\b", re.IGNORECASE),
            "projects": re.compile(r"^(projects|key projects|personal projects|notable projects)\b", re.IGNORECASE),
            "certifications": re.compile(r"^(certifications|licenses|certifications & licenses|certificates)\b", re.IGNORECASE),
            "contact": re.compile(r"^(contact|contact information|personal info)\b", re.IGNORECASE),
        }

    def extract_text_from_bytes(self, file_bytes: bytes, filename: str) -> str:
        """Extract clean text from uploaded file bytes according to file type."""
        ext = filename.lower().split(".")[-1] if "." in filename else ""

        if ext == "pdf":
            return self._extract_pdf(file_bytes)
        elif ext in ["docx", "doc"]:
            return self._extract_docx(file_bytes)
        elif ext in ["txt", "md"]:
            try:
                return file_bytes.decode("utf-8")
            except UnicodeDecodeError:
                return file_bytes.decode("latin-1", errors="ignore")
        else:
            # Fallback to UTF-8
            return file_bytes.decode("utf-8", errors="ignore")

    def _extract_pdf(self, file_bytes: bytes) -> str:
        if not PdfReader:
            raise RuntimeError("pypdf is not installed. Run `pip install pypdf`.")
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            text_parts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            extracted = "\n".join(text_parts).strip()
            if not extracted or len(extracted) < 15:
                raise ValueError(
                    "No readable text could be extracted from this PDF. It appears to be a scanned image or protected document. "
                    "Please upload a text-based PDF or copy-paste your resume text directly into the text box."
                )
            return extracted
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")

    def _extract_docx(self, file_bytes: bytes) -> str:
        if not docx:
            raise RuntimeError("python-docx is not installed. Run `pip install python-docx`.")
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            text_parts = [para.text for para in doc.paragraphs if para.text.strip()]
            for table in doc.tables:
                for row in table.rows:
                    text_parts.extend([cell.text.strip() for cell in row.cells if cell.text.strip()])
            return "\n".join(text_parts).strip()
        except Exception as e:
            raise ValueError(f"Failed to extract text from DOCX: {str(e)}")

    def parse(self, text: str) -> Dict[str, Any]:
        """Perform full structural parse and entity extraction on resume text."""
        cleaned_text = self._clean_text(text)
        contact_info = self._extract_contact_info(cleaned_text)
        sections = self._extract_sections(cleaned_text)
        bullets = self._extract_bullet_points(cleaned_text)

        words = cleaned_text.split()
        word_count = len(words)
        char_count = len(cleaned_text)

        return {
            "raw_text": text,
            "cleaned_text": cleaned_text,
            "word_count": word_count,
            "char_count": char_count,
            "contact_info": contact_info,
            "sections": sections,
            "bullet_points": bullets,
        }

    def _clean_text(self, text: str) -> str:
        # Standardize line breaks and remove weird Unicode artifacts
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        # Replace non-breaking spaces
        text = text.replace("\xa0", " ")
        # Replace multiple spaces with single space, but keep newlines
        lines = [line.strip() for line in text.split("\n")]
        return "\n".join([line for line in lines if line])

    def _extract_contact_info(self, text: str) -> Dict[str, Any]:
        # Email
        email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
        email = email_match.group(0) if email_match else None

        # Phone (International and local patterns)
        phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
        phone = phone_match.group(0).strip() if phone_match else None

        # LinkedIn
        linkedin_match = re.search(r"(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+", text, re.IGNORECASE)
        linkedin = linkedin_match.group(0) if linkedin_match else None

        # GitHub
        github_match = re.search(r"(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+", text, re.IGNORECASE)
        github = github_match.group(0) if github_match else None

        # Portfolio / Personal Website
        portfolio_match = re.search(r"(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.(?:dev|me|io|com|app)(?:/[a-zA-Z0-9_-]+)?", text, re.IGNORECASE)
        portfolio = portfolio_match.group(0) if portfolio_match and not (portfolio_match.group(0) in [linkedin or "", github or ""]) else None

        # Candidate name heuristic: First non-empty line with 2-4 words, capitalized
        lines = text.split("\n")
        detected_name = "Candidate"
        for line in lines[:5]:
            words = line.strip().split()
            if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w and w[0].isalpha()):
                # Exclude common headers
                if not any(header in line.lower() for header in ["resume", "curriculum", "cv", "portfolio"]):
                    detected_name = line.strip()
                    break

        return {
            "name": detected_name,
            "email": email,
            "phone": phone,
            "linkedin": linkedin,
            "github": github,
            "portfolio": portfolio,
        }

    def _extract_sections(self, text: str) -> Dict[str, str]:
        lines = text.split("\n")
        sections = {
            "summary": "",
            "experience": "",
            "education": "",
            "skills": "",
            "projects": "",
            "certifications": "",
            "other": ""
        }

        current_section = "other"
        section_lines = {k: [] for k in sections.keys()}

        for line in lines:
            trimmed = line.strip()
            matched_section = None
            for sec_name, pattern in self.section_patterns.items():
                if pattern.search(trimmed):
                    matched_section = sec_name
                    break

            if matched_section and matched_section in section_lines:
                current_section = matched_section
            else:
                section_lines[current_section].append(line)

        for sec_name, s_lines in section_lines.items():
            sections[sec_name] = "\n".join(s_lines).strip()

        return sections

    def _extract_bullet_points(self, text: str) -> List[str]:
        bullets = []
        lines = text.split("\n")
        for line in lines:
            line_str = line.strip()
            # Bullet point symbols: •, -, *, ➢, ✔, etc.
            if re.match(r"^([•\-\*➢\u2022\u2023\u25E6\u2043\u2219]|(\d+\.))\s+", line_str):
                clean_bullet = re.sub(r"^([•\-\*➢\u2022\u2023\u25E6\u2043\u2219]|(\d+\.))\s+", "", line_str)
                if len(clean_bullet) > 15:  # meaningful length
                    bullets.append(clean_bullet)
        return bullets
