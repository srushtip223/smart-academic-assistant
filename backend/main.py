from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

from database import Base, engine, get_db
import models
import schemas
from priority_engine import calculate_urgency, calculate_priority
from ai_service import extract_task_from_text, generate_schedule

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Academic Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "Smart Academic Assistant API is running"}


@app.get("/tasks", response_model=list[schemas.TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).order_by(models.Task.priority_score.desc()).all()
    return tasks


@app.post("/tasks", response_model=schemas.TaskResponse)
def create_task(payload: schemas.TaskCreateRequest, db: Session = Depends(get_db)):
    try:
        extracted = extract_task_from_text(payload.text)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI extraction failed: {str(e)}")

    try:
        deadline = datetime.fromisoformat(extracted["deadline"])
    except Exception:
        raise HTTPException(status_code=422, detail=f"Invalid deadline from AI: {extracted['deadline']}")

    difficulty = int(extracted["difficulty"])
    urgency = calculate_urgency(deadline)
    priority_score, priority_label = calculate_priority(urgency, difficulty)

    task = models.Task(
        raw_input=payload.text,
        task_name=extracted["task_name"],
        subject=extracted.get("subject", "General"),
        deadline=deadline,
        difficulty=difficulty,
        urgency_score=urgency,
        priority_score=priority_score,
        priority_label=priority_label,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.get("/schedule", response_model=schemas.ScheduleResponse)
def get_schedule(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).order_by(models.Task.priority_score.desc()).limit(10).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found. Add some first.")

    try:
        schedule = generate_schedule(tasks)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Schedule generation failed: {str(e)}")

    return {"schedule": schedule}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"status": "deleted", "id": task_id}