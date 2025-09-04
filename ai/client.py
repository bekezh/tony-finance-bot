import json
from typing import List, Dict, Any, Optional
from config import OPENAI_API_KEY, MODEL_NAME
from ai.prompts import SYSTEM_PROMPT

# OpenAI SDK (v1+)
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

class AIClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or OPENAI_API_KEY
        self.model = model or MODEL_NAME
        self._client = OpenAI(api_key=self.api_key) if (OpenAI and self.api_key) else None

    async def generate(self, messages: List[Dict[str, str]], system: Optional[str] = None) -> Dict[str, Any]:
        """Return JSON per schema. If no API key, return a deterministic demo payload."""
        system_prompt = system or SYSTEM_PROMPT

        if not self._client:
            # Demo fallback
            return {
                "summary": "Демо: спокойный старт. Прогулки + вода + растяжка.",
                "plan": {
                    "weeks": [
                        {"days": [{"title": "Вечерняя прогулка", "duration_min": 25, "intensity": "низкая", "notes": "-"}]}
                    ]
                },
                "habits": [
                    {"title": "Прогулка 25 мин", "time": "19:30", "days": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]},
                    {"title": "Гидратация 6–8 стаканов", "time": "11:00", "days": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]}
                ],
                "terms": [{"term": "Функциональная растяжка", "explain": "Плавные движения, разогрев суставов перед активностью."}],
                "sources": [
                    {"title": "WHO Physical Activity Guidelines", "url": "https://www.who.int/", "year": 2020},
                    {"title": "Harvard Health: Walking for health", "url": "https://www.health.harvard.edu/", "year": 2024}
                ],
                "confidence": "medium"
            }

        resp = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                *messages
            ],
            temperature=0.3,
        )
        content = resp.choices[0].message.content
        # Try parse JSON
        try:
            data = json.loads(content)
        except Exception:
            data = {"summary": content, "plan": {"weeks": []}, "habits": [], "terms": [], "sources": [], "confidence": "low"}
        return data

client_singleton = AIClient()
