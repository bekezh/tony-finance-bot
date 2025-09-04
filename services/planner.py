import json
from typing import Any, Dict

def plan_from_ai_json(data: Dict[str, Any]) -> Dict[str, Any]:
    plan = data.get("plan") or {}
    # Ограничим длительность задач на всякий случай
    for w in plan.get("weeks", []):
        for d in w.get("days", []):
            dur = d.get("duration_min")
            if isinstance(dur, (int, float)) and dur > 60:
                d["duration_min"] = 60
    return plan

def habits_from_ai_json(data: Dict[str, Any]):
    habits = data.get("habits") or []
    norm = []
    for h in habits:
        norm.append({
            "title": h.get("title","Привычка"),
            "time": h.get("time","19:00"),
            "days": h.get("days", ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]),
            "description": h.get("description","")
        })
    return norm
