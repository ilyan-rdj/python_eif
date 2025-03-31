import pandas as pd
import numpy as np

def calculer_statistiques(data):
    """
    Calcule les statistiques pour chaque titre et l'indice.
    
    Args:
        data (pandas.DataFrame): DataFrame des prix ajustés nettoyés
    
    Returns:
        dict: Dictionnaire contenant tous les DataFrames des statistiques calculées
    """
    print("Calcul des statistiques...")
    
    # Calcul des rendements quotidiens
    returns = data.pct_change().dropna()
    
    # Nombre d'années dans la période
    nb_years = (data.index[-1] - data.index[0]).days / 365.25
    
    # Performance totale sur toute la période
    perf_totale = (data.iloc[-1] / data.iloc[0]) - 1
    
    # Performance annualisée sur toute la période
    perf_annualisee = (1 + perf_totale) ** (1 / nb_years) - 1
    
    # Volatilité annualisée sur toute la période
    vol_annualisee = returns.std() * np.sqrt(252)
    
    # Ratio de Sharpe (en supposant un taux sans risque de 0) sur toute la période
    sharpe_ratio = perf_annualisee / vol_annualisee
    
    # Vérifier si l'indice '^STOXX50E' est dans les colonnes
    if "^STOXX50E" in perf_totale.index:
        # Performance relative par rapport à l'indice sur toute la période
        perf_relative = perf_totale - perf_totale["^STOXX50E"]
        
        # Performance annualisée relative par rapport à l'indice
        perf_annualisee_relative = perf_annualisee - perf_annualisee["^STOXX50E"]
    else:
        print("L'indice '^STOXX50E' n'est pas dans les données")
        perf_relative = None
        perf_annualisee_relative = None
    
    # Performances annuelles
    annual_returns = returns.resample('Y').apply(lambda x: (1 + x).prod() - 1)
    annual_returns.index = annual_returns.index.year  # Convertir les dates en années
    
    # Performances annuelles relatives par rapport à l'indice
    if "^STOXX50E" in annual_returns.columns:
        annual_returns_relative = annual_returns.subtract(annual_returns["^STOXX50E"], axis=0)
    else:
        print("L'indice '^STOXX50E' n'est pas dans les rendements annuels")
        annual_returns_relative = None
    
    # Résumé des statistiques globales
    stats_globales = pd.DataFrame({
        "Performance Totale": perf_totale,
        "Performance Annualisée": perf_annualisee,
        "Volatilité Annualisée": vol_annualisee,
        "Sharpe Ratio": sharpe_ratio,
        "Performance Relative": perf_relative,
        "Performance Annualisée Relative": perf_annualisee_relative
    })
    
    # Arrondir pour une meilleure lisibilité
    stats_globales = stats_globales.round(4)
    
    # Retourner toutes les statistiques dans un dictionnaire
    resultat = {
        "prix": data,
        "rendements": returns,
        "stats_globales": stats_globales,
        "perf_annuelle": annual_returns,
        "perf_annuelle_relative": annual_returns_relative
    }
    
    print("Calcul des statistiques terminé")
    return resultat
