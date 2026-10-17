"""
Interview Question Generator: Generates realistic technical, system design,
and behavioral interview questions based on candidate's detected resume skills and projects.
"""
from typing import Dict, Any, List


class InterviewQuestionGenerator:
    def __init__(self):
        # Questions database mapped by technical domains
        self.domain_questions = {
            "Frontend": [
                {
                    "question": "Can you explain how React's virtual DOM reconciliation works, and how you optimize performance using useMemo, useCallback, or lazy loading?",
                    "category": "Technical Deep Dive",
                    "what_they_test": "Core rendering lifecycle knowledge, bundle optimization, and practical memory management.",
                    "star_guide": "Describe a real component you optimized, why it re-rendered needlessly, the tools you used (React DevTools Profiler), and the metric improvement."
                },
                {
                    "question": "How do you manage complex application state, and how do you decide between Context API, Redux/Zustand, or server-state solutions like React Query?",
                    "category": "System Architecture",
                    "what_they_test": "State normalization, caching strategy, and separation of client vs server state.",
                    "star_guide": "State the problem (prop drilling or cache invalidation), your choice of library, trade-offs evaluated, and the final architecture."
                }
            ],
            "Backend": [
                {
                    "question": "How would you design a rate limiter or caching strategy for high-concurrency microservice APIs to protect downstream databases?",
                    "category": "System Design",
                    "what_they_test": "Token bucket / Leaky bucket algorithms, Redis caching patterns, cache stampede prevention.",
                    "star_guide": "Clarify traffic scale, propose Redis with sliding window counters, explain fallback behaviors and error codes (HTTP 429)."
                },
                {
                    "question": "Describe an incident where an API endpoint degraded in production. How did you diagnose the bottleneck and resolve it?",
                    "category": "Problem Solving & Observability",
                    "what_they_test": "Logging, APM tracing, database query indexing, connection pools, and post-mortem execution.",
                    "star_guide": "Situation (slow API under load), Task (find root cause), Action (checked slow query logs, added index, tuned pool), Result (latency dropped)."
                }
            ],
            "Databases": [
                {
                    "question": "When scaling a database under heavy write loads, how do you decide between SQL horizontal sharding, read-replicas, and moving to a NoSQL store?",
                    "category": "Architecture & Data",
                    "what_they_test": "ACID compliance vs eventual consistency, CAP theorem trade-offs, indexing overhead.",
                    "star_guide": "Compare consistency needs, explain how read replicas offload queries, and when schema flexibility or horizontal write-scaling is mandatory."
                }
            ],
            "Cloud & DevOps": [
                {
                    "question": "How do you ensure zero-downtime deployments and configure safe automated rollbacks in your CI/CD pipelines?",
                    "category": "DevOps & Reliability",
                    "what_they_test": "Blue/Green or Canary deployments, health check probes, container orchestration.",
                    "star_guide": "Walk through pipeline steps (lint, unit test, build container, staging smoke test, blue-green swap, automated rollback if 5xx errors spike)."
                }
            ],
            "AI / ML & Data": [
                {
                    "question": "How do you mitigate hallucinations and optimize context window efficiency when designing an LLM / RAG pipeline?",
                    "category": "AI / ML Engineering",
                    "what_they_test": "Vector embeddings, chunking strategies, hybrid search (BM25 + cosine similarity), re-ranking.",
                    "star_guide": "Explain your chunk size experiments, metadata filtering, top-k retrieval, and prompt guardrails to maintain factual grounding."
                }
            ]
        }

        # Universal Behavioral Questions
        self.behavioral_questions = [
            {
                "question": "Tell me about a time you had a technical disagreement with a senior engineer or product manager. How did you resolve it?",
                "category": "Behavioral & Culture",
                "what_they_test": "Communication, humility, data-driven reasoning, and disagreement-and-commitment culture.",
                "star_guide": "Highlight that you focused on metrics, ran a quick prototype/benchmark rather than arguing opinions, and respected team consensus."
            },
            {
                "question": "Describe a project you owned where the requirements were ambiguous or changed midway through the sprint. How did you handle delivery?",
                "category": "Ownership & Adaptability",
                "what_they_test": "Proactive stakeholder communication, MVP scoping, agile adaptation under pressure.",
                "star_guide": "Explain how you broke the ambiguous request into testable milestones, aligned expectations early, and delivered incrementally."
            }
        ]

    def generate(self, detected_skills: Dict[str, List[str]], role_name: str = "Candidate") -> List[Dict[str, Any]]:
        """Selects the most relevant tailored interview questions based on candidate profile."""
        questions = []

        # Find questions matching detected skill domains
        for domain, q_list in self.domain_questions.items():
            if domain in detected_skills:
                # Add top question from this domain
                questions.append(q_list[0])
                if len(q_list) > 1 and len(questions) < 4:
                    questions.append(q_list[1])

        # If not enough domain questions, add default backend/frontend
        if len(questions) < 3:
            questions.extend(self.domain_questions["Backend"][:1])
            questions.extend(self.domain_questions["Frontend"][:1])

        # Always include high-yield behavioral questions
        questions.extend(self.behavioral_questions[:2])

        # Deduplicate and return top 5
        seen = set()
        final_list = []
        for q in questions:
            if q["question"] not in seen:
                seen.add(q["question"])
                final_list.append(q)
            if len(final_list) >= 5:
                break

        return final_list
