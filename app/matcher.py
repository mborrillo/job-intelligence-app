def calculate_score(job, user):
    score = 0
    text = job["description"].lower()

    skills = [s.strip() for s in user.skills.lower().split(",")]
    keywords = [k.strip() for k in user.keywords.lower().split(",")]

    for s in skills:
        if s in text:
            score += 3  # subir peso

    for k in keywords:
        if k in text:
            score += 1

    if "remote" in text:
        score += 2

    if "freelance" in text:
        score += 2

    return score
