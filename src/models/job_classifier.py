
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

PROJECT_ROOT = Path(__file__).resolve().parents[2]
JOBS_FILE = PROJECT_ROOT / "data" / "raw" / "jobs.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"


def classify_domain(title: str) -> str:
    """Crée des catégories initiales à partir du titre du poste."""
    title = str(title).lower()

    if any(word in title for word in [
        "data scientist", "machine learning", "artificial intelligence",
        "ai engineer", "deep learning",
    ]):
        return "Data Science / IA"

    if any(word in title for word in [
        "data analyst", "business intelligence", "bi analyst",
        "analytics", "power bi",
    ]):
        return "Data Analytics / BI"

    if any(word in title for word in [
        "data engineer", "analytics engineer", "data platform",
    ]):
        return "Data Engineering"

    if any(word in title for word in [
        "devops", "site reliability", "cloud engineer",
        "cloud architect",
    ]):
        return "Cloud / DevOps"

    if any(word in title for word in [
        "frontend", "front-end", "backend", "back-end",
        "full stack", "fullstack", "software engineer",
        "software developer", "web developer", "programmer",
        "developer",
    ]):
        return "Développement logiciel"

    if any(word in title for word in [
        "cybersecurity", "security engineer", "information security",
    ]):
        return "Cybersécurité"

    return "Autres métiers"


def train_classifier() -> None:
    if not JOBS_FILE.exists():
        raise FileNotFoundError(f"Fichier introuvable : {JOBS_FILE}")

    # Lire les données sans remplir toutes les colonnes numériques avec du texte.
    df = pd.read_csv(JOBS_FILE)

    for column in ["job_title", "skills"]:
        if column not in df.columns:
            raise ValueError(f"Colonne manquante : {column}")
        df[column] = df[column].fillna("").astype(str)

    df = df[df["job_title"].str.strip() != ""].copy()

    if len(df) < 2:
        print("Il faut au moins deux offres pour entraîner le modèle.")
        return

    df["domain"] = df["job_title"].apply(classify_domain)
    df["text"] = (
        df["job_title"] + " " + df["skills"]
    ).str.strip()

    print("\n===== RÉPARTITION DES CATÉGORIES =====")
    print(df["domain"].value_counts().to_string())

    if df["domain"].nunique() < 2:
        print("\nIl faut au moins deux catégories différentes.")
        print("Collecte davantage d'offres variées puis réessaie.")
        return

    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2),
                max_features=5000,
            ),
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
            ),
        ),
    ])

    model.fit(df["text"], df["domain"])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    model_path = OUTPUT_DIR / "job_classifier.joblib"
    joblib.dump(model, model_path)

    output = df[["job_title", "skills", "domain"]].copy()
    output.to_csv(
        OUTPUT_DIR / "classified_jobs.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print(f"\nOffres utilisées : {len(df)}")
    print(f"Catégories apprises : {df['domain'].nunique()}")
    print(f"Modèle enregistré : {model_path}")
    print(f"Classifications enregistrées : {OUTPUT_DIR / 'classified_jobs.csv'}")


if __name__ == "__main__":
    train_classifier()
