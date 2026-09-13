import streamlit as st
from pathlib import Path

from src.pdf_parser import extract_text_from_pdf

from src.text_processor import (
    extract_email,
    extract_phone,
    extract_linkedin,
    extract_github
)

from src.skill_extractor import extract_skills

from src.matcher import calculate_skill_match

from src.nlp_similarity import calculate_text_similarity

from src.scorer import (
    calculate_keyword_score,
    calculate_structure_score,
    calculate_contact_score,
    calculate_ats_score
)

from src.recommendations import (
    generate_recommendations
)

from src.report_generator import (
    create_analysis_report
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# LOAD CSS
# ==========================================

css_file = Path(
    "assets/styless.css"
)

if css_file.exists():

    with open(
        css_file,
        "r",
        encoding="utf-8"
    ) as file:

        st.markdown(
            f"<style>{file.read()}</style>",
            unsafe_allow_html=True
        )


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title(
        "📄 AI Resume Analyzer"
    )

    st.write(
        "Smart resume analysis powered by "
        "Python, NLP and machine learning."
    )

    st.divider()

    st.markdown(
        "### 🔍 Analysis Features"
    )

    st.write(
        "📄 PDF Resume Parsing"
    )

    st.write(
        "🧠 Skill Detection"
    )

    st.write(
        "🎯 Job Matching"
    )

    st.write(
        "🤖 NLP Similarity"
    )

    st.write(
        "🏆 ATS Scoring"
    )

    st.write(
        "💡 Recommendations"
    )

    st.write(
        "📥 PDF Report"
    )

    st.divider()

    st.caption(
        "Built with Python • Streamlit • NLP"
    )


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '''
    <div class="main-title">
        <span class="neon-letter">A</span>
        <span class="neon-letter">I</span>
        <span class="neon-space">&nbsp;</span>
        <span class="neon-letter">R</span>
        <span class="neon-letter">e</span>
        <span class="neon-letter">s</span>
        <span class="neon-letter">u</span>
        <span class="neon-letter">m</span>
        <span class="neon-letter">e</span>
        <span class="neon-space">&nbsp;</span>
        <span class="neon-letter">A</span>
        <span class="neon-letter">n</span>
        <span class="neon-letter">a</span>
        <span class="neon-letter">l</span>
        <span class="neon-letter">y</span>
        <span class="neon-letter">z</span>
        <span class="neon-letter">e</span>
        <span class="neon-letter">r</span>
    </div>
    ''',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze your resume against a job description '
    'and discover how well you match.'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# INPUT SECTION
# ==========================================

input_col1, input_col2 = st.columns(2)


with input_col1:

    st.subheader(
        "📄 Upload Resume"
    )

    uploaded_file = st.file_uploader(
        "Upload a PDF resume",
        type=["pdf"],
        label_visibility="collapsed"
    )


with input_col2:

    st.subheader(
        "💼 Job Description"
    )

    job_description = st.text_area(
        "Paste the job description",
        height=200,
        placeholder=(
            "Paste the complete job description "
            "here..."
        ),
        label_visibility="collapsed"
    )


st.divider()


# ==========================================
# ANALYZE BUTTON
# ==========================================

analyze_button = st.button(
    "🚀 Analyze Resume",
    type="primary",
    use_container_width=True
)


# ==========================================
# ANALYSIS
# ==========================================

if analyze_button:

    if not uploaded_file:

        st.error(
            "Please upload a PDF resume."
        )

        st.stop()


    if not job_description.strip():

        st.error(
            "Please enter a job description."
        )

        st.stop()


    # ======================================
    # EXTRACT RESUME TEXT
    # ======================================

    with st.spinner(
        "Analyzing your resume..."
    ):

        try:

            resume_text = (
                extract_text_from_pdf(
                    uploaded_file
                )
            )

        except Exception as error:

            st.error(
                f"Could not read the PDF: {error}"
            )

            st.stop()


    if not resume_text:

        st.error(
            "No text could be extracted from "
            "this PDF."
        )

        st.stop()


    # ======================================
    # CONTACT INFORMATION
    # ======================================

    email = extract_email(
        resume_text
    )

    phone = extract_phone(
        resume_text
    )

    linkedin = extract_linkedin(
        resume_text
    )

    github = extract_github(
        resume_text
    )


    # ======================================
    # SKILLS
    # ======================================

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_description
    )


    # ======================================
    # SKILL MATCH
    # ======================================

    match_result = calculate_skill_match(
        resume_skills,
        job_skills
    )

    skill_score = match_result[
        "score"
    ]

    matching_skills = match_result[
        "matching"
    ]

    missing_skills = match_result[
        "missing"
    ]


    # ======================================
    # NLP SIMILARITY
    # ======================================

    similarity_score = (
        calculate_text_similarity(
            resume_text,
            job_description
        )
    )


    # ======================================
    # OTHER SCORES
    # ======================================

    keyword_score = (
        calculate_keyword_score(
            resume_text,
            job_description
        )
    )

    structure_score = (
        calculate_structure_score(
            resume_text
        )
    )

    contact_score = (
        calculate_contact_score(
            email,
            phone,
            linkedin,
            github
        )
    )


    # ======================================
    # ATS SCORE
    # ======================================

    ats_score = calculate_ats_score(
        skill_score,
        similarity_score,
        keyword_score,
        structure_score,
        contact_score
    )


    # ======================================
    # RECOMMENDATIONS
    # ======================================

    recommendations = (
        generate_recommendations(
            missing_skills,
            keyword_score,
            structure_score,
            contact_score,
            ats_score
        )
    )


    # ======================================
    # SUCCESS
    # ======================================

    st.success(
        "✅ Resume analysis completed!"
    )


    # ======================================
    # SCORE CARDS
    # ======================================

    st.markdown(
        '<div class="section-title">'
        '📊 Analysis Overview'
        '</div>',
        unsafe_allow_html=True
    )


    score1, score2, score3 = (
        st.columns(3)
    )


    with score1:

        st.metric(
            "🏆 ATS Score",
            f"{ats_score}/100"
        )


    with score2:

        st.metric(
            "🎯 Skill Match",
            f"{skill_score}%"
        )


    with score3:

        st.metric(
            "🤖 NLP Similarity",
            f"{similarity_score}%"
        )


    st.divider()


    # ======================================
    # SCORE BREAKDOWN
    # ======================================

    st.subheader(
        "📈 Score Breakdown"
    )


    breakdown1, breakdown2 = (
        st.columns(2)
    )


    with breakdown1:

        st.write(
            f"**🎯 Skill Match:** "
            f"{skill_score}%"
        )

        st.progress(
            min(
                skill_score / 100,
                1.0
            )
        )


        st.write(
            f"**🔑 Keyword Relevance:** "
            f"{keyword_score}%"
        )

        st.progress(
            min(
                keyword_score / 100,
                1.0
            )
        )


    with breakdown2:

        st.write(
            f"**🤖 NLP Similarity:** "
            f"{similarity_score}%"
        )

        st.progress(
            min(
                similarity_score / 100,
                1.0
            )
        )


        st.write(
            f"**📋 Resume Structure:** "
            f"{structure_score}%"
        )

        st.progress(
            min(
                structure_score / 100,
                1.0
            )
        )


    # ======================================
    # SCORE MESSAGE
    # ======================================

    if ats_score >= 80:

        st.success(
            "🟢 Excellent! Your resume has "
            "strong alignment with this job."
        )

    elif ats_score >= 60:

        st.warning(
            "🟡 Good match, but your resume "
            "could be improved."
        )

    else:

        st.error(
            "🔴 Your resume needs improvement "
            "for this particular job."
        )


    # ======================================
    # TABS
    # ======================================

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🎯 Skills",
            "📋 Resume Info",
            "💡 Recommendations",
            "📄 Resume Text"
        ]
    )


    # ======================================
    # SKILLS TAB
    # ======================================

    with tab1:

        st.subheader(
            "🎯 Skill Analysis"
        )

        skill_col1, skill_col2 = (
            st.columns(2)
        )


        with skill_col1:

            st.markdown(
                "### ✅ Matching Skills"
            )

            if matching_skills:

                for skill in matching_skills:

                    st.success(
                        skill,
                        icon="✅"
                    )

            else:

                st.info(
                    "No matching skills found."
                )


        with skill_col2:

            st.markdown(
                "### ❌ Missing Skills"
            )

            if missing_skills:

                for skill in missing_skills:

                    st.warning(
                        skill,
                        icon="⚠️"
                    )

            else:

                st.success(
                    "No major missing skills detected!"
                )


        st.divider()

        st.subheader(
            "🧠 Resume Skills"
        )

        if resume_skills:

            for category, skills in (
                resume_skills.items()
            ):

                st.markdown(
                    f"**{category}**"
                )

                st.write(
                    " • ".join(skills)
                )


    # ======================================
    # RESUME INFO TAB
    # ======================================

    with tab2:

        st.subheader(
            "📋 Resume Information"
        )


        info1, info2 = st.columns(2)


        with info1:

            st.write(
                "📧 **Email**"
            )

            st.write(
                email
                if email
                else "Not detected"
            )


            st.write(
                "📱 **Phone**"
            )

            st.write(
                phone
                if phone
                else "Not detected"
            )


        with info2:

            st.write(
                "🔗 **LinkedIn**"
            )

            st.write(
                linkedin
                if linkedin
                else "Not detected"
            )


            st.write(
                "🐙 **GitHub**"
            )

            st.write(
                github
                if github
                else "Not detected"
            )


        st.divider()

        st.subheader(
            "💼 Job Description Skills"
        )

        if job_skills:

            for category, skills in (
                job_skills.items()
            ):

                st.markdown(
                    f"**{category}**"
                )

                st.write(
                    " • ".join(skills)
                )


    # ======================================
    # RECOMMENDATIONS TAB
    # ======================================

    with tab3:

        st.subheader(
            "💡 Resume Improvement Recommendations"
        )

        if recommendations:

            for index, recommendation in enumerate(
                recommendations,
                start=1
            ):

                st.info(
                    f"**{index}.** "
                    f"{recommendation}"
                )

        else:

            st.success(
                "Your resume looks well aligned "
                "with this job!"
            )


    # ======================================
    # RESUME TEXT TAB
    # ======================================

    with tab4:

        st.subheader(
            "📄 Extracted Resume Text"
        )

        st.text_area(
            "Resume Content",
            resume_text,
            height=500
        )


    # ======================================
    # DOWNLOAD REPORT
    # ======================================

    st.divider()

    st.subheader(
        "📥 Download Your Analysis"
    )

    report_file = create_analysis_report(
        ats_score=ats_score,
        skill_score=skill_score,
        similarity_score=similarity_score,
        keyword_score=keyword_score,
        structure_score=structure_score,
        contact_score=contact_score,
        matching_skills=matching_skills,
        missing_skills=missing_skills,
        recommendations=recommendations,
        email=email,
        phone=phone,
        linkedin=linkedin,
        github=github
    )

    st.download_button(
        label="📥 Download Analysis Report",
        data=report_file,
        file_name="resume_analysis_report.pdf",
        mime="application/pdf",
        use_container_width=True
    )