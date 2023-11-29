import pandas as pd
from utils import distance
from point import *
from route import *


"""
    initialise la marguerite : nc tours d'un seul client respectant la contrainte de temps
    @Parameters:
    points : dataFrame contenant , le point de départ,  les coordonnées et les profits des clients, et le point d'arrivee
    
    @Returns:
    listeTournees: Retourne une liste de tournées.
"""
def init_marguerite(points,tmax) : 
    
    # Extraction du point de départ
    depart = points.iloc[[0]] # pd.Series
    pt_depart = point.Point(depart['x'],depart['y'],depart['profit'],True,False)
    
    # Extraction du point d'arrivee
    arrivee = points.iloc[[-1]]
    pt_arrivee = point.Point(arrivee['x'],arrivee['y'],arrivee['profit'], False, True )
    
    # Extraction des clients
    clients = points.iloc[1:-1]
    listeTournees = []
    for i in range(len(clients)) :
        client = point.Point(clients.iloc[[i]]['x'],clients.iloc[[i]]['y'],clients.iloc[[i]]['profit'],False,False)
        print(client)
        if client.distance_to(pt_depart) + client.distance_to(pt_arrivee) <= tmax :
            listeTournees.append(Route([pt_depart,client,pt_arrivee]))
        
    return listeTournees 