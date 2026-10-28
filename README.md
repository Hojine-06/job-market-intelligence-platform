NEXUS — Plateforme d’intelligence du marché de l’emploi

Présentation

NEXUS est un projet d’analyse de données consacré au marché de l’emploi. Il vise à exploiter les offres d’emploi afin d’identifier les compétences recherchées, d’analyser les tendances de recrutement et de classifier les offres selon leurs caractéristiques.

Le projet combine collecte de données, traitement, analyse, apprentissage automatique et visualisation interactive.

Objectifs

- Collecter et exploiter des données relatives aux offres d’emploi.
- Analyser les métiers et les compétences demandées par les recruteurs.
- Identifier les tendances du marché de l’emploi.
- Développer un modèle de classification des offres.
- Présenter les résultats dans un tableau de bord interactif.

 Fonctionnalités

- Collecte et préparation des données d’emploi.
- Analyse des offres et des compétences.
- Classification des offres à l’aide du machine learning.
- Visualisation des résultats dans un tableau de bord.
- Tests automatisés pour contrôler la qualité des données.

 Technologies utilisées

- Python : traitement et analyse des données.
- Pandas : manipulation des données.
- Scikit-learn : apprentissage automatique.
- Streamlit: tableau de bord interactif, si utilisé dans l’application.
- Pytest : tests automatisés.
- Git et GitHub : gestion de versions et hébergement du code.

Structure du projet

```text
job-market-intelligence-platform/
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   ├── clean/
│   ├── processed/
│   └── external/
├── docs/
├── etl/
├── ml/
├── notebooks/
├── scripts/
├── sql/
├── src/
│   ├── analysis/
│   ├── data/
│   ├── features/
│   └── models/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

 Installation

1. Cloner le dépôt

   bash
git clone https://github.com/Hojine-06/job-market-intelligence-platform.git
cd job-market-intelligence-platform


2. Créer un environnement virtuel

Sous Windows :

   powershell
python -m venv .venv
.venv\Scripts\Activate.ps1


 3. Installer les dépendances

   bash
pip install -r requirements.txt

 Tests

Pour exécuter les tests automatisés :

   bash
python -m pytest -v


Les six tests de validation des données exécutés lors de la vérification initiale ont réussi.

Lancement du tableau de bord

Le point d’entrée du tableau de bord est `dashboard/app.py`.

La commande de lancement dépend du framework effectivement utilisé dans ce fichier. Vérifiez les instructions correspondantes avant de lancer l’application.

Perspectives d’évolution

- Automatiser la collecte et la mise à jour des offres.
- Enrichir l’analyse des compétences et des métiers.
- Améliorer les performances du modèle de classification.
- Ajouter des indicateurs et des visualisations au tableau de bord.
- Développer une architecture de traitement de données plus automatisée.

 Auteur

Hojine Anagonou

Projet personnel de data analytics et de machine learning réalisé dans le cadre d'auto apprentissage.
