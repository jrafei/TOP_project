from utils import *
from route import *
from node import Node
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
    pt_depart = Node(depart['x'],depart['y'],depart['profit'])
    
    # Extraction du point d'arrivee
    arrivee = points.iloc[-1]
    pt_arrivee = Node(arrivee['x'],arrivee['y'],arrivee['profit'] )
    
    # Extraction des clients
    clients = points.iloc[1:-1]
    listeTournees = []
    liste_noeuds = [pt_depart]
    for _,row in clients.iterrows():
        client = Node(row['x'],row['y'],row['profit'])
        test_time = client.distance_to(pt_depart) + client.distance_to(pt_arrivee)
        if test_time <= tmax :
            liste_noeuds.append(client)
            listeTournees.append(Route([pt_depart,client,pt_arrivee]))
    
    liste_noeuds.append(pt_arrivee)
    
    return listeTournees, liste_noeuds


    """_summary_
        @Parameters:
        points : un dataFrame contenant les coordonnées et les profits des clients avec les coordonnées de départ
        en tete de dataFrame et les coordonnées d'arrivé en fin du dataFrame 
        tmax : float : le temps de parcours maximal
        m : int : le nombre de tournées à retourner
        @Returns:
        list[Tournee] : Retourne une liste de tournées.
        
        @Complexité: O(n^2 * x)) avec x le nombre d'arc ayant un gain positif , pire cas : O(n^4)
    """
def clarke_wright(points, tmax, m) :
    tours,liste_noeuds = init_marguerite(points, tmax) # complexité : O(n) , tours : list[Tournee]  , liste_noeuds : list[node] ,
    
    if (tours == []) :
        print("Aucune tournée a une distance plus petite ou égale au tmax !")
        return None
    
    svl = SavingList(liste_noeuds) #complexité : O(n^2)  type : liste trié par ordre decroissant ( liste de tuple de type Point) , 
    
    while svl != [] :
        
        # prendre le couple de points (arc) ayant le gain max
        couple = svl.pop(0) #Complexité : O(1)
        
        # prendre la tournée ayant comme dernier client le premier point de l'arc
        iRoute = getEndingRoute(couple[0], tours) #Complexité : O(n)
        # prendre la tournée ayant comme premier client le deuxième point de l'arc
        jRoute = getStartingRoute(couple[1], tours) #Complexité : O(n)
        
        # Verifie que couple relie deux tournées différentes,
        # et que la fusion des deux tournées ne dépasse pas le tmax
        verify = validateMergeDriver(iRoute, jRoute, tmax) # Complexité : O(1)
        
        if (verify == True) :
            # Fusion des deux tournées
            iRoute.fusion(jRoute) #Complexité : O(n)
            opt_2(iRoute) # Complexité : O(n^2) 
            #print("fin opt-2")
            tours.remove(jRoute) # Complexité : O(n)
            
            # pour reduire le temps de parcours d'une tournée, on interdit le parcours d'une arete plus qu'une fois 
            x = (couple[1],couple[0]) 
            if x in svl : # Complexité : O(n)
                svl.remove(x) # Complexité : O(n)
    
         
    # prendre les m tounrés ayant le plus de profit
    tours_triee = sorted(tours, key=lambda route: route.profit, reverse=True)
    res = tours_triee[:m] # Complexité : O(n*log(n))
    for route in res :
        opt_2(route) # Complexité : O(n^2)
    return res


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
    tmp1 = iRoute.longueur - iRoute.nodes[-2].distance_to(iRoute.nodes[-1]) 
    # temps de la route j sans le premier arc
    tmp2 = jRoute.longueur - jRoute.nodes[0].distance_to(jRoute.nodes[1])
    t = iRoute.nodes[-2].distance_to(jRoute.nodes[1])
    if (tmp1 + tmp2 + t) > tmax :
        return False
    
    return True



    """_summary_
    calculer le gain de profits et de temps, en donnant plus de poids au profit
    @Parameters:
        liste_noeuds : list[Point] : liste des points
    @returns:
        dict : dictionnaire triée par ordre croissant contenant les clés (tuple de type Point) et les valeurs (float)
    """
def SavingList(liste_noeuds):
    saving_list = {}
    depart = liste_noeuds[0]
    arrivee = liste_noeuds[-1]
    for client1 in liste_noeuds[1:-1] :
        for client2 in liste_noeuds[1:-1] :
            if client1 != client2 :
                gain1 = 2*get_gain_profit(client1,client2) + get_gain_temps(client1,client2,depart,arrivee)
                if gain1 > 0 :
                    saving_list[(client1,client2)] = gain1
                
    sorted_savings = [couple for couple, _ in sorted(saving_list.items(), key=lambda x: x[1], reverse=True)] # Complexité : O(n^2)
    return sorted_savings


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
def get_gain_temps(i,j,depart, arrivee):
    return distance(i,arrivee) + distance(depart,j) - distance(i,j)

def get_gain_profit(i,j):
    return i.profit + j.profit
