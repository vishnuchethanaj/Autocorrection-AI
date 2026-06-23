"""
AI-Powered Autocorrect Tool — Flask Backend
Uses pyspellchecker for spelling correction.
"""

import re
import os

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from spellchecker import SpellChecker

app = Flask(__name__)
CORS(app)

spell_checker = SpellChecker()

PROTECTED_WORDS = {
    "ai",
    "api",
    "css",
    "flask",
    "github",
    "html",
    "javascript",
    "nlp",
    "python",
    "textblob",
}

COMMON_CORRECTIONS = {
    "hye": "hey",
    "applicaton": "application",
    "learning": "learning",
    "programing": "programming",
    "usefull": "useful",
}

GRAMMAR_RULES = [
    # Pronoun + be verb agreement
    (r"\bI\s+is\b", "I am"),
    (r"\bI\s+are\b", "I am"),
    (r"\b(He|She|It)\s+are\b", r"\1 is"),
    (r"\b(We|They|You)\s+is\b", r"\1 are"),
    # Article usage for simple vowel/consonant mismatches
    (r"\ba\s+([aeiouAEIOU][A-Za-z]*)\b", r"an \1"),
    (r"\ban\s+([bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ][A-Za-z]*)\b", r"a \1"),
]

IRREGULAR_PAST_TO_BASE = {
    "went": "go",
    "ate": "eat",
    "saw": "see",
    "came": "come",
    "did": "do",
    "was": "be",
    "were": "be",
    "had": "have",
    "made": "make",
    "took": "take",
    "gave": "give",
}


def preserve_case(source_word: str, corrected_word: str) -> str:
    """Keep the original capitalization pattern when correcting a word."""
    if source_word.isupper():
        return corrected_word.upper()
    if source_word[:1].isupper():
        return corrected_word.capitalize()
    return corrected_word


def preserve_replacement_case(source_text: str, replacement_text: str) -> str:
    """Preserve broad capitalization style while replacing grammar patterns."""
    if source_text.isupper():
        return replacement_text.upper()
    if source_text[:1].isupper():
        return replacement_text[:1].upper() + replacement_text[1:]
    return replacement_text


def to_base_form_after_does(verb: str) -> str:
    """Convert likely third-person singular verb to base form after 'doesn't'."""
    lower = verb.lower()
    if lower.endswith("ies") and len(lower) > 3:
        return lower[:-3] + "y"
    if lower.endswith(("oes", "ses", "shes", "ches", "xes", "zes")) and len(lower) > 3:
        return lower[:-2]
    if lower.endswith("s") and len(lower) > 2:
        return lower[:-1]
    return lower


def to_base_form_after_did(verb: str) -> str:
    """Convert likely past-tense verb to base form after 'didn't'."""
    lower = verb.lower()
    if lower in IRREGULAR_PAST_TO_BASE:
        return IRREGULAR_PAST_TO_BASE[lower]
    if lower.endswith("ied") and len(lower) > 3:
        return lower[:-3] + "y"
    if lower.endswith("ed") and len(lower) > 3:
        return lower[:-2]
    return lower


def correct_word(word: str) -> str:
    """Correct a single word while protecting technical terms and short words."""
    normalized = word.lower()

    if normalized in COMMON_CORRECTIONS:
        return preserve_case(word, COMMON_CORRECTIONS[normalized])

    if len(word) <= 2 or normalized in PROTECTED_WORDS:
        return word

    if normalized in spell_checker:
        return word

    suggestion = spell_checker.correction(normalized)
    if not suggestion or suggestion == normalized:
        return word

    return preserve_case(word, suggestion)


def correct_grammar_rules(text: str) -> str:
    """Apply lightweight grammar corrections for common sentence-level mistakes."""
    corrected = text

    for pattern, replacement in GRAMMAR_RULES:
        def _replace(match: re.Match) -> str:
            replaced = match.expand(replacement)
            return preserve_replacement_case(match.group(0), replaced)

        corrected = re.sub(pattern, _replace, corrected, flags=re.IGNORECASE)

    corrected = re.sub(
        r"\b(?:doesn['’]?t|does['’]?t|doesnt)\s+([A-Za-z]+)\b",
        lambda m: preserve_replacement_case(m.group(0), f"doesn't {to_base_form_after_does(m.group(1))}"),
        corrected,
        flags=re.IGNORECASE,
    )

    corrected = re.sub(
        r"\b(?:didn['’]?t|did['’]?t|didnt)\s+([A-Za-z]+)\b",
        lambda m: preserve_replacement_case(m.group(0), f"didn't {to_base_form_after_did(m.group(1))}"),
        corrected,
        flags=re.IGNORECASE,
    )

    return corrected


def correct_text_with_spellchecker(text: str) -> str:
    """Correct spelling first, then fix common sentence-level grammar mistakes."""
    parts = re.findall(r"[A-Za-z]+|[^A-Za-z]+", text)
    corrected_parts = [correct_word(part) if part.isalpha() else part for part in parts]
    spelled_text = "".join(corrected_parts)
    return correct_grammar_rules(spelled_text)


@app.route("/")
def index():
    """Serve the frontend landing page."""
    return render_template("index.html")


@app.route("/correct", methods=["POST"])
def correct_text():
    """
    Receive text, run AI-powered spelling correction with pyspellchecker,
    and return the original + corrected versions.
    """
    try:
        data = request.get_json(silent=True) or {}
        original = (data.get("text") or "").strip()

        if not original:
            return jsonify({"error": "No text provided."}), 400

        corrected = correct_text_with_spellchecker(original)

        return jsonify({"original": original, "corrected": corrected})
    except Exception as exc:
        app.logger.exception("Correction failed: %s", exc)
        return jsonify({"error": "Unable to correct text."}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
