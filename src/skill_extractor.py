import json
import re
from pathlib import Path


SKILLS_FILE = Path(__file__).resolve().parent.parent / "data" / "skills.json"


def load_skills():
    """
    Load the skill database from skills.json.
    """

    with open(SKILLS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def extract_skills(text):
    """
    Detect skills present in the given text.
    """

    skills_data = load_skills()

    found_skills = {}

    text_lower = text.lower()

    for category, skills in skills_data.items():

        matched_skills = []

        for skill in skills:

            skill_lower = skill.lower()

            # Escape special characters such as +, #, .
            pattern = r"(?<!\w)" + re.escape(skill_lower) + r"(?!\w)"

            if re.search(pattern, text_lower):

                matched_skills.append(skill)

        if matched_skills:

            found_skills[category] = matched_skills

    return found_skills