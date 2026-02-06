AGE_MAPPING = {
    "4-12": "Elementary School",
    "5-10": "Elementary School",
    "11-13": "Middle School",
    "13-15": "Middle School",
    "16-18": "High School"
}

def normalize_age(age_text):
    if not age_text:
        return ""
    age_text = age_text.strip()
    return AGE_MAPPING.get(age_text, age_text)
