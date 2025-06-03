from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data

def main():
    records = extract_data()
    print("Extract terminé avec succès")
    data = transform_data(records)
    print(f"Nombre d'éléments dans data : {len(data)}")
    print("Exemple de données :")
    print(data[0])  # Affiche le premier élément
    load_data(data)
    print("ETL terminé avec succès")

if __name__ == "__main__":
    main()

