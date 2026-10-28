
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HEADCOUNT_API_KEY")
API_URL = "https://api.headcountlabs.com/v1/jobs"

if not API_KEY:
    raise ValueError(
        "Clé API introuvable. Vérifie le fichier .env à la racine du projet."
    )

response = requests.get(
    API_URL,
    headers={"Authorization": f"Bearer {API_KEY}"},
    params={
        "currentness": "current",
        "limit": 50,
    },
    timeout=30,
)

print("Code HTTP :", response.status_code)

response.raise_for_status()
data = response.json()

print("\nType de réponse :", type(data).__name__)

if isinstance(data, dict):
    print("Clés principales :", list(data.keys()))

    # Repérer la liste des offres dans la réponse.
    for key, value in data.items():
        if isinstance(value, list):
            print(f"\nListe détectée : {key}")
            print("Nombre d'éléments :", len(value))

            if value and isinstance(value[0], dict):
                print("Champs d'une offre :", list(value[0].keys()))
                print("\nExemple d'offre :")

                for field, content in value[0].items():
                    print(f"  {field}: {str(content)[:180]}")

            break

elif isinstance(data, list):
    print("Nombre d'éléments :", len(data))

    if data and isinstance(data[0], dict):
        print("Champs d'une offre :", list(data[0].keys()))

        for field, content in data[0].items():
            print(f"  {field}: {str(content)[:180]}")
