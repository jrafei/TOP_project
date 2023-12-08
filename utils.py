from time import sleep
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from route import *

"""_summary_
    Lit un fichier text et extrait des informations spécifiques dans un dictionnaire.
        
    Parameters:
    chemin_du_fichier (str) : Le chemin complet du fichier texte à lire.
        
    Returns:
    dict: Un dictionnaire contenant les clés 'n' (nombre de sommets), 'm' (nombre de tournées maximale), 'tmax' (temps limite d'une tournée) 
    avec leurs valeurs respectives, et un dataFrame 'points' contenant les coordonnées et les profits des clients avec les coordonnées de départ
    en tete de dataFrame et les coordonnées d'arrivé en fin du dataFrame 
"""
def read_file(chemin_du_fichier):
    # Initialiser un dictionnaire pour contenir les variables
    data_structure = {}

    # Lire les valeurs de n, m et tmax
    try :
        with open(chemin_du_fichier, 'r') as file:
            data_structure['n'] = int(file.readline().split()[1]) # nombre de sommets
            data_structure['m'] = int(file.readline().split()[1]) # nombre de vehicules
            data_structure['tmax'] = float(file.readline().split()[1]) # Temps de parcours limite 

    except FileNotFoundError:
        print("Le fichier n'existe pas !")
        return None
    
    # Lire le reste du fichier dans un DataFrame
    df = pd.read_csv(chemin_du_fichier, skiprows=3, delim_whitespace=True, names=['x', 'y', 'profit'])

    data_structure['points'] = df


    return data_structure


def distance(point1, point2):
    return (((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2) ** 0.5).round(2)
     

    """_summary_
    Calcule la somme des profits de toutes les tournées.
    @Parameters:
        routes (list[Route]) : liste des tournees
    @Returns:
        float : la somme des profits de toutes les tournées
    """
def sum_tournees_profit(routes):
    profit = 0
    for route in routes:
        profit += route.profit
    return profit



"""_summary_
    Applique l'heuristique opt-2 sur une tournée
    @Parameters:
    tournee (Route) : tournée sur laquelle on applique l'heuristique opt-2
    choix de la permutation : la meilleur permutation qui ameliore la tournée
    @Returns:
    void
    """
def opt_2(route):
    improved = True
    noeuds = route.nodes
    
    current_iteration = 0
    while improved :  
        current_iteration += 1
        imin = -1
        jmin = -1
        deltamin = 1000#float('inf') 
        for i in range(0, len(noeuds) - 3):
            for j in range(i + 2, len(noeuds)-1):
                x = noeuds[i]
                v = noeuds[j]
                u = noeuds[i+1]
                y = noeuds[j+1]
                
                # si l'arc (v,y) et (x,u) sont contigusdans la tournée et contigus
                if (x.equal(y)):
                    continue
                delta = x.distance_to(v) + u.distance_to(y) - x.distance_to(u) - v.distance_to(y)
                
                #print(x.distance_to(v), " " , u.distance_to(y), " " ,  x.distance_to(u), " " ,  v.distance_to(y))
                
                if delta < deltamin :
                    deltamin = delta
                    imin = i
                    jmin = j
                    
        deltamin = round(deltamin,2)
        
        if deltamin < 0 and imin != -1 and jmin != -1:
            #print("imin = ", imin, " jmin = ", jmin, " delta = ", deltamin) 
            #print("noeud imin = ",noeuds[imin], "  noeud jmin ", noeuds[jmin]) 
            new_nodes = noeuds[:imin+1] + noeuds[jmin:imin:-1] + noeuds[jmin+1:]
            route.nodes = new_nodes
            noeuds = route.nodes
            #route.print_nodes()
            #printNodes(noeuds)
            #sleep(1)
            
            improved = True
        else :
            improved = False
      
    return route   


def printNodes(nodes):
    for node in nodes :
        print(node)
    print("================================== FIN ======================")
    return None
"""_summary_
    Applique l'heuristique opt-2 sur une tournée
    choix de la permutation : la première permutation qui améliore la tournée
    @Parameters:
    tournee (Route) : tournée sur laquelle on applique l'heuristique opt-2
    @Returns:
    void
    """
def opt_2_premier(route):
    improved = True
    noeuds = route.nodes
    
    while improved:
        improved = False
        imin = -1
        jmin = -1
        #deltamin = float('inf')  # Initialiser deltamin à l'infini
        for i in range(0, len(noeuds) - 3):
            for j in range(i + 2, len(noeuds)-1):
                x = noeuds[i]
                v = noeuds[j]
                u = noeuds[i+1]
                y = noeuds[j+1]
                delta = x.distance_to(v) + u.distance_to(y) - x.distance_to(u) - v.distance_to(y)
                if delta < 0 :
                    #deltamin = delta
                    imin = i
                    jmin = j
                    new_nodes = noeuds[:imin+1] + noeuds[jmin:imin+2:-1] + noeuds[jmin+1:]
                    route.nodes = new_nodes
                    improved = True
        
    return route         





    """_summary_
    cherche la tournée ayant comme dernier client le point lastClient
    @Parameters:
        lastClient : Point : le dernier client de la tournée
        tours : list[Route] : liste des tournées
    @returns:
        Tournee : la tournée ayant comme dernier client le point lastClient
    """
def getEndingRoute(lastClient, tours) :
    for tournee in tours :
        if tournee.nodes[-2] == lastClient :
            return tournee
    return None


    """_summary_
    cherche la tournée ayant comme premier client le point firstClient
    @Parameters:
        firstClient : Point : le premier client de la tournée
        tours : list[Route] : liste des tournées
    @returns:
        Tournee : la tournée ayant comme premier client le point firstClient
    """
def getStartingRoute(firstClient, tours) :
    for tournee in tours :
        if tournee.nodes[1] == firstClient :
            return tournee
    return None


def print_plot(routes, points_df):
    # Extraire les coordonnées x et y pour tous les points
    x_points = points_df['x']
    y_points = points_df['y']

    # Tracer tous les points
    plt.scatter(x_points, y_points, color='blue', label='Points')

    # Générer une palette de couleurs
    colors = plt.cm.viridis(np.linspace(0, 1, len(routes)))

    # Pour chaque route, tracer la trajectoire avec une couleur unique
    for route, color in zip(routes, colors):
        # Assurez-vous que route.nodes contient des objets avec des attributs x et y
        x = [node.x for node in route.nodes]
        y = [node.y for node in route.nodes]

        # Tracer la trajectoire de la route
        plt.plot(x, y, marker='o', linestyle='--', color=color)

    # Marquer le point de départ et d'arrivée avec des marqueurs spécifiques
    plt.scatter(points_df['x'].iloc[0], points_df['y'].iloc[0], color='red', marker='s', edgecolor='black', label='Départ', s=100)
    plt.scatter(points_df['x'].iloc[-1], points_df['y'].iloc[-1], color='green', marker='s', edgecolor='black', label='Arrivée', s=100)

    # Ajouter des titres et des étiquettes
    plt.title("Affichage des Tournées")
    plt.xlabel("Coordonnée X")
    plt.ylabel("Coordonnée Y")
    plt.legend()

    # Afficher le graphique
    plt.show()



        