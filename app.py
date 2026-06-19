"""
AI-Powered Autocorrect Tool — Flask Backend
Uses TextBlob for NLP-based spelling correction.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from textblob import TextBlob

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    """Serve the frontend landing page."""
    return render_template("index.html")


@app.route("/correct", methods=["POST"])
def correct_text():
    """
    Receive text, run AI-powered spelling correction with TextBlob,
    and return the original + corrected versions.
    """
    try:
        data = request.get_json(silent=True) or {}
        original = (data.get("text") or "").strip()

        if not original:
            return jsonify({"error": "No text provided."}), 400

        corrected = str(TextBlob(original).correct())

        return jsonify({"original": original, "corrected": corrected})
    except Exception as exc:
        app.logger.exception("Correction failed: %s", exc)
        return jsonify({"error": "Unable to correct text."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
