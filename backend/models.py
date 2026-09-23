from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    raw_input = Column(Text, nullable=False)          # original user sentence
    task_name = Column(String, nullable=False)
    subject = Column(String, nullable=True)
    deadline = Column(DateTime, nullable=False)        # ISO datetime
    difficulty = Column(Integer, nullable=False)        # 1-10

    urgency_score = Column(Float, nullable=False)
    priority_score = Column(Float, nullable=False)
    priority_label = Column(String, nullable=False)     # Critical/High/Medium/Low

    created_at = Column(DateTime, default=datetime.utcnow)