def generate_recommendations(
    missing_skills,
    keyword_score,
    structure_score,
    contact_score,
    ats_score
):
    """
    Generate resume improvement recommendations.
    """

    recommendations = []


    # ======================================
    # MISSING SKILLS
    # ======================================

    if missing_skills:

        skills_text = ", ".join(
            missing_skills[:8]
        )

        recommendations.append(
            f"Consider adding relevant skills such as "
            f"{skills_text} if you genuinely have experience "
            f"with them."
        )


    # ======================================
    # KEYWORD SCORE
    # ======================================

    if keyword_score < 50:

        recommendations.append(
            "Your resume has relatively low keyword "
            "overlap with the job description. Consider "
            "using relevant terminology from the job "
            "description where it accurately describes "
            "your experience."
        )

    elif keyword_score < 75:

        recommendations.append(
            "Your keyword alignment is moderate. "
            "Review the job description and make sure "
            "important relevant technologies and "
            "responsibilities are clearly mentioned."
        )


    # ======================================
    # RESUME STRUCTURE
    # ======================================

    if structure_score < 60:

        recommendations.append(
            "Improve your resume structure by including "
            "clear sections such as Summary, Skills, "
            "Education, Experience, Projects and "
            "Certifications where applicable."
        )

    elif structure_score < 85:

        recommendations.append(
            "Your resume structure is reasonable, but "
            "consider adding any missing standard sections "
            "that are relevant to your background."
        )


    # ======================================
    # CONTACT INFORMATION
    # ======================================

    if contact_score < 50:

        recommendations.append(
            "Add complete professional contact information "
            "such as email, phone, LinkedIn and GitHub "
            "where applicable."
        )

    elif contact_score < 100:

        recommendations.append(
            "Consider adding any missing professional "
            "contact links such as LinkedIn or GitHub."
        )


    # ======================================
    # ATS SCORE
    # ======================================

    if ats_score >= 80:

        recommendations.append(
            "Your resume has a strong overall alignment "
            "with this job. Focus on keeping your experience "
            "specific and measurable."
        )

    elif ats_score >= 60:

        recommendations.append(
            "Your resume has a moderate match. Improving "
            "skill alignment and using relevant job-specific "
            "keywords could strengthen your application."
        )

    else:

        recommendations.append(
            "Your resume currently has a low match for "
            "this job. Review the required skills and "
            "tailor your resume to highlight genuinely "
            "relevant experience."
        )


    return recommendations