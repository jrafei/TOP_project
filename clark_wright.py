import pandas as pd
from utils import *
import point
from tournee import Tournee

"""
    initialise la marguerite : nc tours d'un seul client
    @Parameters:
    points : dataFrame contenant , le point de départ en premier,  les coordonnées et les profits des clients, 
    et en dernier le point d'arrivee
    
    @Returns:
    listeTournees: Retourne une liste de tournées.
"""
def init_marguerite(points) : 
    
    # Extraction du point de départ
    depart = points.iloc[[0]]
    
    # Extraction du point d'arrivee
    arrivee = points.iloc[[-1]]
    
    # Extraction des clients
    clients = points.iloc[1:-1]
    
    list_tournee = [ Tournee(pd.concat([depart,clients.iloc[[i]], arrivee], ignore_index=True))
                      for i in range(len(clients))]

    return list_tournee




"""
    Calcule le gain entre deux points i et j
    @Parameters :
    i (dataframe) : représente les coordonnées d'un client i 
    j (dataframe) : représente les coordonnées d'un client j 
    depart (dataframe) : 
    arrive (dataframe) :  
"""
def gain(i , j , depart, arrivee) : 
    return distance(i,depart) + distance(depart,j) - distance(j,arrivee)