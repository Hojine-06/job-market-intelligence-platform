
import os
import re
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

API_KEY = os.getenv("HEADCOUNT_API_KEY")
API_URL = "https://api.headcountlabs.com/v1/jobs"
JOBS_FILE = PROJECT_ROOT / "data" / "raw" / "jobs.csv"

SEARCH_TERMS = [
    "data analyst",
    "data engineer",
    "data scientist",
    "python",
    "machine learning",
]

PAGE_SIZE = 100
MAX_PAGES_PER_SEARCH = 3


def get_value(field):
    """Extrait la valeur d'un champ Headcount de type {state, value}."""
    if isinstance(field, dict):
        return field.get("value", "")
    return field if field is not None else ""


def extract_skills(description: str) -> str:
    """Détecte des compétences techniques dans une description."""
    skills = [
        "Python", "SQL", "Power BI", "Tableau", "Excel",
        "AWS", "Azure", "Google Cloud", "Machine Learning",
        "Deep Learning", "Pandas", "NumPy", "Scikit-learn",
        "TensorFlow", "PyTorch", "Spark", "Hadoop", "Airflow",
        "Docker", "Kubernetes", "Java", "JavaScript",
        "TypeScript", "React", "Node.js", "PHP", "Laravel",
        "PostgreSQL", "MySQL", "MongoDB", "ETL",
        "Data Engineering", "Data Analysis", "Statistics", "Git",
    ]

    text = description.lower()
    found = []

    for skill in skills:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"
        if re.search(pattern, text) and skill not in found:
            found.append(skill)

    return ", ".join(found)


def get_location(locations) -> str:
    """Convertit les lieux Headcount en texte lisible."""
    results = []

    for item in locations or []:
        value = get_value(item)

        if isinstance(value, dict):
            parts = [
                value.get("city"),
                value.get("region"),
                value.get("country"),
            ]
            location = ", ".join(str(p) for p in parts if p)
            if location and location not in results:
                results.append(location)

    return " | ".join(results)


def get_posting_url(postings) -> str:
    """Récupère la première URL publique disponible."""
    for posting in postings or []:
        url = get_value(posting.get("posting_url"))
        if isinstance(url, str) and url.startswith(("https://", "http://")):
            return url

    return ""


def normalize_job(job: dict) -> dict:
    """Transforme une offre Headcount dans le format du projet."""
    title = get_value(job.get("title"))
    company = get_value(job.get("employer_name"))
    description = get_value(job.get("description"))
    work_arrangement = get_value(job.get("work_arrangement"))

    postings = job.get("postings") or []
    first_posting = postings[0] if postings else {}

    pay = get_value(first_posting.get("pay"))
    salary = ""

    if isinstance(pay, dict):
        salary = str(pay)

    locations = job.get("locations") or []
    location = get_location(locations)

    country = ""
    for item in locations:
        value = get_value(item)
        if isinstance(value, dict) and value.get("country"):
            country = value["country"]
            break

    return {
        "job_id": job.get("job_id", ""),
        "job_title": title,
        "company": company,
        "location": location,
        "country": country,
        "job_type": "",
        "work_arrangement": work_arrangement,
        "salary": salary,
        "experience": "",
        "skills": extract_skills(description),
        "description": description,
        "date_posted": (
            first_posting.get("source_posted_at")
            or job.get("job_first_seen_at")
            or ""
        ),
        "source": ", ".join(sorted({
            str(posting.get("source"))
            for posting in postings
            if posting.get("source")
        })),
        "job_url": get_posting_url(postings),
    }


def fetch_jobs(search: str) -> list[dict]:
    """Récupère plusieurs pages pour une recherche."""
    if not API_KEY:
        raise ValueError(
            "HEADCOUNT_API_KEY introuvable. Vérifie le fichier .env."
        )

    all_jobs = []
    cursor = None

    for page in range(1, MAX_PAGES_PER_SEARCH + 1):
        params = {
            "q": search,
            "currentness": "current",
            "limit": PAGE_SIZE,
            "description_format": "text",
        }

        if cursor:
            params["cursor"] = cursor

        response = requests.get(
            API_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            params=params,
            timeout=60,
        )
        response.raise_for_status()

        payload = response.json()
        jobs = payload.get("data", [])
        all_jobs.extend(normalize_job(job) for job in jobs)

        print(f"  Page {page} : {len(jobs)} offre(s)")

        cursor = payload.get("next_cursor")
        if not cursor or not jobs:
            break

    return all_jobs


def merge_jobs(new_jobs: list[dict]) -> tuple[int, int]:
    """Fusionne les anciennes et nouvelles offres sans URL dupliquée."""
    JOBS_FILE.parent.mkdir(parents=True, exist_ok=True)

    old_df = (
        pd.read_csv(JOBS_FILE, dtype=str).fillna("")
        if JOBS_FILE.exists()
        else pd.DataFrame()
    )

    new_df = pd.DataFrame(new_jobs)

    if new_df.empty:
        return 0, len(old_df)

    columns = list(dict.fromkeys(
        list(old_df.columns) + list(new_df.columns)
    ))

    old_df = old_df.reindex(columns=columns, fill_value="")
    new_df = new_df.reindex(columns=columns, fill_value="")

    old_count = len(old_df)
    combined = pd.concat([old_df, new_df], ignore_index=True)

    for column in ["job_id", "job_url"]:
        combined[column] = (
            combined[column].fillna("").astype(str).str.strip()
        )

    # Supprimer les URL vides dupliquées uniquement si elles sont réellement
    # renseignées ; garder les offres sans URL.
    has_url = combined["job_url"].ne("")
    with_url = combined[has_url].drop_duplicates(
        subset="job_url", keep="last"
    )
    without_url = combined[~has_url]

    combined = pd.concat(
        [with_url, without_url], ignore_index=True
    )

    # Dédupliquer également les offres sans URL grâce à leur identifiant.
    has_id = combined["job_id"].ne("")
    with_id = combined[has_id].drop_duplicates(
        subset="job_id", keep="last"
    )
    without_id = combined[~has_id]

    combined = pd.concat(
        [with_id, without_id], ignore_index=True
    )

    combined.to_csv(JOBS_FILE, index=False, encoding="utf-8-sig")

    return max(0, len(combined) - old_count), len(combined)

