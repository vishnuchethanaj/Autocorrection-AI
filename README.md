# AI-Powered Autocorrect Tool

A modern Flask web application that corrects spelling mistakes in real time using TextBlob and a responsive HTML/CSS/JavaScript frontend.

## Features

- AI-assisted spelling correction
- Flask backend with REST API
- Responsive, modern UI
- Copy corrected text button
- Clear text button
- Live character counter

## Tech Stack

- Frontend: HTML5, CSS3, JavaScript
- Backend: Python, Flask, Flask-CORS
- NLP: TextBlob

## Project Structure

```text
AutocorrectTool/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Download the required TextBlob corpora:

```bash
python -m textblob.download_corpora
```

3. Run the app:

```bash
python app.py
```

4. Open the app in your browser:

```text
http://127.0.0.1:5000
```

## API

### POST /correct

Request:

```json
{
  "text": "I am lerning artificail inteligence."
}
```

Response:

```json
{
  "original": "I am lerning artificail inteligence.",
  "corrected": "I am learning artificial intelligence."
}
```
