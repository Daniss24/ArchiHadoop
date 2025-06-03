from pymongo import MongoClient
from config import MONGODB_URI, DB_NAME, COLLECTION_NAME

     # === CONNEXION À MONGODB ===
def load_data(data):
    client = MongoClient(MONGODB_URI)
    try:
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        if not data:
            print("Aucune donnée à insérer.")
            return

    # === MISE À JOUR DE LA BASE DE DONNÉES ===
        collection.delete_many({})
        collection.insert_many(data) #all_bornes data
        print("Base MongoDB mise à jour.")
    except Exception as e:
        print(f"Erreur lors de l'insertion MongoDB : {e}")
    finally:
        client.close()