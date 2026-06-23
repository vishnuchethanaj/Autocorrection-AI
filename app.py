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


def preserve_case(source_word: str, corrected_word: str) -> str:
    """Keep the original capitalization pattern when correcting a word."""
    if source_word.isupper():
        return corrected_word.upper()
    if source_word[:1].isupper():
        return corrected_word.capitalize()
    return corrected_word


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


def correct_text_with_spellchecker(text: str) -> str:
    """Correct only alphabetic words and keep punctuation/spacing unchanged."""
    parts = re.findall(r"[A-Za-z]+|[^A-Za-z]+", text)
    corrected_parts = [correct_word(part) if part.isalpha() else part for part in parts]
    return "".join(corrected_parts)


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
