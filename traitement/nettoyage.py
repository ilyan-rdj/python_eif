import pandas as pd
import yfinance as yf
from datetime import datetime

def telecharger_donnees(tickers, date_debut="2015-01-01", date_fin="2025-01-01", fichier_sortie="data/donnees.csv"):
    """
    Télécharge les données de prix des tickers spécifiés et les enregistre dans un fichier CSV.
    
    Args:
        tickers (list): Liste des tickers Yahoo Finance à télécharger
        date_debut (str): Date de début au format YYYY-MM-DD
        date_fin (str): Date de fin au format YYYY-MM-DD
        fichier_sortie (str): Chemin du fichier CSV de sortie
    
    Returns:
        pandas.DataFrame: DataFrame contenant les prix ajustés
    """
    print(f"Téléchargement des données pour {len(tickers)} tickers...")
    data = yf.download(tickers, start=date_debut, end=date_fin, auto_adjust=False)
    data = data["Adj Close"]
    
    # Sauvegarde des données brutes
    data.to_csv(fichier_sortie)
    print(f"Données sauvegardées dans {fichier_sortie}")
    
    return data

def nettoyer_donnees(df):
    """
    Nettoie les données en gérant les valeurs manquantes.
    
    Args:
        df (pandas.DataFrame): DataFrame à nettoyer
    
    Returns:
        pandas.DataFrame: DataFrame nettoyé
    """
    # Gestion des valeurs manquantes (forward fill puis backward fill)
    df_nettoye = df.ffill().bfill()
    
    print("Nettoyage des données terminé")
    return df_nettoye
