# main.py
import pandas as pd
import os
import numpy as np

from traitement.nettoyage import telecharger_donnees, nettoyer_donnees
from traitement.analyse import calculer_statistiques
from traitement.matrice_correlation import calculer_matrice_correlation
from utils.affichage import afficher_statistiques, afficher_matrice_correlation
from utils.export import exporter_statistiques_excel
from visualisation.graphiques import afficher_graphiques
from traitement.beta_calcul import calculer_beta
from utils.struct import generer_structure_projet
from traitement.optimisation import executer_optimisation

def creer_structure_projet():
    """Crée la structure des dossiers pour le projet"""
    dossiers = ["data", "resultats", "traitement", "utils", "visualisation"]
    
    for dossier in dossiers:
        if not os.path.exists(dossier):
            os.makedirs(dossier)
            if dossier not in ["data", "resultats"]:  # Pas besoin d'__init__.py dans data et resultats
                with open(f"{dossier}/__init__.py", "w") as f:
                    f.write("# Fichier d'initialisation du package") 

def main():
    """Fonction principale exécutant tout le processus d'analyse"""
    # Liste des tickers à analyser
    tickers = [
        "^STOXX50E", "ENEL.MI", "ISP.MI", "BBVA.MC", "G.MI", "INGA.AS", "DTE.DE",
        "ENI.MI", "ALV.DE", "CS.PA", "DBK.DE", "AIR.PA", "ABI.BR", "CA.PA", "IBE.MC",
        "ENGI.PA", "AI.PA", "BN.PA", "BAYN.DE", "EOAN.DE", "FRE.DE", "BMW.DE",
        "BAS.DE", "ASML.AS", "BNP.PA", "DG.PA", "GLE.PA"
    ]
    
    # Télécharger les données si elles n'existent pas déjà
    fichier_donnees = "data/donnees.csv"
    if not os.path.exists(fichier_donnees):
        data = telecharger_donnees(tickers, date_debut="2015-01-01", date_fin="2025-01-01", fichier_sortie=fichier_donnees)
    else:
        print(f"Chargement des données depuis {fichier_donnees}")
        data = pd.read_csv(fichier_donnees, index_col=0, parse_dates=True)
    
    # Nettoyer les données
    df_nettoye = nettoyer_donnees(data)
    
    # Calculer les statistiques
    stats = calculer_statistiques(df_nettoye)
    
    # Afficher les résultats
    afficher_statistiques(stats)
    
    # Exporter les statistiques en Excel
    exporter_statistiques_excel(stats, "resultats/statistiques.xlsx")
    
    # Calcul de la matrice de corrélation
    correlation_matrix, min_corr_ticker, max_corr_ticker, mean_corr = calculer_matrice_correlation(df_nettoye)
    
    # Calcul et affichage de la matrice de corrélation
    correlation_matrix, min_corr_ticker, max_corr_ticker, mean_corr = calculer_matrice_correlation(df_nettoye)
    
    # Sauvegarde de la matrice de corrélation
    os.makedirs("resultats", exist_ok=True)
    save_path_png = os.path.join("resultats", "matrice_correlation.png")
    afficher_matrice_correlation(correlation_matrix, save_path=save_path_png)

    # Afficher les résultats relatifs à l'indice
    print(f"\nTitre le moins corrélé à l'indice : {min_corr_ticker}")
    print(f"Titre le plus corrélé à l'indice : {max_corr_ticker}")
    print(f"Corrélation moyenne : {mean_corr:.4f}")
    
    # Sélection de 10 titres pour le graphique
    # On inclut l'indice, les titres avec les meilleurs/pires performances et quelques autres
    best_performer = stats["stats_globales"]["Performance Totale"].idxmax()
    worst_performer = stats["stats_globales"]["Performance Totale"].idxmin()
    best_sharpe = stats["stats_globales"]["Sharpe Ratio"].idxmax()
    worst_sharpe = stats["stats_globales"]["Sharpe Ratio"].idxmin()
    
    selection = ["^STOXX50E", best_performer, worst_performer, best_sharpe, worst_sharpe]
    
    # Ajouter d'autres titres pour atteindre 10 au total
    autres_titres = [t for t in tickers if t not in selection]
    if len(autres_titres) > 5:
        selection += list(np.random.choice(autres_titres, 5, replace=False))
    else:
        selection += autres_titres
    
    # Afficher les graphiques
    afficher_graphiques(df_nettoye, stats, selection)

    # Définir le chemin du fichier Excel dans "resultats"
    save_path_excel = "resultats/beta_titres.xlsx"

    # Appeler la fonction en lui passant les données nettoyées
    beta_df = calculer_beta(data, save_path_excel)

    # Exécuter l'optimisation du portefeuille
    executer_optimisation(df_nettoye)
    
    print("\nAnalyse complète terminée. Tous les résultats et graphiques sont disponibles dans le dossier 'resultats'")

if __name__ == "__main__":
    # Créer la structure de projet si elle n'existe pas
    creer_structure_projet()
    generer_structure_projet()
    
    # Exécuter le programme principal
    main()
