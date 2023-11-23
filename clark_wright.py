import utils
import point
from tournee import Tournee

"""
    initialise la marguerite : nc tours d'un seul client
    Parameters:
    n (int) : Nombre de client disponible
    
    Returns:
    listeTournees: Retourne une liste de tournées.
"""
def init_marguerite(clients, depart, arrivee) : 
    list_tournee = [ Tournee(depart,arrivee, list(x) ) for x in clients ]
    return list_tournee

