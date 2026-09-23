from datetime import datetime


def calculate_urgency(deadline: datetime) -> float:
    """
    Urgency is based on how many hours remain until the deadline.
    Returns a score from 0 to 10.
      - <= 6 hours  → 10 (critical)
      - <= 24 hours → 8
      - <= 3 days   → 6
      - <= 7 days   → 4
      - > 7 days    → 2
      - overdue     → 10 (max urgency)
    """
    now = datetime.now()
    hours_left = (deadline - now).total_seconds() / 3600

    if hours_left <= 0:
        return 10.0   # overdue
    elif hours_left <= 6:
        return 10.0
    elif hours_left <= 24:
        return 8.0
    elif hours_left <= 72:
        return 6.0
    elif hours_left <= 168:  # 7 days
        return 4.0
    else:
        return 2.0


def calculate_priority(urgency: float, difficulty: int) -> tuple:
    """
    Rule-based priority score.
    Formula:  priority = (urgency * 0.6) + (difficulty * 0.4)
    Both inputs are on a 0–10 scale, so score is also on 0–10.

    Returns: (priority_score, priority_label)
    """
    # Normalize difficulty from 1-10 to 0-10 scale (already is)
    priority_score = round((urgency * 0.6) + (difficulty * 0.4), 2)

    if priority_score >= 8.5:
        label = "Critical"
    elif priority_score >= 6.5:
        label = "High"
    elif priority_score >= 4.0:
        label = "Medium"
    else:
        label = "Low"

    return priority_score, label