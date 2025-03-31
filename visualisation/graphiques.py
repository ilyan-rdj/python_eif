import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

def creer_dossier_resultats():
    """Crée un dossier pour stocker les graphiques si nécessaire"""
    if not os.path.exists("resultats"):
        os.makedirs("resultats")

def graphique_performance_cumulee(data, tickers_selection=None, fichier_sortie="resultats/performance_cumulee.png"):
    """
    Crée un graphique de performance cumulée (base 100) pour l'indice et une sélection de titres.
    
    Args:
        data (pandas.DataFrame): DataFrame contenant les prix ajustés
        tickers_selection (list, optional): Liste des tickers à inclure dans le graphique
        fichier_sortie (str): Chemin du fichier de sortie pour le graphique
    """
    # S'assurer que l'indice est inclus
    if tickers_selection is None:
        # Sélectionner l'indice et 9 autres titres aléatoires
        all_tickers = list(data.columns)
        other_tickers = [t for t in all_tickers if t != "^STOXX50E"]
        if len(other_tickers) > 9:
            selected_tickers = np.random.choice(other_tickers, 9, replace=False).tolist()
        else:
            selected_tickers = other_tickers
        
        tickers_selection = ["^STOXX50E"] + selected_tickers
    
    # Sous-ensemble des données pour les titres sélectionnés
    selected_data = data[tickers_selection]
    
    # Normalisation des prix à 100 pour le premier jour
    normalized_data = selected_data / selected_data.iloc[0] * 100
    
    # Création du graphique
    plt.figure(figsize=(14, 8))
    
    # Tracé distinct pour mettre en évidence l'indice
    plt.plot(normalized_data.index, normalized_data["^STOXX50E"], linewidth=3, color='black', label="^STOXX50E")
    
    # Tracé des autres titres
    for ticker in tickers_selection:
        if ticker != "^STOXX50E":
            plt.plot(normalized_data.index, normalized_data[ticker], linewidth=1.5, alpha=0.7, label=ticker)
    
    plt.title('Performance cumulée (base 100) de l\'indice EURO STOXX 50 et titres sélectionnés (2015-2025)', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Performance (base 100)', fontsize=12)
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # Ajout d'une ligne horizontale à 100 pour la référence
    plt.axhline(y=100, color='black', linestyle='--', alpha=0.5)
    
    # Sauvegarde du graphique
    plt.tight_layout()
    plt.savefig(fichier_sortie, dpi=300)
    print(f"Graphique de performance cumulée sauvegardé dans {fichier_sortie}")
    plt.close()

def graphique_distribution_sharpe(stats, fichier_sortie="resultats/distribution_sharpe.png"):
    """
    Crée un histogramme de la distribution des ratios de Sharpe.
    
    Args:
        stats (dict): Dictionnaire contenant les statistiques calculées
        fichier_sortie (str): Chemin du fichier de sortie pour le graphique
    """
    # Récupération des ratios de Sharpe
    sharpe_ratio = stats["stats_globales"]["Sharpe Ratio"]
    
    # Création de l'histogramme
    plt.figure(figsize=(14, 8))
    ax = sns.histplot(sharpe_ratio, bins=10, kde=True, color='steelblue')
    
    # Ajout de lignes verticales pour les valeurs remarquables
    plt.axvline(x=sharpe_ratio.mean(), color='red', linestyle='--', label=f'Moyenne: {sharpe_ratio.mean():.2f}')
    plt.axvline(x=sharpe_ratio.median(), color='green', linestyle='--', label=f'Médiane: {sharpe_ratio.median():.2f}')
    plt.axvline(x=sharpe_ratio["^STOXX50E"], color='purple', linestyle='--', label=f'EURO STOXX 50: {sharpe_ratio["^STOXX50E"]:.2f}')
    
    # Ajout des titres avec les ratios de Sharpe extrêmes
    max_sharpe = sharpe_ratio.idxmax()
    min_sharpe = sharpe_ratio.idxmin()
    plt.axvline(x=sharpe_ratio[max_sharpe], color='gold', linestyle='--', 
                label=f'Max ({max_sharpe}): {sharpe_ratio[max_sharpe]:.2f}')
    plt.axvline(x=sharpe_ratio[min_sharpe], color='black', linestyle='--', 
                label=f'Min ({min_sharpe}): {sharpe_ratio[min_sharpe]:.2f}')
    
    # Amélioration du graphique
    plt.title('Distribution des ratios de Sharpe des composants de l\'EURO STOXX 50 (2015-2025)', fontsize=14)
    plt.xlabel('Ratio de Sharpe', fontsize=12)
    plt.ylabel('Nombre de titres', fontsize=12)
    plt.legend(loc='upper right', fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # Sauvegarde du graphique
    plt.tight_layout()
    plt.savefig(fichier_sortie, dpi=300)
    print(f"Graphique de distribution des ratios de Sharpe sauvegardé dans {fichier_sortie}")
    plt.close()

def afficher_graphiques(data, stats=None, tickers_selection=None):
    """
    Crée tous les graphiques pour l'analyse.
    
    Args:
        data (pandas.DataFrame): DataFrame contenant les prix ajustés
        stats (dict, optional): Dictionnaire contenant les statistiques calculées
        tickers_selection (list, optional): Liste des tickers à inclure dans le graphique de performance
    """
    # Créer le dossier de résultats si nécessaire
    creer_dossier_resultats()
    
    # Si stats n'est pas fourni, le recalculer
    if stats is None:
        # Importer la fonction depuis traitement.analyse
        from traitement.analyse import calculer_statistiques
        stats = calculer_statistiques(data)
    
    # Graphique 1: Performance cumulée
    graphique_performance_cumulee(data, tickers_selection)
    
    # Graphique 2: Distribution des ratios de Sharpe
    graphique_distribution_sharpe(stats)
    
    print("Génération des graphiques terminée")
