"""
Skill Gap Analysis
Target role -> required skills vs student's current skills -> missing skills
"""

ROLE_SKILLS = {
    "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "NLP", "RAG", "PyTorch", "Docker"],
    "ML Engineer": ["Python", "Machine Learning", "Scikit-learn", "TensorFlow", "SQL", "Statistics"],
    "Data Scientist": ["Python", "Pandas", "Statistics", "Machine Learning", "SQL", "Data Visualization"],
    "Backend Developer": ["Node.js", "Express", "MongoDB", "SQL", "REST API", "Redis"],
    "Frontend Developer": ["React", "JavaScript", "HTML", "CSS", "Tailwind", "Redux"],
    "Full Stack Developer": ["React", "Node.js", "MongoDB", "Express", "REST API", "Docker"],
    "Cloud Engineer": ["AWS", "Docker", "Linux", "CI/CD", "Networking", "Python"],
    "DevOps Engineer": ["Docker", "Kubernetes", "CI/CD", "Linux", "AWS", "GitHub Actions"],
}


def analyze_skill_gap(target_role: str, student_skills: str):
    required = ROLE_SKILLS.get(target_role)
    if required is None:
        return {
            "error": f"Unknown role '{target_role}'",
            "available_roles": list(ROLE_SKILLS.keys()),
        }

    student_set = {s.strip().lower() for s in student_skills.split(",")}
    missing = [s for s in required if s.lower() not in student_set]
    matched = [s for s in required if s.lower() in student_set]
    coverage = round(len(matched) / len(required) * 100, 1)

    return {
        "target_role": target_role,
        "coverage_percent": coverage,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestion": (
            f"You have {coverage}% of the skills needed for {target_role}. "
            f"Focus on learning: {', '.join(missing) if missing else 'you are ready to apply!'}"
        ),
    }


if __name__ == "__main__":
    result = analyze_skill_gap("AI Engineer", "Python, Machine Learning")
    print(result)
