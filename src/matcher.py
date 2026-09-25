# =========================================================
# SMART SKILL MATCHER
# AI Resume Skill Extraction & Job Matching
# =========================================================

# Common skill aliases / synonyms.
# Add more aliases here as your project grows.

SKILL_ALIASES = {

    # AI / ML
    "machine learning": {
        "machine learning",
        "ml",
        "machine-learning"
    },

    "artificial intelligence": {
        "artificial intelligence",
        "ai"
    },

    "natural language processing": {
        "natural language processing",
        "nlp"
    },

    "deep learning": {
        "deep learning",
        "dl"
    },

    "computer vision": {
        "computer vision",
        "cv"
    },

    # Programming
    "javascript": {
        "javascript",
        "js",
        "java script"
    },

    "typescript": {
        "typescript",
        "ts",
        "type script"
    },

    "python": {
        "python",
        "py"
    },

    "c++": {
        "c++",
        "cpp"
    },

    "c#": {
        "c#",
        "csharp",
        "c sharp"
    },

    # Databases
    "postgresql": {
        "postgresql",
        "postgres",
        "psql"
    },

    "mysql": {
        "mysql",
        "my sql"
    },

    "microsoft sql server": {
        "microsoft sql server",
        "sql server",
        "mssql"
    },

    "mongodb": {
        "mongodb",
        "mongo",
        "mongo db"
    },

    # Cloud
    "amazon web services": {
        "amazon web services",
        "aws"
    },

    "google cloud platform": {
        "google cloud platform",
        "google cloud",
        "gcp"
    },

    "microsoft azure": {
        "microsoft azure",
        "azure"
    },

    # DevOps
    "continuous integration": {
        "continuous integration",
        "ci"
    },

    "continuous deployment": {
        "continuous deployment",
        "cd"
    },

    "ci/cd": {
        "ci/cd",
        "cicd",
        "ci cd"
    },

    "kubernetes": {
        "kubernetes",
        "k8s"
    },

    "docker": {
        "docker"
    },

    # Frameworks
    "react": {
        "react",
        "reactjs",
        "react.js"
    },

    "node.js": {
        "node.js",
        "nodejs",
        "node"
    },

    "next.js": {
        "next.js",
        "nextjs"
    },

    # ML Frameworks
    "tensorflow": {
        "tensorflow",
        "tf"
    },

    "pytorch": {
        "pytorch",
        "torch"
    },

    # Version control
    "github": {
        "github",
        "git hub"
    },

    "git": {
        "git"
    }
}


# =========================================================
# NORMALIZE TEXT
# =========================================================

def clean_skill(skill):
    """
    Clean a skill name before comparison.
    """

    return (
        str(skill)
        .lower()
        .strip()
        .replace("–", "-")
        .replace("—", "-")
    )


# =========================================================
# FLATTEN SKILLS
# =========================================================

def flatten_skills(skills_dict):
    """
    Convert categorized skills into one set of skills.
    """

    all_skills = set()

    if not skills_dict:
        return all_skills

    for skills in skills_dict.values():

        if not skills:
            continue

        for skill in skills:

            all_skills.add(
                clean_skill(skill)
            )

    return all_skills


# =========================================================
# NORMALIZE SKILL
# =========================================================

def normalize_skill(skill):
    """
    Normalize a skill so aliases can be compared.
    """

    skill = clean_skill(skill)

    for canonical_skill, aliases in (
        SKILL_ALIASES.items()
    ):

        cleaned_aliases = {
            clean_skill(alias)
            for alias in aliases
        }

        if skill in cleaned_aliases:

            return canonical_skill

    return skill


# =========================================================
# CALCULATE SKILL MATCH
# =========================================================

def calculate_skill_match(
    resume_skills,
    job_skills
):
    """
    Compare resume skills with job-required skills
    using smart synonym / alias matching.
    """

    resume_set = flatten_skills(
        resume_skills
    )

    job_set = flatten_skills(
        job_skills
    )


    # -----------------------------------------------------
    # No job skills
    # -----------------------------------------------------

    if not job_set:

        return {
            "score": 0,
            "matching": [],
            "missing": []
        }


    # -----------------------------------------------------
    # Normalize resume skills
    # -----------------------------------------------------

    normalized_resume = {}

    for skill in resume_set:

        canonical = normalize_skill(
            skill
        )

        if canonical not in normalized_resume:

            normalized_resume[
                canonical
            ] = skill


    # -----------------------------------------------------
    # Normalize job skills
    # -----------------------------------------------------

    normalized_job = {}

    for skill in job_set:

        canonical = normalize_skill(
            skill
        )

        if canonical not in normalized_job:

            normalized_job[
                canonical
            ] = skill


    # -----------------------------------------------------
    # Compare
    # -----------------------------------------------------

    matching_skills = []

    missing_skills = []


    for (
        canonical_skill,
        job_original
    ) in normalized_job.items():

        if canonical_skill in normalized_resume:

            matching_skills.append(
                job_original
            )

        else:

            missing_skills.append(
                job_original
            )


    # -----------------------------------------------------
    # Remove duplicates
    # -----------------------------------------------------

    matching_skills = sorted(
        set(matching_skills),
        key=str.lower
    )

    missing_skills = sorted(
        set(missing_skills),
        key=str.lower
    )


    # -----------------------------------------------------
    # Calculate score
    # -----------------------------------------------------

    total_required = len(
        normalized_job
    )

    if total_required == 0:

        score = 0

    else:

        score = (
            len(matching_skills)
            / total_required
        ) * 100


    return {
        "score": round(
            score,
            2
        ),

        "matching": matching_skills,

        "missing": missing_skills
    }