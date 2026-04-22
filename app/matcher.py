from typing import Dict

from app import models

SKILL_WEIGHT = 3
KEYWORD_WEIGHT = 1
REMOTE_BONUS = 2
FREELANCE_BONUS = 2


def _safe_split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.lower().split(",") if item.strip()]


def calculate_score(job: Dict, user: models.User) -> int:
    """
    Calcula un score simple basado en:
    - skills del usuario presentes en la descripción
    - keywords del usuario presentes en la descripción
    - bonus por 'remote' y 'freelance'
    """
    score = 0

    description = job.get("description", "") or ""
    text = description.lower()

    skills = _safe_split_csv(user.skills)
    keywords = _safe_split_csv(user.keywords)

    for s in skills:
        if s and s in text:
            score += SKILL_WEIGHT

    for k in keywords:
        if k and k in text:
            score += KEYWORD_WEIGHT

    if "remote" in text:
        score += REMOTE_BONUS

    if "freelance" in text:
        score += FREELANCE_BONUS

    return score
