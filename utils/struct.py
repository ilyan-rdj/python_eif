import os

def generer_structure_projet(chemin_racine="."):
    """Génère un fichier texte représentant la structure du projet, en ignorant certains éléments."""
    
    def parcourir_dossier(chemin, prefixe=""):
        """Parcourt récursivement les dossiers et fichiers, avec des filtres."""
        contenu = os.listdir(chemin)
        contenu.sort()
        
        lignes = []
        for i, nom in enumerate(contenu):
            chemin_complet = os.path.join(chemin, nom)
            est_dernier = (i == len(contenu) - 1)
            
            # Ignorer .DS_Store, .venv et __pycache__
            if nom == ".DS_Store" or nom == ".venv" or nom == "__pycache__":
                continue
            
            if os.path.isdir(chemin_complet):
                lignes.append(f"{prefixe}├── {nom}/")
                nouveau_prefixe = prefixe + ("│   " if not est_dernier else "    ")
                lignes.extend(parcourir_dossier(chemin_complet, nouveau_prefixe))
            else:
                lignes.append(f"{prefixe}└── {nom}")
        return lignes
    
    lignes_structure = [os.path.basename(os.path.abspath(chemin_racine)) + "/"] + parcourir_dossier(chemin_racine)
    
    with open("structure_du_code.txt", "w") as f:
        f.write("\n".join(lignes_structure))