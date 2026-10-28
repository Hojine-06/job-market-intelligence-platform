
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
JOBS_FILE = PROJECT_ROOT / "data" / "raw" / "jobs.csv"


def load_jobs():
    assert JOBS_FILE.exists(), (
        f"Fichier introuvable : {JOBS_FILE}. "
        "Lance d'abord python src/data/fetch_jobs.py"
    )

    df = pd.read_csv(JOBS_FILE)
    df = df.astype(object).where(pd.notna(df), "")
    return df

def test_jobs_file_is_not_empty():
    df = load_jobs()
    assert len(df) > 0, "Le fichier ne contient aucune offre."


def test_required_columns_exist():
    df = load_jobs()

    required_columns = [
        "job_title",
        "company",
        "location",
        "skills",
        "job_url",
    ]

    for column in required_columns:
        assert column in df.columns, f"Colonne manquante : {column}"


def test_job_titles_are_not_empty():
    df = load_jobs()
    assert df["job_title"].astype(str).str.strip().ne("").all(), (
        "Certaines offres n'ont pas de titre."
    )


def test_no_duplicate_job_urls():
    df = load_jobs()

    urls = df["job_url"].astype(str).str.strip()
    urls = urls[urls.ne("")]

    assert not urls.duplicated().any(), (
        "Des offres possèdent des URL dupliquées."
    )


def test_job_urls_are_valid():
    df = load_jobs()

    urls = df["job_url"].astype(str).str.strip()
    urls = urls[urls.ne("")]

    assert urls.str.startswith(("http://", "https://")).all(), (
        "Certaines URL ne commencent pas par http:// ou https://."
    )


def test_skills_column_exists_and_is_readable():
    df = load_jobs()

    assert "skills" in df.columns
    assert df["skills"].notna().all()
