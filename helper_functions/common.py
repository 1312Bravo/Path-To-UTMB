import re

# -------------------------------------------------
# Time to hours conversion 
# -------------------------------------------------

def time_to_hours(timestr):
    try:
        h, m, s = map(int, timestr.split(":"))
        return h + (m / 60) + (s / 3600)
    except Exception:
        return None

# -------------------------------------------------
# Convert string to snake case
# -------------------------------------------------

def to_snake_case(text: str) -> str:
    text = re.sub(r"(?<!^)(?=[A-Z])", "_", text)
    return text.lower()