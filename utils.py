import pandas as pd
import point

"""_summary_
        Lit un fichier text et extrait des informations spécifiques dans un dictionnaire.
        
        Parameters:
        chemin_du_fichier (str): Le chemin complet du fichier texte à lire.
        
        Returns:
        dict: Un dictionnaire contenant les clés 'n', 'm', 'tmax' avec leurs valeurs respectives,
        et une liste des clients de type 'List[Points]'.
"""
def read_file(chemin_du_fichier):
    # Initialiser un dictionnaire pour contenir les variables
    data_structure = {}

    # Lire les valeurs de n, m et tmax
    with open(chemin_du_fichier, 'r') as file:
        data_structure['n'] = int(file.readline().split()[1]) # nombre de clients
        data_structure['m'] = int(file.readline().split()[1]) # nombre de vehicules
        data_structure['tmax'] = float(file.readline().split()[1]) # Temps de parcours limite 

    
    # Lire le reste du fichier dans un DataFrame
    df = pd.read_csv(chemin_du_fichier, skiprows=3, delim_whitespace=True, names=['x', 'y', 'profit'])

    # Créer un objet Point pour le départ avec la première ligne de données
    depart_data = df.iloc[0]
    data_structure['depart'] = point.Point(depart_data['x'], depart_data['y'], depart_data['profit'])

    # Créer un objet Point pour l'arrivée avec la dernière ligne de données
    arrivee_data = df.iloc[-1]
    data_structure['arrivee'] = point.Point(arrivee_data['x'], arrivee_data['y'], arrivee_data['profit'])

    # Supprimer les lignes 'depart' et 'arrivee' du dataframe
    df = df.iloc[1:-1].reset_index(drop=True)
    
    # Ajouter la liste de clients au dictionnaire
    data_structure['clients'] =dataframe_to_points_list(df)
    
    # Renvoyer la structure de données
    return data_structure

"""
    Convertit un DataFrame en une liste d'objets Point.

    Parameters:
        df (pandas.DataFrame): Le DataFrame contenant les données des points, 
                               avec des colonnes 'x', 'y', et 'profit'.

    Returns:
        List[Point]: Une liste d'objets Point.
    """
def dataframe_to_points_list(df):
    points_list = []
    for _, row in df.iterrows():
        pt = point.Point(row['x'], row['y'], row['profit'])
        points_list.append(pt)

    return points_list



