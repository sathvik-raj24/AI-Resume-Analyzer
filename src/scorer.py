def calculate_keyword_score(resume_text, job_description):
    """
    Calculate how many important words from the job
    description appear in the resume.
    """

    resume_words = set(
        resume_text.lower().split()
    )

    job_words = set(
        job_description.lower().split()
    )

    # Remove very short words
    job_words = {
        word for word in job_words
        if len(word) >= 4
    }

    if not job_words:
        return 0

    matching_words = resume_words.intersection(
        job_words
    )

    score = (
        len(matching_words)
        / len(job_words)
    ) * 100

    return round(
        min(score, 100),
        2
    )


def calculate_structure_score(resume_text):
    """
    Estimate resume structure based on common sections.
    """

    text = resume_text.lower()

    sections = [
        "education",
        "experience",
        "skills",
        "projects",
        "certifications",
        "summary"
    ]

    found_sections = 0

    for section in sections:

        if section in text:
            found_sections += 1

    score = (
        found_sections
        / len(sections)
    ) * 100

    return round(
        score,
        2
    )


def calculate_contact_score(
    email,
    phone,
    linkedin,
    github
):
    """
    Calculate contact information completeness.
    """

    total = 4
    found = 0

    if email:
        found += 1

    if phone:
        found += 1

    if linkedin:
        found += 1

    if github:
        found += 1

    score = (
        found / total
    ) * 100

    return round(
        score,
        2
    )


def calculate_ats_score(
    skill_score,
    similarity_score,
    keyword_score,
    structure_score,
    contact_score
):
    """
    Calculate the final ATS score.
    """

    final_score = (

        (skill_score * 0.40)

        + (similarity_score * 0.30)

        + (keyword_score * 0.15)

        + (structure_score * 0.10)

        + (contact_score * 0.05)

    )

    return round(
        min(final_score, 100),
        2
    )