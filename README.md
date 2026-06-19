# AI-Powered Autocorrect Tool

A modern Flask web application that corrects spelling mistakes in real time using pyspellchecker and a responsive HTML/CSS/JavaScript frontend.

## Features

- AI-assisted spelling correction with protected technical terms
- Flask backend with REST API
- Responsive, modern UI
- Copy corrected text button
- Clear text button
- Live character counter

## Tech Stack

- Frontend: HTML5, CSS3, JavaScript
- Backend: Python, Flask, Flask-CORS
- NLP: pyspellchecker

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

2. Run the app:

```bash
python app.py
```

3. Open the app in your browser:

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
