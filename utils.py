import os
import pandas as pd
import data

"""_summary_
        Lit un fichier text et extrait des informations spécifiques dans un dictionnaire.
        
        Parameters:
        chemin_du_fichier (str): Le chemin complet du fichier texte à lire.
        
        Returns:
        dict: Un dictionnaire contenant les clés 'n', 'm', 'tmax' avec leurs valeurs respectives,
        et 'df' qui contient un pandas DataFrame des données restantes dans le fichier.
"""
def lire_fichier_et_creer_structure(chemin_du_fichier):
    # Initialiser un dictionnaire pour contenir les variables
    data_structure = {}

    # Lire les valeurs de n, m et tmax
    with open(chemin_du_fichier, 'r') as file:
        data_structure['n'] = int(file.readline().split()[1])
        data_structure['m'] = int(file.readline().split()[1])
        data_structure['tmax'] = float(file.readline().split()[1])

    # Lire le reste du fichier dans un DataFrame
    data_structure['df'] = pd.read_csv(chemin_du_fichier, skiprows=4, delim_whitespace=True, names=['x', 'y', 'profit'])

    # Renvoyer la structure de données
    return data_structure

script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "data", "p1.2.a.txt")
data = lire_fichier_et_creer_structure(data_path)
print(data)