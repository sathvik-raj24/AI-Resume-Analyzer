import json
import re
from pathlib import Path


SKILLS_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "skills.json"
)


# =========================================================
# SKILL SYNONYMS
# =========================================================

SKILL_SYNONYMS = {

    # Artificial Intelligence
    "ai": "Artificial Intelligence",
    "artificial intelligence": "Artificial Intelligence",

    # Machine Learning
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",

    # Deep Learning
    "dl": "Deep Learning",
    "deep learning": "Deep Learning",

    # Natural Language Processing
    "nlp": "Natural Language Processing",
    "natural language processing": "Natural Language Processing",

    # Computer Vision
    "cv": "Computer Vision",
    "computer vision": "Computer Vision",

    # Programming
    "py": "Python",
    "python": "Python",

    "js": "JavaScript",
    "javascript": "JavaScript",

    "ts": "TypeScript",
    "typescript": "TypeScript",

    "cpp": "C++",
    "c++": "C++",

    "csharp": "C#",
    "c#": "C#",

    # Databases
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",

    "mongo": "MongoDB",
    "mongodb": "MongoDB",

    # Cloud
    "aws": "AWS",
    "amazon web services": "AWS",

    "gcp": "Google Cloud",
    "google cloud": "Google Cloud",

    "azure": "Microsoft Azure",
    "microsoft azure": "Microsoft Azure",

    # DevOps
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",

    "docker": "Docker",

    # Frameworks
    "reactjs": "React",
    "react.js": "React",
    "react": "React",

    "nodejs": "Node.js",
    "node.js": "Node.js",
    "node": "Node.js",

    # ML Frameworks
    "torch": "PyTorch",
    "pytorch": "PyTorch",

    "tf": "TensorFlow",
    "tensorflow": "TensorFlow",

    # Version Control
    "git": "Git",
    "github": "GitHub",
}


# =========================================================
# LOAD SKILLS
# =========================================================

def load_skills():

    """
    Load the skill database from skills.json.
    """

    with open(
        SKILLS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# =========================================================
# NORMALIZE SKILL
# =========================================================

def normalize_skill(skill):

    """
    Convert skill synonyms into a common canonical name.
    """

    skill_clean = skill.strip()

    skill_lower = skill_clean.lower()

    return SKILL_SYNONYMS.get(
        skill_lower,
        skill_clean
    )


# =========================================================
# CHECK SKILL IN TEXT
# =========================================================

def skill_exists(
    skill,
    text_lower
):

    """
    Check whether a skill or one of its known
    synonyms exists in the supplied text.
    """

    canonical_skill = normalize_skill(
        skill
    )

    # Find every synonym that maps to
    # the same canonical skill.
    possible_names = []

    for synonym, canonical in (
        SKILL_SYNONYMS.items()
    ):

        if canonical.lower() == (
            canonical_skill.lower()
        ):

            possible_names.append(
                synonym
            )


    # Always include original skill
    possible_names.append(
        skill.lower()
    )


    # Remove duplicates
    possible_names = list(
        set(possible_names)
    )


    for name in possible_names:

        pattern = (
            r"(?<!\w)"
            + re.escape(name)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            text_lower
        ):

            return True


    return False


# =========================================================
# EXTRACT SKILLS
# =========================================================

def extract_skills(text):

    """
    Detect skills present in the given text.

    Supports both exact skill matching and
    common skill synonyms.
    """

    skills_data = load_skills()

    found_skills = {}

    text_lower = text.lower()


    for category, skills in (
        skills_data.items()
    ):

        matched_skills = []


        for skill in skills:

            if skill_exists(
                skill,
                text_lower
            ):

                # Keep the original name
                # from skills.json.
                matched_skills.append(
                    skill
                )


        if matched_skills:

            found_skills[
                category
            ] = matched_skills


    return found_skills