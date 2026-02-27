# run.py

from fastapi import FastAPI
from app.routes import complaints

app = FastAPI(title="ComplaintAI Hackathon Backend")

app.include_router(complaints.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("run:app", host="127.0.0.1", port=8000, reload=True)