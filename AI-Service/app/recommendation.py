"""
Alumni-Student Recommendation Engine
TF-IDF Vectorization + Cosine Similarity
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_alumni(path="data/alumni_data.csv"):
    return pd.read_csv(path)


def build_profile_text(row):
    """Combine skills + role + industry into one text profile."""
    return f"{row['skills']} {row['role']} {row['industry']}"


def recommend_alumni(student_skills, top_n=5, data_path="data/alumni_data.csv"):
    alumni = load_alumni(data_path)
    alumni["profile_text"] = alumni.apply(build_profile_text, axis=1)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(alumni["profile_text"])

    student_vector = vectorizer.transform([student_skills])
    similarities = cosine_similarity(student_vector, tfidf_matrix)[0]

    alumni["score"] = similarities
    top = alumni.sort_values("score", ascending=False).head(top_n)

    return top[["alumni_id", "name", "role", "industry", "score"]]


if __name__ == "__main__":
    student = "Python Machine Learning NLP RAG"
    print(f"Student skills: {student}\n")
    results = recommend_alumni(student)
    for _, row in results.iterrows():
        print(f"{row['alumni_id']} - {row['name']} ({row['role']}) -> {row['score']*100:.1f}%")
