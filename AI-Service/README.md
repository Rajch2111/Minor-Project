# AlumniNet AI Service

Python + FastAPI microservice handling:
- Alumni–Student Recommendation
- Resume Parsing + ATS Scoring
- Skill Gap Analysis
- Analytics

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Endpoints
- `GET /` — service info
- `GET /health` — health check
- API docs: http://localhost:8000/docs
