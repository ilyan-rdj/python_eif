import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def afficher_statistiques(stats):
    """
    Affiche les statistiques principales dans la console.
    
    Args:
        stats (dict): Dictionnaire contenant les différentes statistiques
    """
    print("\n" + "="*50)
    print("RÉSUMÉ DES STATISTIQUES PRINCIPALES")
    print("="*50)
    
    # Affichage des statistiques globales
    stats_globales = stats["stats_globales"]
    
    # Titres les plus et moins performants
    best_performer = stats_globales["Performance Totale"].idxmax()
    worst_performer = stats_globales["Performance Totale"].idxmin()
    
    # Titres les plus et moins volatils
    most_volatile = stats_globales["Volatilité Annualisée"].idxmax()
    least_volatile = stats_globales["Volatilité Annualisée"].idxmin()
    
    # Meilleur et pire ratio de Sharpe
    best_sharpe = stats_globales["Sharpe Ratio"].idxmax()
    worst_sharpe = stats_globales["Sharpe Ratio"].idxmin()
    
    # Affichage des résultats
    print("\nPerformances:")
    print(f"- Titre le plus performant: {best_performer} ({stats_globales.loc[best_performer, 'Performance Totale']:.2%})")
    print(f"- Titre le moins performant: {worst_performer} ({stats_globales.loc[worst_performer, 'Performance Totale']:.2%})")
    print(f"- Indice EURO STOXX 50: {stats_globales.loc['^STOXX50E', 'Performance Totale']:.2%}")
    
    print("\nVolatilité annualisée:")
    print(f"- Titre le plus volatil: {most_volatile} ({stats_globales.loc[most_volatile, 'Volatilité Annualisée']:.2%})")
    print(f"- Titre le moins volatil: {least_volatile} ({stats_globales.loc[least_volatile, 'Volatilité Annualisée']:.2%})")
    print(f"- Indice EURO STOXX 50: {stats_globales.loc['^STOXX50E', 'Volatilité Annualisée']:.2%}")
    
    print("\nRatio de Sharpe:")
    print(f"- Meilleur ratio de Sharpe: {best_sharpe} ({stats_globales.loc[best_sharpe, 'Sharpe Ratio']:.2f})")
    print(f"- Pire ratio de Sharpe: {worst_sharpe} ({stats_globales.loc[worst_sharpe, 'Sharpe Ratio']:.2f})")
    print(f"- Indice EURO STOXX 50: {stats_globales.loc['^STOXX50E', 'Sharpe Ratio']:.2f}")
    
    print("\n" + "="*50)

# utils/affichage.py
import matplotlib.pyplot as plt
import seaborn as sns
import os

def afficher_matrice_correlation(correlation_matrix, save_path=None):
    """
    Affiche et sauvegarde la matrice de corrélation sous forme de heatmap.

    Args:
        correlation_matrix (pandas.DataFrame): Matrice de corrélation
        save_path (str, optional): Chemin du fichier pour sauvegarder l’image (PNG/PDF)
    """
    plt.figure(figsize=(12, 10))  # Augmenter la taille de la figure
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', cbar=True, 
                linewidths=0.5, annot_kws={"size": 8})  # Réduire la taille des nombres
    plt.xticks(rotation=45, ha='right', fontsize=9)  # Incliner les étiquettes pour éviter les chevauchements
    plt.yticks(fontsize=9)
    plt.title('Matrice de Corrélation des Rendements', fontsize=14)

    # Sauvegarder l'image si un chemin est spécifié
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches='tight', dpi=300)  # Sauvegarde en haute qualité
        print(f"Matrice de corrélation sauvegardée sous {save_path}")

    plt.show()