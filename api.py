import folium
import webbrowser

import pymongo
import station
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from pymongo import MongoClient
#import time

# === CONFIGURATION ===
MONGO_PORT = 27018
DB_NAME = "ionis_belib_db"
COLLECTION_NAME = "bornes_belib"
RAYON_METRES = 1000  # distance max pour borne affichée

# === CONNEXION À MONGODB ===
client = pymongo.MongoClient(f"mongodb://localhost:{MONGO_PORT}/")
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# === GÉOLOCALISATION DE L’UTILISATEUR ===
geolocator = Nominatim(user_agent="api")
adresse = input("Entrez une adresse ou un code postal : ")

try:
    location = geolocator.geocode(adresse, timeout=10)
except Exception as e:
    print(f"Erreur lors de la géolocalisation : {e}")
    exit()

if not location:
    print("Adresse introuvable.")
    exit()

point_depart = (location.latitude, location.longitude)
print(f"Adresse géolocalisée : {point_depart}")

# === CRÉATION DE LA CARTE FOLIUM ===
m = folium.Map(location=point_depart, zoom_start=15)

# Marqueur pour l'adresse
folium.Marker(
    location=point_depart,
    popup=folium.Popup(f"<b>Départ</b><br>{adresse}", max_width=250),
    icon=folium.Icon(color="blue", icon="home"),
).add_to(m)

# === AFFICHAGE DES BORNES À PROXIMITÉ (1000 m) ===
for borne in collection.find():
    coords = borne.get("coordonneesxy")
    if not coords or not isinstance(coords, dict):
        continue

    try:
        lat = float(coords.get("lat"))
        lon = float(coords.get("lon"))
    except (TypeError, ValueError):
        continue

    station_loc = (lat, lon)
    try:
        distance = geodesic(point_depart, station_loc).meters
    except Exception:
        continue

    if distance <= RAYON_METRES:

        nom = borne.get("id_pdc", "Borne")
        adresse_station = borne.get("adresse_station", "Adresse inconnue")
        etat = borne.get("statut_pdc", "Inconnu")
        nb_points = borne.get("arrondissement", "?")
        description = borne.get("url_description_pdc", "?")

        msg1 = f"Adresse borne : {adresse_station} "
        msg2 = f"Points de charge : {nb_points}"
        msg3 = f"Etat : {etat} "
        msg4 = f"Description : "
        msg5 = f"Distance : {int(distance)} mètres"


        street_view_url = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={coords['lat']},{coords['lon']}"

        msg_html = f"""
                    <div style="font-family: Arial, sans-serif; width: 250px;">
                      <h3 style="color: #4a4a4a; margin-bottom: 10px;">{nom}</h3>
                      <img src="img/belib_logo.png" style="width: 50%; margin-bottom: 10px;">
                      <p style="color: #666; margin: 5px 0;">{msg1}</p>
                      <p style="color: #666; margin: 5px 0;">{msg2}</p>
                      <p style="color: #666; margin: 5px 0;">{msg3}</p>
                     <p style="color: #666; margin: 5px 0;">{msg4}<a href="{description}" target="_blank" style="display: inline-block; background-color: #4285F4; color: white;">ici</a></p>
                      <p style="color: #000; margin: 5px 0; font-weight: bold;">{msg5}</p>
                      <a href="{street_view_url}" target="_blank" style="display: inline-block; background-color: #4285F4; color: white;">Voir en Street View</a>
                    </div>
                    """

#popup_html


        folium.Marker(
            location=station_loc,
            popup=folium.Popup(msg_html , max_width=300),
            icon=folium.Icon(color="green" if etat.lower() == "disponible" else "red", icon="flash"),
        ).add_to(m)

# === SAUVEGARDE DE LA CARTE ===
map_file = "bornes_belib_proximite.html"
m.save(map_file)
webbrowser.open(map_file)

