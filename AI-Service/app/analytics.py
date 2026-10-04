"""
Alumni Analytics — statistics for the dashboard
"""
from collections import Counter

import pandas as pd


def compute_analytics(data_path="data/alumni_data.csv") -> dict:
    alumni = pd.read_csv(data_path)

    all_skills = []
    for skills in alumni["skills"]:
        all_skills.extend([s.strip() for s in skills.split(",")])

    return {
        "total_alumni": int(len(alumni)),
        "avg_experience_years": round(float(alumni["experience_years"].mean()), 1),
        "role_distribution": dict(Counter(alumni["role"])),
        "industry_distribution": dict(Counter(alumni["industry"])),
        "top_skills": dict(Counter(all_skills).most_common(10)),
        "experience_buckets": {
            "0-2 years": int((alumni["experience_years"] <= 2).sum()),
            "3-4 years": int(((alumni["experience_years"] >= 3) & (alumni["experience_years"] <= 4)).sum()),
            "5+ years": int((alumni["experience_years"] >= 5).sum()),
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(compute_analytics(), indent=2))
