import re


# =========================================================
# BASIC ATS SCORING
# =========================================================

def calculate_keyword_score(
    resume_text,
    job_description
):
    """
    Calculate keyword overlap between resume
    and job description.
    """

    resume_words = set(
        extract_keywords(resume_text)
    )

    job_words = set(
        extract_keywords(job_description)
    )

    if not job_words:
        return 0

    matching_words = (
        resume_words.intersection(
            job_words
        )
    )

    score = (
        len(matching_words)
        / len(job_words)
    ) * 100

    return round(
        min(score, 100),
        2
    )


# =========================================================
# RESUME STRUCTURE SCORE
# =========================================================

def calculate_structure_score(
    resume_text
):
    """
    Estimate resume structure using
    common resume sections.
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


# =========================================================
# CONTACT SCORE
# =========================================================

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


# =========================================================
# ATS SCORE
# =========================================================

def calculate_ats_score(
    skill_score,
    similarity_score,
    keyword_score,
    structure_score,
    contact_score
):
    """
    Calculate the project's heuristic ATS score.

    This is NOT the score produced by
    a real employer ATS.
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


# =========================================================
# SMART KEYWORD EXTRACTION
# =========================================================

def extract_keywords(text):
    """
    Extract meaningful keywords from text.

    Removes common filler words while keeping
    technical terms such as:
        C++
        C#
        Node.js
        React.js
        CI/CD
        PostgreSQL
    """

    if not text:
        return set()


    text = text.lower()


    # -----------------------------------------------------
    # Normalize common technical spellings
    # -----------------------------------------------------

    text = text.replace(
        "machine-learning",
        "machine learning"
    )

    text = text.replace(
        "deep-learning",
        "deep learning"
    )

    text = text.replace(
        "artificial-intelligence",
        "artificial intelligence"
    )

    text = text.replace(
        "natural-language-processing",
        "natural language processing"
    )


    # -----------------------------------------------------
    # Extract words
    # -----------------------------------------------------

    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z0-9+#./-]*\b",
        text
    )


    # -----------------------------------------------------
    # Stop words
    # -----------------------------------------------------

    stop_words = {

        "the",
        "and",
        "for",
        "with",
        "from",
        "this",
        "that",
        "are",
        "you",
        "your",
        "our",
        "have",
        "has",
        "had",
        "will",
        "would",
        "could",
        "should",
        "can",
        "may",
        "might",

        "into",
        "using",
        "use",
        "used",
        "work",
        "working",
        "worked",

        "role",
        "job",
        "candidate",
        "required",
        "requirements",

        "looking",
        "seeking",
        "preferred",

        "years",
        "year",
        "month",
        "months",

        "ability",
        "strong",
        "good",
        "excellent",

        "team",
        "teams",
        "environment",

        "responsibilities",
        "responsibility",

        "including",
        "etc",

        "about",
        "more",
        "their",
        "they",
        "them",
        "these",
        "those",

        "who",
        "what",
        "when",
        "where",
        "which",
        "how",

        "not",
        "but",
        "also",

        "all",
        "any",
        "some",

        "our",
        "we",
        "us",

        "a",
        "an",
        "as",
        "at",
        "by",
        "in",
        "of",
        "on",
        "to"
    }


    # -----------------------------------------------------
    # Clean keywords
    # -----------------------------------------------------

    keywords = set()


    for word in words:

        word = word.strip(
            ".,:;()[]{}\"'!?|"
        )

        if len(word) < 3:
            continue

        if word in stop_words:
            continue

        keywords.add(
            word
        )


    # -----------------------------------------------------
    # Detect important multi-word technical phrases
    # -----------------------------------------------------

    technical_phrases = [

        "machine learning",

        "deep learning",

        "artificial intelligence",

        "natural language processing",

        "computer vision",

        "data science",

        "data analysis",

        "data engineering",

        "software engineering",

        "software development",

        "web development",

        "full stack",

        "full stack development",

        "frontend development",

        "backend development",

        "cloud computing",

        "cloud computing",

        "database management",

        "object oriented programming",

        "object-oriented programming",

        "version control",

        "continuous integration",

        "continuous deployment",

        "ci/cd",

        "generative ai",

        "large language model",

        "large language models",

        "neural network",

        "neural networks",

        "reinforcement learning",

        "computer science",

        "api development",

        "rest api",

        "restful api",

        "microservices",

        "system design"
    ]


    for phrase in technical_phrases:

        if phrase in text:

            keywords.add(
                phrase
            )


    return keywords


# =========================================================
# KEYWORD CANONICALIZATION
# =========================================================

KEYWORD_ALIASES = {

    "ml": "machine learning",

    "machine-learning":
        "machine learning",

    "ai":
        "artificial intelligence",

    "artificial-intelligence":
        "artificial intelligence",

    "nlp":
        "natural language processing",

    "natural-language-processing":
        "natural language processing",

    "dl":
        "deep learning",

    "cv":
        "computer vision",

    "js":
        "javascript",

    "javascript":
        "javascript",

    "ts":
        "typescript",

    "py":
        "python",

    "postgres":
        "postgresql",

    "psql":
        "postgresql",

    "mongo":
        "mongodb",

    "gcp":
        "google cloud platform",

    "aws":
        "amazon web services",

    "azure":
        "microsoft azure",

    "k8s":
        "kubernetes",

    "cicd":
        "ci/cd",

    "ci cd":
        "ci/cd",

    "reactjs":
        "react",

    "react.js":
        "react",

    "nodejs":
        "node.js",

    "node":
        "node.js",

    "tf":
        "tensorflow",

    "torch":
        "pytorch"
}


def normalize_keyword(
    keyword
):
    """
    Convert keyword aliases into
    canonical keyword names.
    """

    keyword = (
        keyword
        .lower()
        .strip()
    )

    return KEYWORD_ALIASES.get(
        keyword,
        keyword
    )


# =========================================================
# KEYWORD GAP ANALYSIS
# =========================================================

def calculate_keyword_gap(
    resume_text,
    job_description
):
    """
    Compare important keywords between
    the resume and job description.

    Returns:

        score
        matched_keywords
        missing_keywords
    """

    resume_keywords = extract_keywords(
        resume_text
    )

    job_keywords = extract_keywords(
        job_description
    )


    if not job_keywords:

        return {

            "score": 0,

            "matched_keywords": [],

            "missing_keywords": []

        }


    # -----------------------------------------------------
    # Normalize keywords
    # -----------------------------------------------------

    normalized_resume = {}

    for keyword in resume_keywords:

        canonical = normalize_keyword(
            keyword
        )

        normalized_resume[
            canonical
        ] = keyword


    normalized_job = {}

    for keyword in job_keywords:

        canonical = normalize_keyword(
            keyword
        )

        normalized_job[
            canonical
        ] = keyword


    # -----------------------------------------------------
    # Compare
    # -----------------------------------------------------

    matched_keywords = []

    missing_keywords = []


    for (
        canonical,
        original_job_keyword
    ) in normalized_job.items():

        if canonical in normalized_resume:

            matched_keywords.append(
                original_job_keyword
            )

        else:

            missing_keywords.append(
                original_job_keyword
            )


    # -----------------------------------------------------
    # Remove duplicates
    # -----------------------------------------------------

    matched_keywords = sorted(
        set(matched_keywords),
        key=str.lower
    )

    missing_keywords = sorted(
        set(missing_keywords),
        key=str.lower
    )


    # -----------------------------------------------------
    # Score
    # -----------------------------------------------------

    total_keywords = len(
        normalized_job
    )

    if total_keywords == 0:

        score = 0

    else:

        score = (
            len(matched_keywords)
            / total_keywords
        ) * 100


    return {

        "score": round(
            min(score, 100),
            2
        ),

        "matched_keywords":
            matched_keywords,

        "missing_keywords":
            missing_keywords

    }


# =========================================================
# EXPERIENCE RELEVANCE
# =========================================================

def calculate_experience_relevance(
    resume_text,
    job_description
):
    """
    Estimate experience relevance using
    experience-related terminology.

    This is a heuristic project metric.
    """

    if not resume_text or not job_description:

        return 0


    experience_terms = {

        "experience",

        "internship",

        "intern",

        "developer",

        "engineer",

        "analyst",

        "project",

        "developed",

        "built",

        "designed",

        "implemented",

        "managed",

        "led",

        "created",

        "worked"

    }


    resume_words = set(
        re.findall(
            r"\b[a-zA-Z]+\b",
            resume_text.lower()
        )
    )


    job_words = set(
        re.findall(
            r"\b[a-zA-Z]+\b",
            job_description.lower()
        )
    )


    job_experience_terms = (
        job_words.intersection(
            experience_terms
        )
    )


    if not job_experience_terms:

        return 50


    matching_terms = (
        resume_words.intersection(
            job_experience_terms
        )
    )


    score = (
        len(matching_terms)
        / len(job_experience_terms)
    ) * 100


    return round(
        min(score, 100),
        2
    )


# =========================================================
# ADDITIONAL ATS CHECKS
# =========================================================

def calculate_ats_checks(
    resume_text,
    email=None,
    phone=None,
    linkedin=None,
    github=None
):
    """
    Perform additional resume quality checks.
    """

    text = (
        resume_text.lower()
        if resume_text
        else ""
    )


    checks = {

        "contact_information":
            bool(
                email or phone
            ),

        "linkedin_present":
            bool(linkedin),

        "github_present":
            bool(github),

        "education_present":
            "education" in text,

        "experience_present":
            (
                "experience" in text
                or "work experience" in text
            ),

        "skills_present":
            "skills" in text,

        "projects_present":
            "projects" in text,

        "certifications_present":
            (
                "certifications" in text
                or "certification" in text
            ),

        "reasonable_length":
            (
                300 <= len(
                    resume_text.split()
                ) <= 1500
                if resume_text
                else False
            )

    }


    return checks


# =========================================================
# RESUME SECTION DETECTION
# =========================================================

def detect_resume_sections(
    resume_text
):
    """
    Detect common resume sections.
    """

    if not resume_text:

        return {}


    text = resume_text.lower()


    section_aliases = {

        "Summary": [

            "summary",

            "professional summary",

            "profile",

            "objective",

            "career objective"

        ],

        "Education": [

            "education",

            "academic background",

            "academic qualifications"

        ],

        "Experience": [

            "experience",

            "work experience",

            "professional experience",

            "employment history"

        ],

        "Skills": [

            "skills",

            "technical skills",

            "core skills",

            "key skills"

        ],

        "Projects": [

            "projects",

            "academic projects",

            "personal projects",

            "project experience"

        ],

        "Certifications": [

            "certifications",

            "certificates",

            "professional certifications"

        ],

        "Achievements": [

            "achievements",

            "accomplishments",

            "awards"

        ],

        "Languages": [

            "languages",

            "language proficiency"

        ]

    }


    detected = {}


    for (
        section,
        aliases
    ) in section_aliases.items():

        found = False


        for alias in aliases:

            pattern = (
                r"\b"
                + re.escape(alias)
                + r"\b"
            )


            if re.search(
                pattern,
                text
            ):

                found = True

                break


        detected[
            section
        ] = found


    return detected


# =========================================================
# BULLET-POINT ANALYZER
# =========================================================

def analyze_resume_bullets(
    resume_text
):
    """
    Analyze resume bullet points for:

    - strong action verbs
    - weak phrases
    - measurable achievements
    """

    if not resume_text:

        return {

            "total_bullets": 0,

            "strong_bullets": 0,

            "weak_bullets": 0,

            "achievement_bullets": 0,

            "weak_phrases": [],

            "metrics_found": []

        }


    lines = resume_text.splitlines()


    action_verbs = {

        "developed",

        "built",

        "created",

        "designed",

        "implemented",

        "engineered",

        "optimized",

        "automated",

        "analyzed",

        "deployed",

        "managed",

        "led",

        "improved",

        "integrated",

        "tested",

        "configured",

        "delivered"

    }


    weak_phrases = {

        "responsible for",

        "worked on",

        "helped with",

        "involved in",

        "participated in",

        "worked with",

        "was responsible"

    }


    bullet_lines = []


    for line in lines:

        cleaned = line.strip()


        if not cleaned:

            continue


        if cleaned.startswith(
            (
                "-",
                "•",
                "*",
                "▪",
                "●",
                "→"
            )
        ):

            bullet_lines.append(
                cleaned
            )


    strong_bullets = 0

    weak_bullets = 0

    achievement_bullets = 0


    detected_weak_phrases = set()

    detected_metrics = set()


    for bullet in bullet_lines:

        bullet_lower = (
            bullet.lower()
        )


        has_action_verb = any(

            re.search(

                r"\b"
                + re.escape(verb)
                + r"\b",

                bullet_lower

            )

            for verb in action_verbs

        )


        if has_action_verb:

            strong_bullets += 1


        found_weak = False


        for phrase in weak_phrases:

            if phrase in bullet_lower:

                detected_weak_phrases.add(
                    phrase
                )

                found_weak = True


        if found_weak:

            weak_bullets += 1


        metrics = re.findall(

            r"\b\d+(?:\.\d+)?%?\b",

            bullet

        )


        if metrics:

            achievement_bullets += 1

            detected_metrics.update(
                metrics
            )


    return {

        "total_bullets":
            len(bullet_lines),

        "strong_bullets":
            strong_bullets,

        "weak_bullets":
            weak_bullets,

        "achievement_bullets":
            achievement_bullets,

        "weak_phrases":
            sorted(
                detected_weak_phrases
            ),

        "metrics_found":
            sorted(
                detected_metrics
            )

    }