import re


def clean_text(text):
    """
    Clean extracted resume text for further analysis.
    """

    # Convert everything to lowercase
    text = text.lower()

    # Replace multiple spaces/newlines with one space
    text = re.sub(r"\s+", " ", text)

    # Remove unnecessary special characters
    text = re.sub(r"[^a-zA-Z0-9@.+#\-/ ]", "", text)

    return text.strip()
def extract_email(text):
    """
    Extract email address from resume text.
    """

    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return None
def extract_phone(text):
    """
    Extract Indian phone number from resume text.
    """

    pattern = r"(?:\+91[\s-]?)?[6-9]\d{9}"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return None
def extract_linkedin(text):
    """
    Extract LinkedIn profile URL.
    """

    pattern = r"(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group(0)

    return None
def extract_github(text):
    """
    Extract GitHub profile URL.
    """

    pattern = r"(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group(0)

    return None