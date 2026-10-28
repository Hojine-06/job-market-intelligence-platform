
from pathlib import Path

import pandas as pd

# Racine du projet
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def save_jobs(jobs: list[dict], filename: str = "jobs.csv") -> Path:
    """Enregistre une liste d'offres d'emploi au format CSV."""
    output_path = DATA_DIR / filename

    columns = [
        "job_title",
        "company",
        "location",
        "country",
        "job_type",
        "salary",
        "experience",
        "skills",
        "date_posted",
        "source",
        "job_url",
    ]

    df = pd.DataFrame(jobs, columns=columns)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"{len(df)} offre(s) enregistrée(s) dans : {output_path}")
    return output_path


if __name__ == "__main__":
    sample_jobs = [
        {
            "job_title": "Data Analyst",
            "company": "Entreprise exemple",
            "location": "Cotonou",
            "country": "Bénin",
            "job_type": "CDI",
            "salary": None,
            "experience": "Junior",
            "skills": "Python, SQL, Power BI",
            "date_posted": "2026-10-26",
            "source": "test",
            "job_url": "",
        }
    ]

    save_jobs(sample_jobs)
