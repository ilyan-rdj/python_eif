import os
import pandas as pd
import numpy as np

def calculer_beta(data, save_path):
    """
    Calcule le beta de chaque titre par rapport à l'indice et exporte les résultats en Excel.
    
    Args:
        data (pandas.DataFrame): DataFrame des prix ajustés nettoyés.
        save_path (str): Chemin où enregistrer le fichier Excel.
    
    Returns:
        pandas.DataFrame: Tableau des bêtas calculés.
    """
    print("Calcul des bêtas...")
    
    # Calcul des rendements quotidiens
    returns = data.pct_change().dropna()
    
    # Vérifier si l'indice est présent
    if "^STOXX50E" not in returns.columns:
        raise ValueError("L'indice '^STOXX50E' n'est pas dans les données.")
    
    # Rendements de l'indice
    index_returns = returns["^STOXX50E"]
    
    betas = {}
    for ticker in returns.columns:
        if ticker != "^STOXX50E":
            covariance = np.cov(returns[ticker], index_returns)[0, 1]
            variance_index = np.var(index_returns)
            betas[ticker] = covariance / variance_index if variance_index != 0 else np.nan
    
    # Convertir en DataFrame
    beta_df = pd.DataFrame(list(betas.items()), columns=["Titre", "Beta"])
    beta_df.set_index("Titre", inplace=True)
    
    # Trouver le titre avec le plus gros et le plus faible beta
    max_beta_ticker = beta_df["Beta"].idxmax()
    min_beta_ticker = beta_df["Beta"].idxmin()
    
    print(f"Titre avec le plus grand beta : {max_beta_ticker} ({beta_df.loc[max_beta_ticker, 'Beta']:.2f})")
    print(f"Titre avec le plus petit beta : {min_beta_ticker} ({beta_df.loc[min_beta_ticker, 'Beta']:.2f})")
    
    # Sauvegarde en Excel
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    beta_df.to_excel(save_path)
    print(f"Résultats enregistrés dans {save_path}")
    
    return beta_df
