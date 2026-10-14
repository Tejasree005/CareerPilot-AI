from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
import re
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "careerpilot.db"
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key-for-production")

JOBS = [
    {"id": 1, "title": "Python Developer Intern", "company": "TechNova Labs", "location": "Remote", "type": "Internship", "skills": ["Python", "Flask", "SQL", "Git"], "stipend": "₹10,000–₹15,000/month", "description": "Build and test Python web applications, write clean code, and work with APIs and databases."},
    {"id": 2, "title": "Data Analyst Intern", "company": "InsightWorks", "location": "Hyderabad", "type": "Internship", "skills": ["Python", "Pandas", "SQL", "Excel", "Matplotlib"], "stipend": "₹12,000–₹18,000/month", "description": "Clean datasets, create reports, and communicate insights using Python and visualization tools."},
    {"id": 3, "title": "Junior Web Developer", "company": "BrightByte", "location": "Visakhapatnam", "type": "Full-time", "skills": ["HTML", "CSS", "JavaScript", "Python", "Flask"], "stipend": "Entry-level role", "description": "Create responsive web pages and connect frontend features to backend services."},
    {"id": 4, "title": "Machine Learning Intern", "company": "ModelSpring", "location": "Remote", "type": "Internship", "skills": ["Python", "Pandas", "Scikit-learn", "NumPy", "Machine Learning"], "stipend": "₹8,000–₹15,000/month", "description": "Prepare data, train baseline machine-learning models, and evaluate model performance."},
    {"id": 5, "title": "Software Engineer Trainee", "company": "CloudNest", "location": "Bengaluru", "type": "Full-time", "skills": ["Python", "Problem Solving", "SQL", "Git", "OOP"], "stipend": "Entry-level role", "description": "Contribute to software features, review code, and collaborate with an engineering team."},
    {"id": 6, "title": "Frontend Developer Intern", "company": "PixelCraft", "location": "Remote", "type": "Internship", "skills": ["HTML", "CSS", "JavaScript", "Responsive Design", "Git"], "stipend": "₹8,000–₹12,000/month", "description": "Build accessible, responsive interfaces and test them across common screen sizes."},
]

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS saved_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL UNIQUE,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                applicant_name TEXT NOT NULL,
                email TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Applied',
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

def get_saved_ids():
    with connect_db() as conn:
        rows = conn.execute("SELECT job_id FROM saved_jobs").fetchall()
    return {row["job_id"] for row in rows}

def extract_pdf_text(file_path):
    if PdfReader is None:
        raise RuntimeError("PDF reading library is missing. Run: pip install -r requirements.txt")
    reader = PdfReader(str(file_path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def analyze_resume(resume_text, job_description):
    common_skills = [
        "python", "java", "c++", "sql", "html", "css", "javascript", "flask",
        "django", "pandas", "numpy", "scikit-learn", "machine learning",
        "data analysis", "excel", "git", "github", "oop", "problem solving",
        "communication", "react", "api", "rest api", "matplotlib", "statistics"
    ]
    resume_lower = resume_text.lower()
    job_lower = job_description.lower()
    job_skills = [skill for skill in common_skills if skill in job_lower]
    resume_skills = [skill for skill in common_skills if skill in resume_lower]
    # If the job description doesn't mention a known skill, compare meaningful words instead.
    if not job_skills:
        stop_words = {"with", "that", "this", "from", "will", "have", "your", "you", "and", "the", "for", "are", "our", "into", "using"}
        job_skills = list(dict.fromkeys(
            word for word in re.findall(r"[a-zA-Z][a-zA-Z+#.-]{2,}", job_lower)
            if word not in stop_words
        ))[:12]
    matched = [skill for skill in job_skills if skill in resume_lower]
    missing = [skill for skill in job_skills if skill not in resume_lower]
    score = round((len(matched) / len(job_skills)) * 100) if job_skills else 0
    return {"score": score, "matched": matched, "missing": missing, "resume_skills": resume_skills}

@app.route("/")
def home():
    saved_ids = get_saved_ids()
    return render_template("index.html", jobs=JOBS[:3], saved_ids=saved_ids)

@app.route("/jobs")
def jobs():
    query = request.args.get("q", "").strip().lower()
    job_type = request.args.get("type", "").strip()
    location = request.args.get("location", "").strip().lower()
    filtered = []
    for job in JOBS:
        searchable = " ".join([job["title"], job["company"], job["location"], job["description"], " ".join(job["skills"])]).lower()
        if query and query not in searchable:
            continue
        if job_type and job["type"] != job_type:
            continue
        if location and location not in job["location"].lower():
            continue
        filtered.append(job)
    return render_template("jobs.html", jobs=filtered, saved_ids=get_saved_ids(), q=query, job_type=job_type, location=location)

@app.post("/save/<int:job_id>")
def save_job(job_id):
    if not any(job["id"] == job_id for job in JOBS):
        flash("Job not found.", "error")
        return redirect(url_for("jobs"))
    with connect_db() as conn:
        exists = conn.execute("SELECT id FROM saved_jobs WHERE job_id = ?", (job_id,)).fetchone()
        if exists:
            conn.execute("DELETE FROM saved_jobs WHERE job_id = ?", (job_id,))
            flash("Job removed from saved jobs.", "success")
        else:
            conn.execute("INSERT INTO saved_jobs (job_id) VALUES (?)", (job_id,))
            flash("Job saved successfully.", "success")
    return redirect(request.referrer or url_for("jobs"))

@app.route("/saved")
def saved():
    saved_ids = get_saved_ids()
    saved_jobs = [job for job in JOBS if job["id"] in saved_ids]
    return render_template("saved.html", jobs=saved_jobs, saved_ids=saved_ids)

@app.route("/apply/<int:job_id>", methods=["GET", "POST"])
def apply(job_id):
    job = next((job for job in JOBS if job["id"] == job_id), None)
    if not job:
        flash("Job not found.", "error")
        return redirect(url_for("jobs"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        if not name or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            flash("Please enter your name and a valid email address.", "error")
            return render_template("apply.html", job=job)
        with connect_db() as conn:
            conn.execute("INSERT INTO applications (job_id, applicant_name, email) VALUES (?, ?, ?)", (job_id, name, email))
        flash("Demo application saved locally. This does not submit an application to a real employer.", "success")
        return redirect(url_for("applications"))
    return render_template("apply.html", job=job)

@app.route("/applications")
def applications():
    with connect_db() as conn:
        rows = conn.execute("""
            SELECT applications.id, applications.applicant_name, applications.email,
                   applications.status, applications.applied_at, applications.job_id
            FROM applications ORDER BY applications.applied_at DESC
        """).fetchall()
    job_map = {job["id"]: job for job in JOBS}
    items = []
    for row in rows:
        item = dict(row)
        item["job"] = job_map.get(item["job_id"], {"title": "Unknown role", "company": ""})
        items.append(item)
    return render_template("applications.html", applications=items)

@app.route("/analyzer", methods=["GET", "POST"])
def analyzer():
    result = None
    if request.method == "POST":
        job_description = request.form.get("job_description", "").strip()
        resume_text = request.form.get("resume_text", "").strip()
        uploaded = request.files.get("resume_pdf")
        if uploaded and uploaded.filename:
            if not uploaded.filename.lower().endswith(".pdf"):
                flash("Please upload a PDF file.", "error")
                return render_template("analyzer.html", result=None)
            safe_name = re.sub(r"[^A-Za-z0-9_.-]", "_", uploaded.filename)
            file_path = UPLOAD_DIR / safe_name
            uploaded.save(file_path)
            try:
                resume_text = extract_pdf_text(file_path)
            except Exception as exc:
                flash(str(exc), "error")
                return render_template("analyzer.html", result=None)
            finally:
                try:
                    file_path.unlink(missing_ok=True)
                except Exception:
                    pass
        if not resume_text or not job_description:
            flash("Paste resume text or upload a PDF, and enter a job description.", "error")
        else:
            result = analyze_resume(resume_text, job_description)
    return render_template("analyzer.html", result=result)

@app.route("/about")
def about():
    return render_template("about.html")

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

init_db()

if __name__ == "__main__":
    app.run(debug=True)
