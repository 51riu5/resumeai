from fastapi import FastAPI

app = FastAPI(title="Resume Skill Intelligence API")

@app.get("/")
def root():
    return {"message": "API is running"}
