import os
import json
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)

# Use Gemini 1.5 Flash — fast and free tier available
model = genai.GenerativeModel(
    "gemini-3.5-flash-lite",
    generation_config={"temperature": 0.2, "max_output_tokens": 500},
)


EXTRACTION_PROMPT = """
You are an information extraction system for a student task manager.
Extract structured data from the user's natural language input.

Return ONLY a valid JSON object with these exact keys:
- "task_name": short title (string)
- "subject": the academic subject or category (string, or "General" if unclear)
- "deadline": ISO 8601 datetime string (YYYY-MM-DDTHH:MM:SS). If no time given, use 23:59:00. If no date given, use tomorrow's date.
- "difficulty": integer from 1 to 10 based on how challenging the task sounds (1=trivial, 10=extremely hard)

Today's date is {today}. Use it to resolve relative dates like "tomorrow", "next Tuesday", "in 3 days".

User input: "{user_input}"

Return ONLY the JSON. No markdown, no explanation, no code fences.
"""


def extract_task_from_text(user_input: str) -> dict:
    """
    Sends natural language input to Gemini and returns structured task data.
    """
    today = datetime.now().strftime("%Y-%m-%d (%A)")
    prompt = EXTRACTION_PROMPT.format(today=today, user_input=user_input)

    response = model.generate_content(prompt)
    raw = response.text.strip()

    # Strip markdown code fences if Gemini adds them
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"Gemini returned invalid JSON: {raw}")

    # Basic validation
    required = ["task_name", "subject", "deadline", "difficulty"]
    for key in required:
        if key not in data:
            raise ValueError(f"Missing key '{key}' in Gemini response: {data}")

    return data


SCHEDULE_PROMPT = """
You are a study planner. Based on the student's prioritized task list below,
generate a realistic 3-day study schedule.

Prioritized Tasks:
{tasks_json}

Return a plain-text, day-by-day schedule (Day 1, Day 2, Day 3) with specific
time blocks. Be realistic — humans need breaks. Keep it under 200 words.
"""


def generate_schedule(tasks: list) -> str:
    """
    Sends the prioritized tasks to Gemini and returns a study schedule.
    """
    simplified = [
        {
            "task": t.task_name,
            "subject": t.subject,
            "deadline": t.deadline.isoformat(),
            "priority": t.priority_label,
            "difficulty": t.difficulty,
        }
        for t in tasks
    ]
    prompt = SCHEDULE_PROMPT.format(tasks_json=json.dumps(simplified, indent=2))
    response = model.generate_content(prompt)
    return response.text.strip()