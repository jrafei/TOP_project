from matplotlib import pyplot as plt
import pandas as pd
import point

"""_summary_
        Lit un fichier text et extrait des informations spécifiques dans un dictionnaire.
        
        Parameters:
        chemin_du_fichier (str): Le chemin complet du fichier texte à lire.
        
        Returns:
        dict: Un dictionnaire contenant les clés 'n', 'm', 'tmax' avec leurs valeurs respectives,
        et un dataFrame 'points' contenant les coordonnées et les profits des clients avec les coordonnées de départ
        en tete de dataFrame et les coordonnées d'arrivé en fin de la dataFrame 
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

    data_structure['points'] = df


    return data_structure


"""
  Affichage des tournées
   Parameters:
        liste_tournee (list[Tournee])  
"""
def print_plot(liste_tournees) : 
    
    # Pour chaque tournée, tracer la trajectoire
    for tournee in liste_tournees:
        x = tournee.points_df['x']
        y = tournee.points_df['y']

        # Tracer la trajectoire de la tournée
        plt.plot(x, y, marker='o')  # Points intermédiaires

    # Marquer le point de départ en rouge avec un marqueur spécifique
    plt.scatter(liste_tournees[0].points_df['x'].iloc[0], liste_tournees[0].points_df['y'].iloc[0], color='red', marker='s', edgecolor='black', label='Départ', s=100)

    # Marquer le point d'arrivée en vert avec un marqueur spécifique
    plt.scatter(liste_tournees[0].points_df['x'].iloc[-1], liste_tournees[0].points_df['y'].iloc[-1], color='green', marker='s', edgecolor='black', label='Arrivée', s=100)

    # Ajouter des titres et des étiquettes
    plt.title("Affichage des Tournées")
    plt.xlabel("Coordonnée X")
    plt.ylabel("Coordonnée Y")
    plt.legend()

    # Afficher le graphique
    plt.show()



"""
    Calcule la distance euclidienne entre deux points représentés par deux DataFrames.

    Parameters:
    df1 (pandas.DataFrame): DataFrame représentant le premier point.
    df2 (pandas.DataFrame): DataFrame représentant le second point.

    Returns:
    float: La distance euclidienne entre les deux points.
"""
def distance(df1, df2):
    # Extraction des coordonnées x et y
    x1, y1 = df1['x'].iloc[0], df1['y'].iloc[0]
    x2, y2 = df2['x'].iloc[0], df2['y'].iloc[0]

    # Calcul de la distance euclidienne
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return distance


"""
    [NON UTILISEE]
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


