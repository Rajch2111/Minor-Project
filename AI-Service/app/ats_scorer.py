"""
ATS Compatibility Scorer
Evaluates resume text against sections + job description keywords
"""
import re

SECTION_POINTS = {
    "education": 15,
    "skills": 15,
    "experience": 15,
    "projects": 15,
    "certifications": 10,
}


def _keywords_from_job_description(jd: str):
    words = re.findall(r"[a-zA-Z+#.]+", jd.lower())
    stopwords = {"the", "and", "for", "with", "you", "will", "our", "are", "to", "of", "in", "a", "an", "on"}
    return {w for w in words if len(w) > 2 and w not in stopwords}


def ats_score(resume_text: str, job_description: str = "") -> dict:
    lowered = resume_text.lower()

    score = 0
    checks = {}

    # 1. Contact info
    has_email = bool(re.search(r"[\w\.-]+@[\w\.-]+\.\w+", resume_text))
    has_phone = bool(re.search(r"(\+?\d[\d\s-]{8,}\d)", resume_text))
    checks["email"] = has_email
    checks["phone"] = has_phone
    score += (10 if has_email else 0) + (5 if has_phone else 0)

    # 2. Sections
    missing_sections = []
    for section, points in SECTION_POINTS.items():
        found = section in lowered
        checks[section] = found
        if found:
            score += points
        else:
            missing_sections.append(section)

    # 3. Keyword match with job description
    keyword_score = 0
    matched_kw, missing_kw = [], []
    if job_description.strip():
        job_kws = _keywords_from_job_description(job_description)
        matched_kw = sorted([k for k in job_kws if k in lowered])
        missing_kw = sorted([k for k in job_kws if k not in lowered])
        keyword_score = round(len(matched_kw) / max(len(job_kws), 1) * 25, 1)
        score += keyword_score

    score = min(round(score, 1), 100)
    return {
        "ats_score": score,
        "checks": checks,
        "missing_sections": missing_sections,
        "matched_keywords": matched_kw[:20],
        "missing_keywords": missing_kw[:20],
        "suggestions": _suggestions(missing_sections, missing_kw),
    }


def _suggestions(missing_sections, missing_kw):
    tips = []
    if missing_sections:
        tips.append(f"Add missing sections: {', '.join(missing_sections)}")
    if missing_kw:
        tips.append(f"Include these job keywords: {', '.join(missing_kw[:8])}")
    if not tips:
        tips.append("Resume looks well-structured. Add measurable achievements to stand out.")
    return tips
