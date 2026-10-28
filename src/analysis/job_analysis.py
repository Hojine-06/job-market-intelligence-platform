
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
JOBS_FILE = PROJECT_ROOT / "data" / "raw" / "jobs.csv"


def load_jobs() -> pd.DataFrame:
    """Charge les offres d'emploi enregistrées."""
    if not JOBS_FILE.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {JOBS_FILE}"
        )

    return pd.read_csv(JOBS_FILE)


def analyze_jobs() -> None:
    """Affiche un résumé des offres d'emploi."""
    df = load_jobs()

    print("\n===== ANALYSE DU MARCHÉ DE L'EMPLOI =====")
    print(f"Nombre total d'offres : {len(df)}")

    if "job_title" in df.columns:
        print("\nPostes recherchés :")
        print(df["job_title"].value_counts().head(10))

    if "company" in df.columns:
        print("\nEntreprises qui recrutent :")
        print(df["company"].value_counts().head(10))

    if "location" in df.columns:
        print("\nLieux des offres :")
        print(df["location"].value_counts().head(10))

    if "skills" in df.columns:
        skills = (
            df["skills"]
            .dropna()
            .str.split(",")
            .explode()
            .str.strip()
        )

        print("\nCompétences mentionnées :")
        print(skills.value_counts().head(15))


if __name__ == "__main__":
    analyze_jobs()

