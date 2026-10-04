# AI-Service — Testing & Endpoints

Base URL: `http://localhost:8000`  |  Interactive docs: `/docs`

## Endpoint Test Checklist

| # | Endpoint | Method | Test Input | Expected |
|---|----------|--------|------------|----------|
| 1 | `/` | GET | — | service running message |
| 2 | `/health` | GET | — | `{"status":"ok"}` |
| 3 | `/recommend` | GET | `skills=Python ML NLP&top_n=5` | top-5 alumni + scores |
| 4 | `/skill-gap` | GET | `target_role=AI Engineer&skills=Python, ML` | missing skills list |
| 5 | `/parse-resume` | POST | upload PDF/DOCX | extracted skills/email/sections |
| 6 | `/ats-score` | POST | upload PDF + job description | score + suggestions |
| 7 | `/analytics` | GET | — | totals, distributions |
| 8 | `/chat` | GET | `question=Which alumni work as AI engineers?` | RAG answer |

## Node.js Integration Checklist (Backend on :5000)

| Endpoint | Via |
|----------|-----|
| `GET /api/ai/recommend?skills=...` | requires Bearer token |
| `GET /api/ai/skill-gap?target_role=...&skills=...` | requires Bearer token |
| `GET /api/ai/analytics` | requires Bearer token |

## Sample Viva Points (your contributions)

- Recommendation engine: TF-IDF vectorization + cosine similarity over combined alumni profiles (skills + role + industry)
- Weighted skill-gap scoring against role skill matrix
- Resume parsing pipeline: PDF/DOCX → text extraction → regex + keyword extraction
- ATS scoring: section checks + job-description keyword match percentage
- RAG: TF-IDF retriever over alumni profiles, optional LLM generation with fallback
- Analytics: Pandas aggregations for dashboard charts
