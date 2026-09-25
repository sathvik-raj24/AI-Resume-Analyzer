# =========================================================
# RESUME IMPROVEMENT RECOMMENDATIONS
# AI Resume Skill Extraction & Job Matching
# =========================================================


def generate_recommendations(
    missing_skills,
    keyword_score,
    structure_score,
    contact_score,
    ats_score,
    experience_score=0,
    detected_sections=None,
    bullet_analysis=None,
    missing_keywords=None
):
    """
    Generate detailed resume improvement recommendations.

    These recommendations are heuristic suggestions based on
    the analysis performed by this project.
    """

    recommendations = []

    detected_sections = detected_sections or {}

    bullet_analysis = bullet_analysis or {}

    missing_keywords = missing_keywords or []

    # =====================================================
    # MISSING SKILLS
    # =====================================================

    if missing_skills:

        skills_text = ", ".join(
            missing_skills[:8]
        )

        recommendations.append(
            f"Consider adding relevant skills such as "
            f"{skills_text} if you genuinely have experience "
            f"with them."
        )

    # =====================================================
    # KEYWORD GAP
    # =====================================================

    if keyword_score < 50:

        recommendations.append(
            "Your resume has low keyword alignment with "
            "the job description. Review the important "
            "job-specific terminology and include terms "
            "that accurately describe your actual experience."
        )

    elif keyword_score < 75:

        recommendations.append(
            "Your keyword alignment is moderate. Review "
            "the job description and make sure important "
            "technologies, responsibilities and domain terms "
            "are clearly represented where applicable."
        )

    if missing_keywords:

        important_keywords = ", ".join(
            missing_keywords[:10]
        )

        recommendations.append(
            f"Potential keyword gaps include: "
            f"{important_keywords}. Add them only when "
            f"they genuinely match your skills or experience."
        )

    # =====================================================
    # EXPERIENCE RELEVANCE
    # =====================================================

    if experience_score < 50:

        recommendations.append(
            "Your resume shows limited terminology overlap "
            "with the experience-related requirements of the "
            "job description. Highlight relevant projects, "
            "internships and responsibilities that directly "
            "relate to the target role."
        )

    elif experience_score < 75:

        recommendations.append(
            "Your experience relevance is moderate. Consider "
            "making your most relevant projects, internships "
            "and responsibilities more visible."
        )

    # =====================================================
    # RESUME SECTIONS
    # =====================================================

    if detected_sections:

        important_sections = {
            "Education",
            "Experience",
            "Skills",
            "Projects"
        }

        missing_sections = [
            section
            for section in important_sections
            if not detected_sections.get(section, False)
        ]

        if missing_sections:

            sections_text = ", ".join(
                missing_sections
            )

            recommendations.append(
                f"Consider adding or clearly labeling these "
                f"relevant resume sections: {sections_text}."
            )

    # =====================================================
    # BULLET ANALYSIS
    # =====================================================

    weak_bullets = bullet_analysis.get(
        "weak_bullets",
        0
    )

    strong_bullets = bullet_analysis.get(
        "strong_bullets",
        0
    )

    achievement_bullets = bullet_analysis.get(
        "achievement_bullets",
        0
    )

    weak_phrases = bullet_analysis.get(
        "weak_phrases",
        []
    )

    metrics_found = bullet_analysis.get(
        "metrics_found",
        []
    )

    if weak_bullets > 0:

        recommendations.append(
            f"{weak_bullets} resume bullet(s) contain "
            f"weak or generic phrases. Rewrite them using "
            f"specific actions, technologies and outcomes "
            f"that accurately reflect your work."
        )

    if weak_phrases:

        phrases_text = ", ".join(
            weak_phrases[:5]
        )

        recommendations.append(
            f"Generic phrases detected include: "
            f"{phrases_text}. Replace them with specific "
            f"descriptions of what you actually accomplished."
        )

    if strong_bullets == 0 and bullet_analysis.get(
        "total_bullets",
        0
    ) > 0:

        recommendations.append(
            "Your bullet points do not contain many detected "
            "action verbs. Consider beginning bullets with "
            "clear action verbs that accurately describe "
            "your contribution."
        )

    if achievement_bullets == 0 and bullet_analysis.get(
        "total_bullets",
        0
    ) > 0:

        recommendations.append(
            "No measurable results were detected in the "
            "analyzed bullet points. Where truthful and "
            "relevant, include measurable outcomes such as "
            "percentages, counts, time saved or performance "
            "improvements."
        )

    elif achievement_bullets > 0:

        recommendations.append(
            f"Your analysis detected measurable information "
            f"in {achievement_bullets} bullet(s). Continue "
            f"using specific metrics where they accurately "
            f"represent your achievements."
        )

    # =====================================================
    # RESUME STRUCTURE
    # =====================================================

    if structure_score < 60:

        recommendations.append(
            "Improve your resume structure by using clear "
            "sections such as Summary, Skills, Education, "
            "Experience, Projects and Certifications where "
            "applicable."
        )

    elif structure_score < 85:

        recommendations.append(
            "Your resume structure is reasonable, but review "
            "whether any relevant standard sections are "
            "missing or difficult to identify."
        )

    # =====================================================
    # CONTACT INFORMATION
    # =====================================================

    if contact_score < 50:

        recommendations.append(
            "Add complete professional contact information "
            "such as email, phone, LinkedIn and GitHub "
            "where applicable."
        )

    elif contact_score < 100:

        recommendations.append(
            "Consider adding missing professional contact "
            "links such as LinkedIn or GitHub."
        )

    # =====================================================
    # ATS SCORE
    # =====================================================

    if ats_score >= 80:

        recommendations.append(
            "The heuristic analysis shows strong overall "
            "alignment with this job. Continue keeping your "
            "experience specific, relevant and measurable."
        )

    elif ats_score >= 60:

        recommendations.append(
            "The heuristic analysis shows moderate alignment. "
            "Improving relevant skill alignment, keywords "
            "and evidence of experience may strengthen the "
            "resume's match with this job."
        )

    else:

        recommendations.append(
            "The heuristic analysis shows lower alignment "
            "with this job. Review the required skills and "
            "tailor the resume to highlight genuinely "
            "relevant experience."
        )

    # =====================================================
    # FINAL CLEANUP
    # =====================================================

    # Remove duplicate recommendations
    recommendations = list(
        dict.fromkeys(recommendations)
    )

    return recommendations