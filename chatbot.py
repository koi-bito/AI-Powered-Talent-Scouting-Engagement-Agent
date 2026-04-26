def engage(candidate):
    level = candidate.get("interest_level", "medium")
    responses = {
        "high": "Very interested!",
        "medium": "Somewhat interested.",
        "low": "Not very interested."
    }
    return responses.get(level, "Neutral")
