"""Rule-based symptom helper.

This is not a diagnosis. It only matches words the user typed
against a small dictionary of known symptoms.
"""

import json
from pathlib import Path

RULES_PATH = Path(__file__).resolve().parent / "data" / "symptom_rules.json"
UNKNOWN_LOG = Path(__file__).resolve().parent / "data" / "unknown_queries.txt"


def load_rules():
    with RULES_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def check_symptoms(text, rules=None):
    """Return a result dict for a sentence typed by the user."""
    if rules is None:
        rules = load_rules()

    cleaned = text.lower().strip()
    if not cleaned:
        return {
            "matched": [],
            "category": "No input",
            "advice": "Type a symptom, for example: fever and headache.",
            "see_doctor_if": "If you feel very unwell, contact a doctor or campus clinic.",
        }

    matched = []
    for keyword, info in rules.items():
        if keyword in cleaned:
            matched.append({"keyword": keyword, **info})

    if not matched:
        UNKNOWN_LOG.parent.mkdir(parents=True, exist_ok=True)
        with UNKNOWN_LOG.open("a", encoding="utf-8") as handle:
            handle.write(cleaned + "\n")
        return {
            "matched": [],
            "category": "Not in the rule list",
            "advice": "This word is not in the campus rule file. It was saved so the list can be updated.",
            "see_doctor_if": "If the problem is serious, go to the campus clinic. This app cannot diagnose you.",
        }

    # If several keywords match, keep the first two so the answer stays short.
    top = matched[:2]
    categories = []
    advice_lines = []
    doctor_lines = []
    for item in top:
        if item["category"] not in categories:
            categories.append(item["category"])
        advice_lines.append(item["advice"])
        doctor_lines.append(item["see_doctor_if"])

    return {
        "matched": [item["keyword"] for item in top],
        "category": " + ".join(categories),
        "advice": " ".join(advice_lines),
        "see_doctor_if": " ".join(doctor_lines),
    }
