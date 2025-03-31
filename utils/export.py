import pandas as pd
import os

def exporter_statistiques_excel(stats, fichier_sortie):
    """
    Exporte toutes les statistiques dans un fichier Excel avec plusieurs feuilles.
    
    Args:
        stats (dict): Dictionnaire contenant les différentes statistiques
        fichier_sortie (str): Chemin du fichier Excel de sortie
    """
    # Créer le dossier de sortie s'il n'existe pas
    dossier_sortie = os.path.dirname(fichier_sortie)
    if dossier_sortie and not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)
        
    # Exportation en Excel avec plusieurs feuilles
    with pd.ExcelWriter(fichier_sortie) as writer:
        # Feuille 1: Statistiques globales
        stats["stats_globales"].to_excel(writer, sheet_name="Stats Globales")
        
        # Feuille 2: Performances annuelles
        stats["perf_annuelle"].to_excel(writer, sheet_name="Performances Annuelles")
        
        # Feuille 3: Performances annuelles relatives
        stats["perf_annuelle_relative"].to_excel(writer, sheet_name="Perf Annuelles Relatives")
        
        # Feuille 4: Données de prix (limité aux 100 premières et 100 dernières lignes pour éviter les fichiers trop volumineux)
        prix = stats["prix"]
        if len(prix) > 200:
            prix_sample = pd.concat([prix.head(100), prix.tail(100)])
            prix_sample.to_excel(writer, sheet_name="Prix Ajustés (échantillon)")
        else:
            prix.to_excel(writer, sheet_name="Prix Ajustés")
    
    print(f"Statistiques exportées dans {fichier_sortie}")
