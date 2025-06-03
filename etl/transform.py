def transform_data(records):
    transformed = []

    for r in records:
        id_pdc = r.get("id_pdc", "Inconnu")
        etat_pdc = r.get("statut_pdc", "Inconnu")
        date_maj = r.get("last_updated")
        geo = r.get("coordonneesxy") #geo_point_2d
        adresse = r.get("adresse_station", "NC")
        code_insee = r.get("code_insee_commune", "NC")
        arrondissement = r.get("arrondissement", "NC")

        # Vérification que les coordonnées sont disponibles
        if not geo or "lon" not in geo or "lat" not in geo:
            continue

        # Générer un lien vers la description statique de ce PDC
        url_description = (
            "https://parisdata.opendatasoft.com/explore/dataset/"
            "belib-points-de-recharge-pour-vehicules-electriques-donnees-statiques/"
            "table/?q=" + id_pdc
        )

        transformed.append({
            "id_pdc": id_pdc,
            "statut_pdc": etat_pdc,
            "url_description_pdc": url_description,
            "last_updated": date_maj,
            "coordonneesxy": {
                "lon": geo["lon"],
                "lat": geo["lat"]
            },
            "adresse_station": adresse,
            "code_insee_commune": code_insee,
            "arrondissement": arrondissement
        })

    return transformed