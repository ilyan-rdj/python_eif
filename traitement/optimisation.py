import numpy as np
import pandas as pd
import scipy.optimize as sco
from traitement.analyse import calculer_statistiques
from visualisation.graphiques import graphique_performance_cumulee
from utils.export import exporter_statistiques_excel

def selectionner_meilleurs_titres(df_stats, n=10):
    """Sélectionne les n meilleurs titres selon le ratio de Sharpe."""
    # Accéder au DataFrame des statistiques globales
    df_sharpe = df_stats['stats_globales']
    # Ajuster pour utiliser la colonne 'Sharpe Ratio' au lieu de 'Sharpe'
    meilleurs_titres = df_sharpe.nlargest(n, 'Sharpe Ratio').index.values
    return meilleurs_titres

def optimiser_portefeuille(rendements, cov_matrix, poids_min=0.01, contrainte=True):
    """Optimise les pondérations du portefeuille pour maximiser le Sharpe Ratio, avec un poids minimum par actif si contrainte=True."""
    nb_actifs = len(rendements)
    
    def sharpe_ratio(weights):
        port_return = np.sum(weights * rendements)
        port_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        # Éviter la division par zéro
        if port_volatility < 1e-8:  # Seuil numérique plus sûr
            return 0
        return -port_return / port_volatility  # On minimise donc on met un "-"
    
    # Contraintes : somme des poids = 1
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    
    # Si contrainte est activée, on impose un poids minimum pour chaque actif
    if contrainte:
        bounds = tuple((poids_min, 1) for _ in range(nb_actifs))  # Poids entre 0.01 et 1
    else:
        bounds = tuple((0, 1) for _ in range(nb_actifs))  # Poids entre 0 et 1, sans contrainte de poids minimum
    
    # Répartition initiale uniforme
    init_guess = nb_actifs * [1. / nb_actifs]  # Répartition initiale uniforme
    
    # Optimisation
    opt_result = sco.minimize(sharpe_ratio, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    
    return opt_result.x if opt_result.success else None

def executer_optimisation(df_rendements):
    """Exécute toutes les étapes de l'optimisation et exporte les résultats."""
    # Calculer les statistiques, qui retourne un dictionnaire
    df_stats = calculer_statistiques(df_rendements)
    
    # Identifier l'indice (STOXX50E) pour référence ultérieure
    indice = None
    for col in df_rendements.columns:
        if "^STOXX50E" in col:
            indice = col
            break
    
    # Sélection des meilleurs titres en utilisant les statistiques calculées
    meilleurs_titres = selectionner_meilleurs_titres(df_stats, n=10)
    
    # Filtrer les rendements pour les meilleurs titres
    df_rendements_selection = df_rendements[meilleurs_titres]
    
    # Optimisation sans contrainte (poids libres, y compris proches de 0)
    rendements_moyens = df_rendements_selection.mean()
    cov_matrix = df_rendements_selection.cov()
    
    # Optimisation sans contrainte (sans contraintes sur les poids)
    poids_optimaux_sans_contrainte = optimiser_portefeuille(rendements_moyens, cov_matrix, contrainte=False)
    
    # Optimisation avec contrainte de poids minimum (avec contrainte de poids minimum)
    poids_optimaux_avec_contrainte = optimiser_portefeuille(rendements_moyens, cov_matrix, poids_min=0.01)
    
    if poids_optimaux_sans_contrainte is None:
        print("L'optimisation sans contrainte n'a pas réussi. Utilisation de poids égaux.")
        poids_optimaux_sans_contrainte = np.array([1/len(meilleurs_titres)] * len(meilleurs_titres))
    
    if poids_optimaux_avec_contrainte is None:
        print("L'optimisation avec contrainte n'a pas réussi. Utilisation de poids égaux.")
        poids_optimaux_avec_contrainte = np.array([1/len(meilleurs_titres)] * len(meilleurs_titres))
    
    # Création des DataFrames des résultats avec les bons indices
    df_resultats_sans_contrainte = pd.DataFrame({
        'Poids Optimaux': poids_optimaux_sans_contrainte
    }, index=meilleurs_titres)
    
    df_resultats_avec_contrainte = pd.DataFrame({
        'Poids Optimaux': poids_optimaux_avec_contrainte
    }, index=meilleurs_titres)
    
    # Calcul des performances du portefeuille optimisé sans contrainte
    portfolio_returns_sans_contrainte = (df_rendements_selection * poids_optimaux_sans_contrainte).sum(axis=1)
    prix_portfolio_sans_contrainte = (1 + portfolio_returns_sans_contrainte).cumprod()
    prix_portfolio_sans_contrainte = prix_portfolio_sans_contrainte / prix_portfolio_sans_contrainte.iloc[0]
    
    # Calcul des performances du portefeuille optimisé avec contrainte
    portfolio_returns_avec_contrainte = (df_rendements_selection * poids_optimaux_avec_contrainte).sum(axis=1)
    prix_portfolio_avec_contrainte = (1 + portfolio_returns_avec_contrainte).cumprod()
    prix_portfolio_avec_contrainte = prix_portfolio_avec_contrainte / prix_portfolio_avec_contrainte.iloc[0]
    
    # Créer un DataFrame pour stocker les prix des portefeuilles optimisés
    df_portfolio_sans_contrainte = pd.DataFrame(prix_portfolio_sans_contrainte, columns=['Portfolio_Optimise_Sans_Contrainte'])
    df_portfolio_avec_contrainte = pd.DataFrame(prix_portfolio_avec_contrainte, columns=['Portfolio_Optimise_Avec_Contrainte'])
    
    # Si l'indice est disponible, ajouter également sa performance
    if indice is not None:
        df_portfolio_sans_contrainte[indice] = df_stats['prix'][indice] / df_stats['prix'][indice].iloc[0]
        df_portfolio_avec_contrainte[indice] = df_stats['prix'][indice] / df_stats['prix'][indice].iloc[0]
    
    # Appeler la fonction graphique_performance_cumulee avec les titres à afficher
    titres_a_afficher = ['Portfolio_Optimise_Sans_Contrainte', 'Portfolio_Optimise_Avec_Contrainte']
    if indice is not None:
        titres_a_afficher.append(indice)
    
    # Calcul des statistiques pour chaque portefeuille
    def calculer_stats(portfolio_returns, prefix):
        nb_years = (df_rendements.index[-1] - df_rendements.index[0]).days / 365.25
        perf_totale = portfolio_returns.iloc[-1] - 1
        perf_annualisee = (1 + perf_totale) ** (1 / nb_years) - 1
        vol_annualisee = portfolio_returns.std() * np.sqrt(252)
        sharpe_ratio = perf_annualisee / vol_annualisee
        
        # Calcul du beta par rapport à l'indice
        beta = None
        if indice is not None:
            cov_with_index = portfolio_returns.cov(df_rendements[indice])
            var_index = df_rendements[indice].var()
            beta = cov_with_index / var_index
        
        return pd.DataFrame({
            f'Performance Totale {prefix}': [perf_totale],
            f'Performance Annualisée {prefix}': [perf_annualisee],
            f'Volatilité Annualisée {prefix}': [vol_annualisee],
            f'Sharpe Ratio {prefix}': [sharpe_ratio],
            f'Beta (vs Indice) {prefix}': [beta if beta is not None else np.nan]
        }, index=[f'Portefeuille Optimisé {prefix}'])

    stats_sans_contrainte = calculer_stats(portfolio_returns_sans_contrainte, 'Sans Contrainte')
    stats_avec_contrainte = calculer_stats(portfolio_returns_avec_contrainte, 'Avec Contrainte')
    
    # Afficher les compositions des portefeuilles
    print("\nComposition du portefeuille optimisé sans contrainte:")
    print(df_resultats_sans_contrainte)
    
    print("\nComposition du portefeuille optimisé avec contrainte:")
    print(df_resultats_avec_contrainte)
    
    # Export des résultats dans un fichier Excel
    with pd.ExcelWriter("resultats/portefeuille_optimise.xlsx") as writer:
        # Exporter la composition des portefeuilles
        df_resultats_sans_contrainte.to_excel(writer, sheet_name="Composition_Sans_Contrainte")
        df_resultats_avec_contrainte.to_excel(writer, sheet_name="Composition_Avec_Contrainte")
        # Exporter les statistiques des portefeuilles
        stats_sans_contrainte.to_excel(writer, sheet_name="Statistiques_Sans_Contrainte")
        stats_avec_contrainte.to_excel(writer, sheet_name="Statistiques_Avec_Contrainte")
        # Exporter les performances
        df_portfolio_sans_contrainte.to_excel(writer, sheet_name="Perf_Sans_Contrainte")
        df_portfolio_avec_contrainte.to_excel(writer, sheet_name="Perf_Avec_Contrainte")
    
    # Afficher les résultats
    print("\nStatistiques du portefeuille optimisé sans contrainte:")
    print(stats_sans_contrainte.to_string())
    
    print("\nStatistiques du portefeuille optimisé avec contrainte:")
    print(stats_avec_contrainte.to_string())
    
    return {
        'sans_contrainte': {
            'stats': stats_sans_contrainte,
            'composition': df_resultats_sans_contrainte,
            'prix': df_portfolio_sans_contrainte
        },
        'avec_contrainte': {
            'stats': stats_avec_contrainte,
            'composition': df_resultats_avec_contrainte,
            'prix': df_portfolio_avec_contrainte
        }
    }
