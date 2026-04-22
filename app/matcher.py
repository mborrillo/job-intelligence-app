def calculate_score(job, user):
    score = 0

    skills = user.skills.split(",")
    keywords = user.keywords.split(",")

    for s in skills:
        if s.lower() in job["description"].lower():
            score += 2

    for k in keywords:
        if k.lower() in job["description"].lower():
            score += 1

    if "remote" in job["description"].lower():
        score += 2

    return score
