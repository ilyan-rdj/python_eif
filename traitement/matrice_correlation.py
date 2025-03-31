# traitement/matrice_correlation.py
import pandas as pd

def calculer_matrice_correlation(data):
    """
    Calcule la matrice de corrélation entre les rendements des titres et de l'indice.
    
    Args:
        data (pandas.DataFrame): DataFrame des rendements des titres
    
    Returns:
        pandas.DataFrame: Matrice de corrélation entre les titres et l'indice
    """
    # Calcul des rendements quotidiens
    returns = data.pct_change().dropna()
    
    # Matrice de corrélation
    correlation_matrix = returns.corr()
    
    # Corrélation avec l'indice '^STOXX50E'
    correlation_index = correlation_matrix["^STOXX50E"].drop("^STOXX50E", errors="ignore")
    
    # Titre le moins et le plus corrélé à l'indice
    min_corr_ticker = correlation_index.idxmin()
    max_corr_ticker = correlation_index.idxmax()
    
    # Corrélation moyenne
    mean_corr = correlation_index.mean()
    
    return correlation_matrix, min_corr_ticker, max_corr_ticker, mean_corr
