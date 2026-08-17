from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib.units import inch
from io import BytesIO


def create_analysis_report(
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
    github
):
    """
    Create a downloadable PDF analysis report.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=24,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=16,
        spaceBefore=15,
        spaceAfter=10
    )

    normal_style = ParagraphStyle(
        "ReportNormal",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15
    )

    story = []

    # ======================================
    # TITLE
    # ======================================

    story.append(
        Paragraph(
            "AI Resume Analyzer",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Resume Analysis & ATS Report",
            styles["Heading3"]
        )
    )

    story.append(Spacer(1, 20))


    # ======================================
    # ATS SCORE
    # ======================================

    story.append(
        Paragraph(
            "ATS Score",
            heading_style
        )
    )

    score_table = Table(
        [
            ["ATS Score", "Skill Match", "NLP Similarity"],
            [
                f"{ats_score}/100",
                f"{skill_score}%",
                f"{similarity_score}%"
            ]
        ],
        colWidths=[
            1.8 * inch,
            1.8 * inch,
            1.8 * inch
        ]
    )

    score_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.black
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "FONTNAME",
                (0, 1),
                (-1, 1),
                "Helvetica-Bold"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                11
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                1,
                colors.grey
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                10
            )
        ])
    )

    story.append(score_table)

    story.append(Spacer(1, 20))


    # ======================================
    # SCORE BREAKDOWN
    # ======================================

    story.append(
        Paragraph(
            "Score Breakdown",
            heading_style
        )
    )

    breakdown_table = Table(
        [
            ["Metric", "Score"],
            ["Skill Match", f"{skill_score}%"],
            ["NLP Similarity", f"{similarity_score}%"],
            ["Keyword Relevance", f"{keyword_score}%"],
            ["Resume Structure", f"{structure_score}%"],
            ["Contact Information", f"{contact_score}%"]
        ],
        colWidths=[
            3.8 * inch,
            1.8 * inch
        ]
    )

    breakdown_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "ALIGN",
                (1, 1),
                (1, -1),
                "CENTER"
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            )
        ])
    )

    story.append(
        breakdown_table
    )


    # ======================================
    # CONTACT INFORMATION
    # ======================================

    story.append(
        Paragraph(
            "Candidate Information",
            heading_style
        )
    )

    contact_table = Table(
        [
            ["Email", email or "Not detected"],
            ["Phone", phone or "Not detected"],
            ["LinkedIn", linkedin or "Not detected"],
            ["GitHub", github or "Not detected"]
        ],
        colWidths=[
            1.5 * inch,
            4.1 * inch
        ]
    )

    contact_table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            )
        ])
    )

    story.append(
        contact_table
    )


    # ======================================
    # MATCHING SKILLS
    # ======================================

    story.append(
        Paragraph(
            "Matching Skills",
            heading_style
        )
    )

    if matching_skills:

        for skill in matching_skills:

            story.append(
                Paragraph(
                    f"✓ {skill}",
                    normal_style
                )
            )

    else:

        story.append(
            Paragraph(
                "No matching skills found.",
                normal_style
            )
        )


    # ======================================
    # MISSING SKILLS
    # ======================================

    story.append(
        Paragraph(
            "Missing Skills",
            heading_style
        )
    )

    if missing_skills:

        for skill in missing_skills:

            story.append(
                Paragraph(
                    f"• {skill}",
                    normal_style
                )
            )

    else:

        story.append(
            Paragraph(
                "No major missing skills detected.",
                normal_style
            )
        )


    # ======================================
    # RECOMMENDATIONS
    # ======================================

    story.append(
        Paragraph(
            "Resume Improvement Recommendations",
            heading_style
        )
    )

    if recommendations:

        for index, recommendation in enumerate(
            recommendations,
            start=1
        ):

            story.append(
                Paragraph(
                    f"{index}. {recommendation}",
                    normal_style
                )
            )

            story.append(
                Spacer(1, 5)
            )

    else:

        story.append(
            Paragraph(
                "No recommendations available.",
                normal_style
            )
        )


    # ======================================
    # FOOTER
    # ======================================

    story.append(
        Spacer(1, 25)
    )

    story.append(
        Paragraph(
            "Generated by AI Resume Analyzer",
            styles["Italic"]
        )
    )


    document.build(story)

    buffer.seek(0)

    return buffer