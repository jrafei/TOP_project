import pandas as pd
from utils import *
import point
from route import *


"""
    initialise la marguerite : nc tours d'un seul client respectant la contrainte de temps
    @Parameters:
    points : dataFrame contenant , le point de départ,  les coordonnées et les profits des clients, et le point d'arrivee
    
    @Returns:
    listeTournees: Retourne une liste de tournées.
    
    @Complexité: O(n)
"""
def init_marguerite(points,tmax) : 
    
    # Extraction du point de départ
    depart = points.iloc[0] 
    pt_depart = point.Point(depart['x'],depart['y'],depart['profit'],True,False)
    
    # Extraction du point d'arrivee
    arrivee = points.iloc[-1]
    pt_arrivee = point.Point(arrivee['x'],arrivee['y'],arrivee['profit'], False, True )
    
    # Extraction des clients
    clients = points.iloc[1:-1]
    listeTournees = []
    for i in range(len(clients)) :
        client = point.Point(clients.iloc[i]['x'],clients.iloc[i]['y'],clients.iloc[i]['profit'],False,False)
        test_time = client.distance_to(pt_depart) + client.distance_to(pt_arrivee)
        if test_time <= tmax :
            listeTournees.append(Route([(pt_depart,client),(client,pt_arrivee)]))
        
    return listeTournees 


    """_summary_
        @Parameters:
        top : un dictionnaire contenant les clés 'n', 'm', 'tmax' avec leurs valeurs respectives,
        et un dataFrame 'points' contenant les coordonnées et les profits des clients avec les coordonnées de départ
        en tete de dataFrame et les coordonnées d'arrivé en fin du dataFrame 
        @Returns:
        list[Tournee] : Retourne une liste de tournées.
        
        @Complexité: O(n^2)
    """
def clarke_wright(top):
    tours = init_marguerite(top['points'], top['tmax']) # type : list[Tournee]  , complexité : O(n)
    
    if (tours == []) :
        print("Aucune tournée a une distance plus petite ou égale au tmax !")
        return None
    
    svl = SavingList(tours) # type : dictionnaire (clé : tuple de type Point, valeur : float) , complexité : O(n^2)
    
    while svl != {} :
        
        # prendre le couple de points (arc) ayant le gain max
        couple = max(svl, key=svl.get)
        
        # prendre la tournée ayant comme dernier client le premier point de l'arc
        iRoute = getEndingRoute(couple[0], tours) #Complexité : O(n)
        # prendre la tournée ayant comme premier client le deuxième point de l'arc
        jRoute = getStartingRoute(couple[1], tours) #Complexité : O(n)
        
        # Verifie que couple relie deux tournées différentes, que i est le dernier client de t1 et que j est le premier client de t2
        # et que la fusion des deux tournées ne dépasse pas le tmax
        verify = validateMergeDriver(iRoute, jRoute, top['tmax']) #@Complexité : O(1)
        
        if (verify == True) :
            # Fusion des deux tournées
            fusion(iRoute, jRoute)
            opt_2(iRoute) # Complexité : O(n^2)
            tours.remove(jRoute)
            # Suppression des arcs de la saving list
            # Mise à jour de la saving list
            #updateSavingList(svl, tours)
    
        del svl[couple]
    
    # prendre les m tounrés ayant le plus de profit
    tours_triee = sorted(tours, key=lambda route: route.profit, reverse=True)
    
    return tours_triee[:top['m']]


    """_summary_
    Verifie que les deux tournées sont différentes, que le temps de parcours de leurs fusion est inférieur au tmax
    @Parameters:
        iRoute : Tournee : la tournée ayant comme dernier client le premier point de l'arc
        jRoute : Tournee : la tournée ayant comme premier client le deuxième point de l'arc
        tmax : float : le temps de parcours maximal
    @Returns:
        bool : True si les deux tournées sont différentes, que le temps de parcours de leurs fusion est inférieur au tmax
    """
def validateMergeDriver(iRoute, jRoute, tmax) :
    if iRoute == None or jRoute == None or iRoute == jRoute :
        return False
    
    # temps de la route i sans le dernier arc
    tmp1 = iRoute.longueur - iRoute.arcs[-1][0].distance_to(iRoute.arcs[-1][1]) 
    # temps de la route j sans le premier arc
    tmp2 = jRoute.longueur - jRoute.arcs[0][0].distance_to(jRoute.arcs[0][1])
    t = iRoute.arcs[-1][0].distance_to(jRoute.arcs[0][1])
    if (tmp1 + tmp2 + t) > tmax :
        return False
    
    return True


"""
    @Parameters:
    iRoute : Route : la tournée ayant comme dernier client le premier point de l'arc
    jRoute : Route : la tournée ayant comme premier client le deuxième point de l'arc
    @Returns:
    None
"""
def fusion(iRoute, jRoute):
    #Creer un nouveau arc qui relie le dernier client de la tournée i au premier client de la tournée j
    arc1 = (iRoute.arcs[-1][0], jRoute.arcs[0][1])
    #Remplacer le dernier arc de la tournée i par le nouveau arc
    iRoute.arcs[-1] = arc1
    #Coller les arcs de la tournée j à la fin de la tournée i sauf le premier arc
    iRoute.arcs.extend(jRoute.arcs[1:])
    #Mettre à jour la longueur et le profit de la tournée i
    iRoute.longueur = iRoute.calculer_longueur()
    #Mettre à jour la longueur et le profit de la tournée i
    iRoute.profit = iRoute.profit + jRoute.profit
    
    return None

    """_summary_
    calculer le gain de temps pour chaque arc
    @Parameters:
        routes : list[Tournee] : liste des tournées
    @returns:
        dict : dictionnaire contenant les clés (tuple de type Point) et les valeurs (float)
    """
def SavingList(routes):
    liste_points = getSetPoints(routes)
    saving_list = {}
    depart = routes[0].arcs[0][0]
    arrivee = routes[0].arcs[-1][1]
    for client1 in liste_points :
        for client2 in liste_points :
            if client1 != client2 :
                gain1 = get_gain(client1,client2,depart,arrivee)
                saving_list[(client1,client2)] = gain1
                gain2 = get_gain(client2,client1,depart,arrivee)
                saving_list[(client2,client1)] = gain2
    
    return saving_list


    """_summary_
    calcule le gain de temps si on fusionne deux tournées
    @Parameters:
        i : Point : le dernier client de t1 
        j : Point : le premier client de t2
        depart : Point : le point de départ
        arrivee : Point : le point d'arrivée
    @Returns:
        float : le gain de temps si on fusionne t1 et t2
    """
def get_gain(i,j,depart, arrivee):
    return distance(i,arrivee) + distance(depart,j) - distance(i,j)