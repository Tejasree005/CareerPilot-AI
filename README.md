# CareerPilot AI — Career & Internship Platform

A portfolio project built with Python, Flask, SQLite, HTML, CSS, and JavaScript. It demonstrates a simple career exploration workflow with sample job listings, saved jobs, a local application tracker, and a resume keyword comparison tool.

## Features

- Responsive landing page and modern dark UI
- Search and filter sample job/internship listings
- Save and unsave roles using SQLite
- Record demo applications locally
- Compare pasted resume text or a text-based PDF with a job description
- Show an approximate keyword-overlap score, matched keywords, and potential gaps
- Mobile navigation and responsive layouts

## Important project limitations

- Job listings are sample data, not live or verified vacancies.
- Demo application submissions are saved locally; they are not sent to employers.
- The resume analyzer uses simple keyword matching. It is not a trained AI model and its score is not a hiring prediction.
- This starter app does not include user accounts or production-grade authentication.
- Do not deploy with real personal data until security, privacy, authentication, and data handling have been reviewed.

## Requirements

- Python 3.10+
- VS Code (recommended)

## Run locally

### 1. Open the project folder

Open `CareerPilot-AI` in VS Code.

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the app

```bash
python app.py
```

Open this address in your browser:

`http://127.0.0.1:5000`

Stop the server with `Ctrl+C` in the terminal.

## Project structure

```text
CareerPilot-AI/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── jobs.html
│   ├── analyzer.html
│   ├── saved.html
│   ├── apply.html
│   ├── applications.html
│   ├── about.html
│   └── 404.html
├── static/
│   ├── style.css
│   └── script.js
├── uploads/          # temporary PDF processing folder
└── careerpilot.db    # created automatically when app starts
```

## Suggested GitHub description

`Responsive Python Flask career platform with sample job search, saved roles, application tracking, and resume keyword analysis.`

## Suggested resume entry (after you run and understand the project)

**CareerPilot AI — Career & Internship Platform**  
*Python, Flask, SQLite, HTML, CSS, JavaScript*

- Built a responsive career platform to search and filter sample job and internship listings.
- Implemented SQLite-backed saved jobs and a local demo application tracker.
- Developed a resume-to-job-description keyword comparison tool with matched and missing skill indicators.

Only list features you have tested and can explain in an interview.
