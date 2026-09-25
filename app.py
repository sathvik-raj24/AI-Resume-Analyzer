import streamlit as st
from pathlib import Path

from src.pdf_parser import extract_text_from_pdf
from src.text_processor import (
    extract_email,
    extract_phone,
    extract_linkedin,
    extract_github,
)
from src.skill_extractor import extract_skills
from src.matcher import calculate_skill_match
from src.nlp_similarity import calculate_text_similarity

from src.scorer import (
    calculate_keyword_score,
    calculate_structure_score,
    calculate_contact_score,
    calculate_ats_score,
    calculate_keyword_gap,
    calculate_experience_relevance,
    calculate_ats_checks,
    detect_resume_sections,
    analyze_resume_bullets,
)

from src.recommendations import generate_recommendations
from src.report_generator import create_analysis_report


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ResumeAI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# LOAD CSS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
CSS_FILE = BASE_DIR / "assets" / "styless.css"

if CSS_FILE.exists():
    st.markdown(
        f"<style>{CSS_FILE.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "analysis_done": False,
    "resume_text": "",
    "job_description": "",
    "email": "",
    "phone": "",
    "linkedin": "",
    "github": "",
    "resume_skills": {},
    "job_skills": {},
    "matching_skills": [],
    "missing_skills": [],
    "skill_score": 0,
    "similarity_score": 0,
    "keyword_score": 0,
    "keyword_gap": {},
    "experience_score": 0,
    "structure_score": 0,
    "contact_score": 0,
    "ats_score": 0,
    "ats_checks": {},
    "sections": {},
    "bullet_analysis": {},
    "recommendations": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.title("✦ ResumeAI")
    st.caption("AI RESUME INTELLIGENCE")

    st.success("● Analysis Engine Online")

    st.divider()

    st.subheader("Workspace")

    st.write("01  Resume Analysis")
    st.write("02  Skill Intelligence")
    st.write("03  Job Matching")
    st.write("04  ATS Evaluation")
    st.write("05  Recommendations")

    st.divider()

    st.subheader("System Modules")

    st.write("✓ PDF Resume Parsing")
    st.write("✓ NLP Similarity")
    st.write("✓ Skill Intelligence")
    st.write("✓ Keyword Analysis")
    st.write("✓ ATS Evaluation")
    st.write("✓ Resume Recommendations")
    st.write("✓ PDF Report Generation")

    st.divider()

    st.caption("ResumeAI v1.0")
    st.caption("Python • NLP • Streamlit")


# =========================================================
# HERO
# =========================================================

st.title("Understand your resume.")
st.header("Improve your match.")

st.write(
    "Context-aware resume analysis using NLP, skill intelligence, "
    "keyword analysis and heuristic ATS evaluation."
)

st.info(
    "✦ PDF Parsing   •   NLP   •   Skill Matching   •   ATS Analysis"
)


# =========================================================
# INPUT SECTION
# =========================================================

st.divider()

st.subheader("Resume Analysis")

left, right = st.columns(2)

with left:
    st.markdown("### 01 — Resume Document")

    uploaded_file = st.file_uploader(
        "Upload your resume PDF",
        type=["pdf"],
        help="Upload a text-based PDF resume.",
    )

with right:
    st.markdown("### 02 — Target Job")

    job_description = st.text_area(
        "Paste the job description",
        height=220,
        placeholder=(
            "Paste the complete job description here..."
        ),
    )


# =========================================================
# ANALYZE
# =========================================================

st.write("")

analyze = st.button(
    "✦  ANALYZE RESUME",
    type="primary",
    use_container_width=True,
)


if analyze:

    if uploaded_file is None:
        st.error("Please upload a PDF resume.")
        st.stop()

    if not job_description.strip():
        st.error("Please enter a job description.")
        st.stop()

    with st.spinner("Analyzing your resume..."):

        # -------------------------------------------------
        # PDF TEXT
        # -------------------------------------------------

        try:
            resume_text = extract_text_from_pdf(
                uploaded_file
            )
        except Exception as error:
            st.error(
                f"Could not read the PDF: {error}"
            )
            st.stop()

        if not resume_text or not resume_text.strip():
            st.error(
                "No readable text could be extracted from this PDF."
            )
            st.stop()


        # -------------------------------------------------
        # CONTACT INFORMATION
        # -------------------------------------------------

        email = extract_email(resume_text)
        phone = extract_phone(resume_text)
        linkedin = extract_linkedin(resume_text)
        github = extract_github(resume_text)


        # -------------------------------------------------
        # SKILLS
        # -------------------------------------------------

        resume_skills = extract_skills(
            resume_text
        )

        job_skills = extract_skills(
            job_description
        )


        # -------------------------------------------------
        # SMART SKILL MATCH
        # -------------------------------------------------

        match_result = calculate_skill_match(
            resume_skills,
            job_skills,
        )

        skill_score = match_result.get(
            "score",
            0,
        )

        matching_skills = match_result.get(
            "matching",
            [],
        )

        missing_skills = match_result.get(
            "missing",
            [],
        )


        # -------------------------------------------------
        # NLP SIMILARITY
        # -------------------------------------------------

        try:
            similarity_score = calculate_text_similarity(
                resume_text,
                job_description,
            )
        except Exception:
            similarity_score = 0


        # -------------------------------------------------
        # BASIC ATS COMPONENTS
        # -------------------------------------------------

        keyword_score = calculate_keyword_score(
            resume_text,
            job_description,
        )

        structure_score = calculate_structure_score(
            resume_text,
        )

        contact_score = calculate_contact_score(
            email,
            phone,
            linkedin,
            github,
        )


        # -------------------------------------------------
        # HEURISTIC ATS SCORE
        # -------------------------------------------------

        ats_score = calculate_ats_score(
            skill_score,
            similarity_score,
            keyword_score,
            structure_score,
            contact_score,
        )


        # -------------------------------------------------
        # KEYWORD GAP
        # -------------------------------------------------

        keyword_gap = calculate_keyword_gap(
            resume_text,
            job_description,
        )

        missing_keywords = keyword_gap.get(
            "missing_keywords",
            [],
        )

        matched_keywords = keyword_gap.get(
            "matched_keywords",
            [],
        )


        # -------------------------------------------------
        # EXPERIENCE RELEVANCE
        # -------------------------------------------------

        experience_score = calculate_experience_relevance(
            resume_text,
            job_description,
        )


        # -------------------------------------------------
        # RESUME SECTIONS
        # -------------------------------------------------

        sections = detect_resume_sections(
            resume_text
        )


        # -------------------------------------------------
        # BULLET ANALYSIS
        # -------------------------------------------------

        bullet_analysis = analyze_resume_bullets(
            resume_text
        )


        # -------------------------------------------------
        # ATS CHECKS
        # -------------------------------------------------

        ats_checks = calculate_ats_checks(
            resume_text,
            email=email,
            phone=phone,
            linkedin=linkedin,
            github=github,
        )


        # -------------------------------------------------
        # RECOMMENDATIONS
        # -------------------------------------------------

        recommendations = generate_recommendations(
            missing_skills,
            keyword_score,
            structure_score,
            contact_score,
            ats_score,
            experience_score=experience_score,
            detected_sections=sections,
            bullet_analysis=bullet_analysis,
            missing_keywords=missing_keywords,
        )


        # -------------------------------------------------
        # SAVE RESULTS
        # -------------------------------------------------

        st.session_state.analysis_done = True

        st.session_state.resume_text = resume_text
        st.session_state.job_description = job_description

        st.session_state.email = email
        st.session_state.phone = phone
        st.session_state.linkedin = linkedin
        st.session_state.github = github

        st.session_state.resume_skills = resume_skills
        st.session_state.job_skills = job_skills

        st.session_state.matching_skills = matching_skills
        st.session_state.missing_skills = missing_skills

        st.session_state.skill_score = skill_score
        st.session_state.similarity_score = similarity_score
        st.session_state.keyword_score = keyword_score
        st.session_state.keyword_gap = keyword_gap
        st.session_state.experience_score = experience_score
        st.session_state.structure_score = structure_score
        st.session_state.contact_score = contact_score
        st.session_state.ats_score = ats_score

        st.session_state.ats_checks = ats_checks
        st.session_state.sections = sections
        st.session_state.bullet_analysis = bullet_analysis
        st.session_state.recommendations = recommendations

    st.success("✓ Resume analysis completed!")


# =========================================================
# RESULTS
# =========================================================

if st.session_state.analysis_done:

    resume_text = st.session_state.resume_text

    email = st.session_state.email
    phone = st.session_state.phone
    linkedin = st.session_state.linkedin
    github = st.session_state.github

    matching_skills = st.session_state.matching_skills
    missing_skills = st.session_state.missing_skills

    skill_score = st.session_state.skill_score
    similarity_score = st.session_state.similarity_score
    keyword_score = st.session_state.keyword_score
    keyword_gap = st.session_state.keyword_gap
    experience_score = st.session_state.experience_score
    structure_score = st.session_state.structure_score
    contact_score = st.session_state.contact_score
    ats_score = st.session_state.ats_score

    ats_checks = st.session_state.ats_checks
    sections = st.session_state.sections
    bullet_analysis = st.session_state.bullet_analysis
    recommendations = st.session_state.recommendations


    # =====================================================
    # OVERVIEW
    # =====================================================

    st.divider()
    st.header("Analysis Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "ATS SCORE",
            f"{ats_score:.0f}%",
        )

    with c2:
        st.metric(
            "SKILL MATCH",
            f"{skill_score:.0f}%",
        )

    with c3:
        st.metric(
            "KEYWORD MATCH",
            f"{keyword_score:.0f}%",
        )

    with c4:
        st.metric(
            "EXPERIENCE",
            f"{experience_score:.0f}%",
        )


    st.warning(
        "ATS score shown here is a project-specific heuristic estimate. "
        "It is not the score produced by a real employer ATS."
    )


    # =====================================================
    # TABS
    # =====================================================

    (
        overview_tab,
        skills_tab,
        keywords_tab,
        ats_tab,
        bullets_tab,
        recommendations_tab,
        cover_tab,
        report_tab,
    ) = st.tabs(
        [
            "Overview",
            "Skills",
            "Keywords",
            "ATS Checks",
            "Bullet Analysis",
            "Recommendations",
            "Cover Letter",
            "PDF Report",
        ]
    )


    # =====================================================
    # OVERVIEW TAB
    # =====================================================

    with overview_tab:

        st.subheader("Score Breakdown")

        a, b = st.columns(2)

        with a:
            st.write("Skill Match")
            st.progress(
                min(float(skill_score) / 100, 1.0)
            )

            st.write(f"{skill_score:.1f}%")

            st.write("NLP Similarity")
            st.progress(
                min(float(similarity_score) / 100, 1.0)
            )

            st.write(f"{similarity_score:.1f}%")

            st.write("Keyword Match")
            st.progress(
                min(float(keyword_score) / 100, 1.0)
            )

            st.write(f"{keyword_score:.1f}%")

        with b:
            st.write("Resume Structure")
            st.progress(
                min(float(structure_score) / 100, 1.0)
            )

            st.write(f"{structure_score:.1f}%")

            st.write("Contact Information")
            st.progress(
                min(float(contact_score) / 100, 1.0)
            )

            st.write(f"{contact_score:.1f}%")

            st.write("Experience Relevance")
            st.progress(
                min(float(experience_score) / 100, 1.0)
            )

            st.write(f"{experience_score:.1f}%")


        st.subheader("Contact Information")

        contacts = {
            "Email": email,
            "Phone": phone,
            "LinkedIn": linkedin,
            "GitHub": github,
        }

        for name, value in contacts.items():

            if value:
                st.success(
                    f"✓ {name}: {value}"
                )
            else:
                st.warning(
                    f"○ {name}: Not detected"
                )


    # =====================================================
    # SKILLS TAB
    # =====================================================

    with skills_tab:

        left, right = st.columns(2)

        with left:

            st.subheader(
                f"✓ Matching Skills ({len(matching_skills)})"
            )

            if matching_skills:
                for skill in matching_skills:
                    st.success(skill)
            else:
                st.info("No matching skills detected.")

        with right:

            st.subheader(
                f"Missing Skills ({len(missing_skills)})"
            )

            if missing_skills:
                for skill in missing_skills:
                    st.warning(skill)
            else:
                st.success(
                    "No missing job-specific skills detected."
                )


    # =====================================================
    # KEYWORDS TAB
    # =====================================================

    with keywords_tab:

        st.subheader("Keyword Gap Analysis")

        matched_keywords = keyword_gap.get(
            "matched_keywords",
            [],
        )

        missing_keywords = keyword_gap.get(
            "missing_keywords",
            [],
        )

        st.metric(
            "Keyword Score",
            f"{keyword_gap.get('score', keyword_score):.1f}%",
        )

        a, b = st.columns(2)

        with a:

            st.markdown(
                f"### ✓ Matched ({len(matched_keywords)})"
            )

            if matched_keywords:
                st.write(
                    ", ".join(matched_keywords)
                )
            else:
                st.info("No matched keywords.")

        with b:

            st.markdown(
                f"### + Missing ({len(missing_keywords)})"
            )

            if missing_keywords:
                st.write(
                    ", ".join(missing_keywords)
                )
            else:
                st.success(
                    "No keyword gaps detected."
                )


    # =====================================================
    # ATS CHECKS TAB
    # =====================================================

    with ats_tab:

        st.subheader("ATS Compatibility Checks")

        labels = {
            "contact_information": "Contact information",
            "linkedin_present": "LinkedIn profile",
            "github_present": "GitHub profile",
            "education_present": "Education section",
            "experience_present": "Experience section",
            "skills_present": "Skills section",
            "projects_present": "Projects section",
            "certifications_present": "Certifications section",
            "reasonable_length": "Reasonable resume length",
        }

        for key, label in labels.items():

            if ats_checks.get(key, False):
                st.success(
                    f"✓ {label}"
                )
            else:
                st.warning(
                    f"○ {label}"
                )


        st.subheader("Detected Resume Sections")

        section_cols = st.columns(4)

        for index, (section, found) in enumerate(
            sections.items()
        ):

            with section_cols[index % 4]:

                if found:
                    st.success(
                        f"✓ {section}"
                    )
                else:
                    st.error(
                        f"○ {section}"
                    )


    # =====================================================
    # BULLET ANALYSIS
    # =====================================================

    with bullets_tab:

        st.subheader(
            "Resume Bullet-Point Analyzer"
        )

        b1, b2, b3, b4 = st.columns(4)

        with b1:
            st.metric(
                "Total Bullets",
                bullet_analysis.get(
                    "total_bullets",
                    0,
                ),
            )

        with b2:
            st.metric(
                "Strong Bullets",
                bullet_analysis.get(
                    "strong_bullets",
                    0,
                ),
            )

        with b3:
            st.metric(
                "Weak Bullets",
                bullet_analysis.get(
                    "weak_bullets",
                    0,
                ),
            )

        with b4:
            st.metric(
                "Achievement Bullets",
                bullet_analysis.get(
                    "achievement_bullets",
                    0,
                ),
            )


        weak_examples = bullet_analysis.get(
            "weak_examples",
            [],
        )

        weak_phrases = bullet_analysis.get(
            "weak_phrases",
            [],
        )

        metric_examples = bullet_analysis.get(
            "metric_examples",
            [],
        )

        metrics_found = bullet_analysis.get(
            "metrics_found",
            [],
        )


        if weak_examples:

            st.subheader(
                "Weak Bullet Examples"
            )

            for item in weak_examples:
                st.warning(item)


        if weak_phrases:

            st.subheader(
                "Weak Phrases Detected"
            )

            st.write(
                ", ".join(weak_phrases)
            )


        if metric_examples:

            st.subheader(
                "Achievement / Metric Bullets"
            )

            for item in metric_examples:
                st.success(item)


        if metrics_found:

            st.subheader(
                "Detected Metrics"
            )

            st.write(
                ", ".join(metrics_found)
            )


    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    with recommendations_tab:

        st.subheader(
            "Resume Improvement Recommendations"
        )

        if recommendations:

            for index, recommendation in enumerate(
                recommendations,
                start=1,
            ):

                st.info(
                    f"**{index}.** {recommendation}"
                )

        else:

            st.success(
                "No major recommendations detected."
            )


    # =====================================================
    # COVER LETTER
    # =====================================================

    with cover_tab:

        st.subheader(
            "✦ AI Cover-Letter Generator"
        )

        st.write(
            "Generate a tailored draft using your resume "
            "and the target job description."
        )

        name = st.text_input(
            "Your Name",
            placeholder="Enter your name",
        )

        company = st.text_input(
            "Company Name",
            placeholder="Enter company name",
        )

        role = st.text_input(
            "Target Role",
            placeholder="e.g. Machine Learning Intern",
        )

        generate_letter = st.button(
            "Generate Cover Letter",
            type="primary",
            use_container_width=True,
        )

        if generate_letter:

            display_name = name.strip() or "Your Name"
            display_company = (
                company.strip()
                or "the company"
            )
            display_role = (
                role.strip()
                or "the position"
            )

            matched_text = ", ".join(
                matching_skills[:8]
            )

            if not matched_text:
                matched_text = (
                    "relevant technical and analytical skills"
                )

            missing_text = ", ".join(
                missing_skills[:5]
            )

            if not missing_text:
                missing_text = (
                    "the requirements of the role"
                )

            cover_letter = f"""Dear Hiring Manager,

I am writing to express my interest in the {display_role} opportunity at {display_company}.

My background includes experience with {matched_text}. My resume also demonstrates technical projects and practical work that align with several of the requirements described in the position.

I am particularly interested in this opportunity because it would allow me to apply my technical knowledge, problem-solving abilities, and willingness to learn in a professional environment.

Based on the job description, I am especially interested in contributing to work involving the technologies, responsibilities, and objectives associated with this role. I am also continuing to strengthen areas related to {missing_text} where applicable.

I would appreciate the opportunity to discuss how my background, projects, and technical skills could contribute to your team.

Thank you for your time and consideration.

Sincerely,
{display_name}
"""

            st.text_area(
                "Generated Cover Letter",
                value=cover_letter,
                height=500,
            )

            st.download_button(
                "↓ Download Cover Letter",
                data=cover_letter,
                file_name="AI_Cover_Letter.txt",
                mime="text/plain",
                use_container_width=True,
            )


    # =====================================================
    # PDF REPORT
    # =====================================================

    with report_tab:

        st.subheader(
            "Analysis Report"
        )

        st.write(
            "Download the complete resume analysis as a PDF."
        )

        try:

            report_file = create_analysis_report(
                ats_score,
                skill_score,
                similarity_score,
                keyword_score,
                structure_score,
                contact_score,
                matching_skills,
                missing_skills,
                recommendations,
                email,
                phone,
                linkedin,
                github,
            )

            if hasattr(
                report_file,
                "getvalue",
            ):
                report_data = report_file.getvalue()
            else:
                report_data = report_file

            st.download_button(
                "↓ DOWNLOAD PDF REPORT",
                data=report_data,
                file_name="AI_Resume_Analysis_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        except Exception as error:

            st.error(
                f"Could not generate PDF report: {error}"
            )


    # =====================================================
    # EXTRACTED TEXT
    # =====================================================

    with st.expander(
        "View Extracted Resume Text"
    ):

        st.text_area(
            "Extracted Text",
            resume_text,
            height=500,
            label_visibility="collapsed",
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "ResumeAI • AI Resume Intelligence • "
    "Python + NLP + Streamlit"
)