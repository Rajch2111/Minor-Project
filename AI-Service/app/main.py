from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AlumniNet AI Service",
    description="AI/ML service for recommendation, ATS analysis and analytics",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "AlumniNet AI Service running"}


from app.recommendation import recommend_alumni
from app.skill_gap import analyze_skill_gap
from app.resume_parser import parse_resume, extract_text
from app.ats_scorer import ats_score
from app.analytics import compute_analytics
from app.rag import ask
from fastapi import UploadFile, File, Form


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ai-service"}


@app.get("/recommend")
def recommend(skills: str, top_n: int = 5):
    results = recommend_alumni(skills, top_n=top_n)
    return {
        "skills": skills,
        "recommendations": [
            {
                "alumni_id": row["alumni_id"],
                "name": row["name"],
                "role": row["role"],
                "industry": row["industry"],
                "score": round(float(row["score"]), 4),
            }
            for _, row in results.iterrows()
        ],
    }


@app.get("/skill-gap")
def skill_gap(target_role: str, skills: str):
    return analyze_skill_gap(target_role, skills)


@app.post("/parse-resume")
async def parse_resume_endpoint(file: UploadFile = File(...)):
    content = await file.read()
    try:
        parsed = parse_resume(file.filename, content)
        return {"success": True, "data": parsed}
    except ValueError as e:
        return {"success": False, "error": str(e)}


@app.post("/ats-score")
async def ats_score_endpoint(
    file: UploadFile = File(...),
    job_description: str = Form(default=""),
):
    content = await file.read()
    try:
        text = extract_text(file.filename, content)
        return {"success": True, "analysis": ats_score(text, job_description)}
    except ValueError as e:
        return {"success": False, "error": str(e)}


@app.get("/analytics")
def analytics():
    return compute_analytics()


@app.get("/chat")
def chat(question: str):
    return ask(question)
