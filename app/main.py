from fastapi import FastAPI, UploadFile, File, Form, Body
import pdfplumber
from app.skill_extractor import extract_skills
from app.matcher import match_skills




app = FastAPI(title="Resume Skill Intelligence API")


@app.get("/")
def root():
    return {"message": "API is running"}


@app.post("/analyze-resume/")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    # 1. Validate file
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported"}

    # 2. Extract resume text
    resume_text = ""

    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            resume_text += page.extract_text() or ""

    # 3. Extract skills
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    # 4. Match skills
    analysis = match_skills(resume_skills, job_skills)

    # 5. Return combined result
    return {
        "filename": file.filename,
        "resume_skills": resume_skills,
        "job_required_skills": job_skills,
        "analysis": analysis
    }
