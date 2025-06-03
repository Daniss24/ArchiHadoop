import offset
import requests
import time

from config import API_BASE_URL, API_LIMIT


# === RÉCUPÉRATION COMPLÈTE DE L’API BELIB' ===

def extract_data():

    print("Téléchargement des données Belib'...")
    all_bornes = []
    offset = 0

    while True:
        url = f"{API_BASE_URL}?limit={API_LIMIT}&offset={offset}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Erreur API à l'offset {offset} : {e}")
            break
        data = response.json().get("results", [])
        if not data:
                break

        all_bornes.extend(data)
        offset += API_LIMIT
        time.sleep(0.2)  # éviter surcharge du serveur

    print(f"Nombre total de bornes récupérées : {len(all_bornes)}")

    return all_bornes