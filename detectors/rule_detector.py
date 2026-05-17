import re

patterns = [
    r"ignore previous instructions",
    r"reveal system prompt",
    r"bypass safety",
    r"show hidden configuration",
    r"pretend you are unrestricted",
    r"api keys",
]

def detect_rule_attack(text):

    text = text.lower()

    score = 0

    for pattern in patterns:
        if re.search(pattern, text):
            score += 0.2

    return min(score, 1.0)
