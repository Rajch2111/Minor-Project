"""
RAG Career Assistant (lite version)
Retriever: TF-IDF over alumni profiles + optional OpenAI answer generation
Falls back to a retrieved-context answer when no API key is set.
"""
import os

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

KNOWLEDGE = []


def _load_knowledge(data_path="data/alumni_data.csv"):
    global KNOWLEDGE
    alumni = pd.read_csv(data_path)
    KNOWLEDGE = [
        {
            "text": f"{row['name']} works as {row['role']} in {row['industry']} industry with skills: {row['skills']}. Experience: {row['experience_years']} years.",
            "name": row["name"],
        }
        for _, row in alumni.iterrows()
    ]
    return KNOWLEDGE


def retrieve(question: str, top_k: int = 3):
    knowledge = _load_knowledge()
    vectorizer = TfidfVectorizer()
    corpus = [k["text"] for k in knowledge]
    tfidf = vectorizer.fit_transform(corpus + [question])
    sims = cosine_similarity(tfidf[-1], tfidf[:-1])[0]
    top_idx = sims.argsort()[::-1][:top_k]
    return [knowledge[i]["text"] for i in top_idx]


def ask(question: str) -> dict:
    contexts = retrieve(question)

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            prompt = (
                "You are AlumniNet career assistant. Use ONLY this context to answer.\n\n"
                + "\n".join(contexts)
                + f"\n\nQuestion: {question}\nAnswer:"
            )
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )
            return {"answer": resp.choices[0].message.content, "sources": contexts}
        except Exception as e:
            return {"answer": f"(LLM error: {e}) Fallback: {contexts[0]}", "sources": contexts}

    # No API key -> retrieval-based fallback answer
    return {
        "answer": (
            f"Based on alumni data, most relevant matches for your query:\n"
            + "\n".join(f"- {c}" for c in contexts)
        ),
        "sources": contexts,
    }


if __name__ == "__main__":
    print(ask("Which alumni work as AI engineers?")["answer"])
