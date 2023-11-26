
import matplotlib.pyplot as plt
import pandas as pd
import point
import numpy as np

"""_summary_
    Lit un fichier text et extrait des informations spécifiques dans un dictionnaire.
        
    Parameters:
    chemin_du_fichier (str): Le chemin complet du fichier texte à lire.
        
    Returns:
    dict: Un dictionnaire contenant les clés 'n' (nombre de sommets), 'm' (nombre de tournées maximale), 'tmax' (temps limite d'une tournée) 
    avec leurs valeurs respectives, et un dataFrame 'points' contenant les coordonnées et les profits des clients avec les coordonnées de départ
    en tete de dataFrame et les coordonnées d'arrivé en fin du dataFrame 
"""
def read_file(chemin_du_fichier):
    # Initialiser un dictionnaire pour contenir les variables
    data_structure = {}

    # Lire les valeurs de n, m et tmax
    with open(chemin_du_fichier, 'r') as file:
        data_structure['n'] = int(file.readline().split()[1]) # nombre de sommets
        data_structure['m'] = int(file.readline().split()[1]) # nombre de vehicules
        data_structure['tmax'] = float(file.readline().split()[1]) # Temps de parcours limite 

    
    # Lire le reste du fichier dans un DataFrame
    df = pd.read_csv(chemin_du_fichier, skiprows=3, delim_whitespace=True, names=['x', 'y', 'profit'])

    data_structure['points'] = df


    return data_structure



    """_summary_
    Calcule la distance euclidienne entre deux points.

    Parameters:
    point1 (pandas.Series): Un point avec les coordonnées x et y.
    point2 (pandas.Series): Un autre point avec les coordonnées x et y.

    Returns:
    float: La distance euclidienne entre point1 et point2.
    """
def distance(point1, point2):
    return (((point2['x'] - point1['x']) ** 2 + (point2['y'] - point1['y']) ** 2) ** 0.5).round(2)


    """_summary_
    Calcule la somme des profits de toutes les tournées.
    @Parameters:
        tournees (list[Tournee]) : liste des tournées
    @Returns:
        float : la somme des profits de toutes les tournées
    """
def sum_tournees_profit(tournees):
    profit = 0
    for tournee in tournees:
        profit += tournee.total_profit
    return profit


    """_summary_
    Affiche les tournées
    @Parameters:
        tournees (list[Tournee]) : liste des tournées
    @Returns:
        void
    """
def print_tournees(tournees):
    for tournee in tournees:
        print(tournee)
        
        
        
"""
  Affichage des tournées
   Parameters:
        liste_tournee :list[Tournee] 
        points_df : DataFrame contenant les clients, le point de départ et le point d'arrivée.
"""
def print_plot_v1(liste_tournees,points_df) : 
    
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


def print_plot(points_df, liste_tournees):
    # Extraire les coordonnées x et y pour tous les points
    x_points = points_df['x']
    y_points = points_df['y']

    # Tracer tous les points
    plt.scatter(x_points, y_points, color='blue', label='Points')  # Points intermédiaires

    # Pour chaque tournée, tracer la trajectoire
    for tournee in liste_tournees:
        x = tournee.points_df['x']
        y = tournee.points_df['y']

        # Tracer la trajectoire de la tournée
        plt.plot(x, y, marker='o', linestyle='--')  # Points intermédiaires avec ligne pointillée

    # Marquer le point de départ en rouge avec un marqueur spécifique
    plt.scatter(points_df['x'].iloc[0], points_df['y'].iloc[0], color='red', marker='s', edgecolor='black', label='Départ', s=100)

    # Marquer le point d'arrivée en vert avec un marqueur spécifique
    plt.scatter(points_df['x'].iloc[-1], points_df['y'].iloc[-1], color='green', marker='s', edgecolor='black', label='Arrivée', s=100)

    # Ajouter des titres et des étiquettes
    plt.title("Affichage des Tournées")
    plt.xlabel("Coordonnée X")
    plt.ylabel("Coordonnée Y")
    plt.legend()

    # Afficher le graphique
    plt.show()


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


"""
     _summary_ [NON UTILISEE]
    Crée une matrice de distance entre chaque paire de points dans le DataFrame.

    Parameters:
    df (pandas.DataFrame): DataFrame contenant les colonnes 'x', 'y', et 'profit'.

    Returns:
    numpy.ndarray: Une matrice carrée de distance.
    """
def distance_matrix(df):
    n = len(df)
    matrice = np.zeros((n, n))

    for i in range(n):
        for j in range(i + 1, n):
            # Calcul de la distance euclidienne
            distance = np.sqrt((df.iloc[i]['x'] - df.iloc[j]['x'])**2 + 
                               (df.iloc[i]['y'] - df.iloc[j]['y'])**2).round(2)
            matrice[i, j] = matrice[j, i] = distance

    return matrice

