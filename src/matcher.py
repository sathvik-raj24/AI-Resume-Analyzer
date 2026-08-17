def flatten_skills(skills_dict):
    """
    Convert categorized skills into one set of skills.
    """

    all_skills = set()

    for skills in skills_dict.values():
        all_skills.update(skills)

    return all_skills


def calculate_skill_match(resume_skills, job_skills):
    """
    Compare resume skills with job-required skills.
    """

    resume_set = flatten_skills(resume_skills)
    job_set = flatten_skills(job_skills)

    # No skills in job description
    if not job_set:
        return {
            "score": 0,
            "matching": [],
            "missing": []
        }

    matching_skills = sorted(
        resume_set.intersection(job_set)
    )

    missing_skills = sorted(
        job_set - resume_set
    )

    score = (
        len(matching_skills)
        / len(job_set)
    ) * 100

    return {
        "score": round(score, 2),
        "matching": matching_skills,
        "missing": missing_skills
    }