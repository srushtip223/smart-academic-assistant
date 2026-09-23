# 🎓 Smart Academic Assistant

> An intelligent task prioritization and study planning system powered by Google Gemini and a Rule-Based Inference Engine.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.39-FF4B4B?logo=streamlit)
![Gemini](https://img.shields.io/badge/Gemini-3.5%20Flash-4285F4?logo=google)

---

## 📌 Overview

**Smart Academic Assistant** is a full-stack AI application that helps students manage their academic workload intelligently. Users describe their tasks in natural language (e.g., *"DBMS exam next Tuesday, really tough"*), and the system:

1. **Extracts** structured data using Google Gemini (task name, subject, deadline, difficulty)
2. **Computes** a priority score using a Rule-Based Inference Engine
3. **Stores** the task in a database
4. **Generates** a 3-day personalized study schedule using Generative AI

This project demonstrates the integration of **Expert Systems**, **Natural Language Processing**, and **Generative AI** concepts from the Introduction to Intelligent Systems syllabus.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🗣️ **Natural Language Input** | Type tasks in plain English — no forms required |
| 🧠 **AI Task Extraction** | Gemini extracts task name, subject, deadline, difficulty |
| 📊 **Rule-Based Priority Engine** | Urgency (60%) + Difficulty (40%) → Priority Score |
| 🏷️ **Priority Labels** | Color-coded: 🔴 Critical, 🟠 High, 🟡 Medium, 🟢 Low |
| 📅 **AI Study Planner** | Generates a realistic 3-day study schedule |
| ⚡ **Quick-Add Presets** | One-click task templates for common scenarios |
| 📈 **Dashboard Metrics** | Total tasks, critical count, next deadline |
| 🗑️ **Full CRUD** | Create, Read, Delete tasks |
| 🎨 **Modern UI** | Dark gradient theme with glassmorphism cards |

---

## 🏗️ Architecture

```
┌─────────────────────┐        ┌──────────────────────┐        ┌─────────────────────┐
│  Streamlit Frontend │◄──────►│  FastAPI Backend     │◄──────►│  Google Gemini API  │
│  (Port 8501)        │  HTTP  │  (Port 8000)         │  SDK   │  (Cloud)            │
└─────────────────────┘        └──────────┬───────────┘        └─────────────────────┘
                                          │
                                          ▼
                               ┌──────────────────────┐
                               │  SQLite Database     │
                               │  (tasks.db)          │
                               └──────────────────────┘
```

### Data Flow

```
User input → Gemini extracts structured data → Rule-Based Engine computes priority
          → Task saved to SQLite → Sorted list returned to UI
```

---

## 🧠 Intelligent Systems Concepts Demonstrated

| Module | Concept | Implementation |
|---|---|---|
| **Module 2** | Intelligent Agents | The system perceives user input and acts on the environment |
| **Module 4** | Knowledge & Reasoning | Rule-Based Inference Engine computes priority |
| **Module 6** | Expert Systems | Combines symbolic rules with Generative AI |
| **Module 6** | Generative AI | Gemini extracts structured data from unstructured text |
| **Module 6** | NLP | Natural language processing of student tasks |

### 🧮 The Priority Formula

```
priority_score = (urgency_score × 0.6) + (difficulty × 0.4)
```

Where:
- **urgency_score** (0–10) is derived from hours remaining until the deadline
- **difficulty** (1–10) is estimated by Gemini

**Priority Label Mapping:**
- Score ≥ 8.5 → 🔴 Critical
- Score ≥ 6.5 → 🟠 High
- Score ≥ 4.0 → 🟡 Medium
- Score < 4.0 → 🟢 Low

---

## 🛠️ Tech Stack

**Backend**
- Python 3.13
- FastAPI 0.115
- SQLAlchemy 2.0
- SQLite
- Google Generative AI SDK
- Pydantic v2

**Frontend**
- Streamlit 1.39
- Requests
- Custom CSS (dark gradient theme)

**AI**
- Google Gemini 3.5 Flash Lite

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Google Gemini API key ([get one free](https://aistudio.google.com/apikey))

### 1. Clone the repository

```bash
git clone https://github.com/srushtip223/smart-academic-assistant.git
cd smart-academic-assistant
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate       # Windows
# source venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///./tasks.db
```

Run the backend:

```bash
uvicorn main:app --reload
```

Backend runs at **http://127.0.0.1:8000** — API docs at **/docs**.

### 3. Frontend setup

Open a **new terminal**:

```bash
cd frontend
python -m venv venv
.\venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

Run the frontend:

```bash
streamlit run app.py
```

Frontend opens at **http://localhost:8501**.

---

## 📁 Project Structure

```
smart-academic-assistant/
│
├── backend/
│   ├── main.py               # FastAPI app + routes
│   ├── ai_service.py         # Gemini integration
│   ├── priority_engine.py    # Rule-based inference engine
│   ├── database.py           # SQLAlchemy setup
│   ├── models.py             # Task ORM model
│   ├── schemas.py            # Pydantic schemas
│   └── requirements.txt
│
├── frontend/
│   ├── app.py                # Streamlit UI
│   └── requirements.txt
│
└── README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `GET` | `/tasks` | List all tasks sorted by priority |
| `POST` | `/tasks` | Create a task from natural language |
| `DELETE` | `/tasks/{id}` | Delete a task by ID |
| `GET` | `/schedule` | Generate a 3-day study schedule |

Full interactive docs at `http://127.0.0.1:8000/docs`.

### Example Request

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"text": "DBMS exam next Tuesday, really tough"}'
```

### Example Response

```json
{
  "id": 1,
  "task_name": "DBMS Exam",
  "subject": "DBMS",
  "deadline": "2026-09-29T23:59:00",
  "difficulty": 8,
  "urgency_score": 6.0,
  "priority_score": 6.8,
  "priority_label": "High",
  "created_at": "2026-09-23T18:53:00"
}
```

---

## 🔮 Future Enhancements

- 🔐 User authentication (multi-user support)
- 📅 Google Calendar integration
- 🔔 Email/SMS reminders for deadlines
- 📱 Mobile-responsive PWA
- 🔊 Voice input
- 📊 Analytics dashboard

---

## 📚 References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API](https://ai.google.dev/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/)

---

## 👨‍💻 Author

**Srushti P**
- Roll No: 14 *(update if different)*
- Course: TE Sem V — Introduction to Intelligent Systems
- College: TCET, University of Mumbai

---

## 📝 License

This project is developed for academic purposes as part of the Introduction to Intelligent Systems course.

---

⭐ **If you found this project helpful, give it a star!**