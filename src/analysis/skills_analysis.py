
from collections import Counter
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
JOBS_FILE = PROJECT_ROOT / "data" / "raw" / "jobs.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "skills_analysis.csv"


def analyze_skills() -> pd.DataFrame:
    """Analyse la fréquence des compétences dans les offres."""
    if not JOBS_FILE.exists():
        raise FileNotFoundError(f"Fichier introuvable : {JOBS_FILE}")

    df = pd.read_csv(JOBS_FILE)

    if "skills" not in df.columns:
        raise ValueError("La colonne 'skills' est absente du CSV.")

    counter = Counter()

    for skills in df["skills"].dropna():
        for skill in str(skills).split(","):
            skill = skill.strip()
            if skill:
                counter[skill] += 1

    result = pd.DataFrame(
        counter.most_common(),
        columns=["skill", "job_count"],
    )

    if not result.empty:
        result["percentage"] = (
            result["job_count"] / len(df) * 100
        ).round(2)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print("\n===== ANALYSE DES COMPÉTENCES =====")
    print(f"Nombre d'offres analysées : {len(df)}")
    print(f"Nombre de compétences distinctes : {len(result)}")

    if not result.empty:
        print("\nCompétences les plus fréquentes :")
        print(result.head(15).to_string(index=False))

    print(f"\nRésultats enregistrés dans : {OUTPUT_FILE}")
    return result


if __name__ == "__main__":
    analyze_skills()
