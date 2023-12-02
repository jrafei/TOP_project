from time import sleep
import pandas as pd
from utils import *
import point
from tournee import Tournee

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
    
    # Extraction du point d'arrivee
    arrivee = points.iloc[[-1]]
    
    # Extraction des clients
    clients = points.iloc[1:-1]
    
    return [ Tournee(pd.concat([depart,clients.iloc[[i]], arrivee], ignore_index=True))
                      for i in range(len(clients)) if distance_sans_classe(depart.iloc[0],clients.iloc[i]) + distance_sans_classe(clients.iloc[i],arrivee.iloc[0]) <= tmax]



    """_summary_
        @Parameters:
        top : un dictionnaire contenant les clés 'n', 'm', 'tmax' avec leurs valeurs respectives,
        et un dataFrame 'points' contenant les coordonnées et les profits des clients avec les coordonnées de départ
        en tete de dataFrame et les coordonnées d'arrivé en fin du dataFrame 
    """
def clarke_wright_sans_classe(top):
    
    tours = init_marguerite(top['points'], top['tmax']) # type : list[Tournee] 
    if (tours == []) :
        print("Aucune tournée a une distance plus petite ou égale au tmax !")
        return None
    
    s = tours[0].points_df.iloc[0] # sommet de départ
    t = tours[0].points_df.iloc[-1] # sommet d'arrivée
    
    
    for t1 in tours : # t1 de type Tournee
        ideal_tour2 = None # type : Tournee (tournée ayant le gain max)
        gmax = -10 #initialisation du gain max
        
        y = t1.points_df.iloc[t1.nb_clients] # le dernier client de t1
        
        for t2 in tours : # t2 de type Tournee
            if t1 != t2 :
                u = t2.points_df.iloc[1] # le premier client de t2
                #gain = distance_sans_classe(y,t) + distance_sans_classe(s,u) - distance_sans_classe(y,u) # gain de temps si on fusionne t1 et t2
                gain = get_gain(y,u,s,t)
                tps = calculTempsIfFusion(t1,t2) # temps de parcours si on fusionne t1 et t2

                # Si le temps de parcours est inférieur à tmax et le nouveau gain est supérieur au gain max
                if  tps <= top['tmax'] and gain > gmax :
                    gmax = gain
                    ideal_tour2 = t2

        if (ideal_tour2 != None) :
            fusion(t1,ideal_tour2) # Fusionne t1 et ideal_tour2 
            opt_2(t1) # Applique l'heuristique opt-2 sur t1
            tours.remove(ideal_tour2) # Supprime ideal_tour2 de la liste des tournées
    
    # prendre les m tournés ayant le plus de profit
    tours_triee = sorted(tours, key=lambda tournee: tournee.total_profit, reverse=True)
    
    return tours_triee[:top['m']]

  
  
    
    """_summary_
    Calcule le gain entre deux points i et j
    @Parameters :
    i (dataframe) : représente les coordonnées du dernier client 
    j (dataframe) : représente les coordonnées du premier client 
    depart (dataframe) : représente les coordonnées du point de départ
    arrive (dataframe) : représente les coordonnées du point d'arrivée
    """
def get_gain(i , j , depart, arrivee) : 
    return distance_sans_classe(i,arrivee) + distance_sans_classe(depart,j) - distance_sans_classe(i,j)


    """_summary_
    Calcule le gain entre deux points i et j
    @Parameters :
    p1 (dataframe) : représente les coordonnées du premier client de tournée 1
    d1 (dataframe) : représente les coordonnées du dernier client de tournée 1
    p2 (dataframe) : représente les coordonnées du premier client de tournée 2
    d2 (dataframe) : représente les coordonnées du dernier client de tournée 2
    depart (dataframe) : représente les coordonnées du point de départ
    arrive (dataframe) : représente les coordonnées du point d'arrivée
    @Returns:
    (float, dataframe, dataframe, boolean) : le gain max et les points correspondants (d et p) et 
    un boolean qui indique si d est le dernier client de t1 ou de t2 (True si d est le dernier client de t1, False sinon)
    """
def get_gain_max(p1 , d1 ,p2, d2, depart, arrivee) :
    # Calcul des 2 gains possibles 
    g1 = get_gain(d1,p2,depart,arrivee)
    g2 = get_gain(d2,p1,depart,arrivee)
    
    # Retourner le gain max et les points correspondants
    if (g1 >= g2) :
        return (g1,d1,p2,True)
    
    return (g2,d2,p1,False)

    """_summary_
    Calcule le temps de parcours si on fusionne deux tournées
    @Parameters:
    t1 (Tournee) : tournée 1
    t2 (Tournee) : tournée 2
    @Returns:
    float : le temps de parcours si on fusionne t1 et t2
    """
def calculTempsIfFusion(t1,t2):
    tmp_t1 = t1.longueur - distance_sans_classe(t1.points_df.iloc[t1.nb_clients],t1.points_df.iloc[-1]) # longueur de t1 sans le dernier arc
    tmp_t2 = t2.longueur - distance_sans_classe(t2.points_df.iloc[0],t2.points_df.iloc[1]) # longueur de t2 sans le premier arc
    return (tmp_t1 + tmp_t2).round(2)



    """_summary_
    Fusionne deux tournées
    @Parameters:
    t1 (Tournee) : tournée 1
    t2 (Tournee) : tournée 2
    @Returns:
    void    
    """
def fusion(t1,t2):
    t1.points_df = pd.concat([t1.points_df[0:t1.nb_clients+1],t2.points_df.iloc[1:]], ignore_index=True) # on concatene t2 à t1
    t1.longueur = t1.calculer_longueur()
    t1.total_profit = t1.calculer_total_profit()
    return




    """_summary_
    Applique l'heuristique opt-2 sur une tournée
    @Parameters:
    tournee (Tournee) : tournée sur laquelle on applique l'heuristique opt-2
    @Returns:
    void
    """
def opt_2(tournee):
    points = tournee.points_df
    for i in range(1,len(points)-2): # parcours de tous les arcs de la tournée
        for j in range(i+1,len(points)-1):
            
            if distance_sans_classe(points.iloc[i-1],points.iloc[j]) + distance_sans_classe(points.iloc[i],points.iloc[j+1]) < distance_sans_classe(points.iloc[i-1],points.iloc[i]) + distance_sans_classe(points.iloc[j],points.iloc[j+1]):
                points.iloc[i:j+1] = points.iloc[j:i-1:-1].values
                tournee.longueur = tournee.calculer_longueur()
                #tournee.total_profit = tournee.calculer_total_profit()
                return
            
    return  # si on ne trouve pas d'amélioration, on ne fait rien et on sort de la fonction

