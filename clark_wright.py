from time import sleep
import pandas as pd
from utils import distance
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
                      for i in range(len(clients)) if distance(depart.iloc[0],clients.iloc[i]) + distance(clients.iloc[i],arrivee.iloc[0]) <= tmax]



    """_summary_
        @Parameters:
        top : un dictionnaire contenant les clés 'n', 'm', 'tmax' avec leurs valeurs respectives,
        et un dataFrame 'points' contenant les coordonnées et les profits des clients avec les coordonnées de départ
        en tete de dataFrame et les coordonnées d'arrivé en fin du dataFrame 
    """
def clarke_wright(top):
    
    tours = init_marguerite(top['points'], top['tmax']) # type : list[Tournee] 
    if (tours == []) :
        print("Aucune tournée n'a été générée !")
        return None
    test = tours[0].points_df
    s = tours[0].points_df.iloc[0] # sommet de départ
    t = tours[0].points_df.iloc[-1] # sommet d'arrivée
    
    for t1 in tours : # t1 de type Tournee
        ideal_tour2 = None # type : Tournee (tournée ayant le gain max)
        gmax = -10 #initialisation du gain max
        
        y = t1.points_df.iloc[t1.nb_clients] # le dernier client de t1
        
        for t2 in tours : # t2 de type Tournee
            if t1 != t2 :
                u = t2.points_df.iloc[1] # le premier client de t2
                #gain = distance(y,t) + distance(s,u) - distance(y,u) # gain de temps si on fusionne t1 et t2
                gain = gain(y,u,s,t)
                tps = calculTempsIfFusion(t1,t2) # temps de parcours si on fusionne t1 et t2

                # Si le temps de parcours est inférieur à tmax et le nouveau gain est supérieur au gain max
                if  tps <= top['tmax'] and gain > gmax :
                    gmax = gain
                    ideal_tour2 = t2

        if (ideal_tour2 != None) :
            fusion(t1,ideal_tour2) # Fusionne t1 et ideal_tour2 
            opt_2(tours,t1) # Applique l'heuristique opt-2 sur ideal_tour2
            tours.remove(ideal_tour2) # Supprime ideal_tour2 de la liste des tournées
            


    
    # prendre les m tounrés ayant le plus de profit
    tours_triee = sorted(tours, key=lambda tournee: tournee.total_profit, reverse=True)
    
    return tours[:top['m']]
  
  
  
    
    """_summary_
    Calcule le gain entre deux points i et j
    @Parameters :
    i (dataframe) : représente les coordonnées d'un client i
    j (dataframe) : représente les coordonnées d'un client j
    depart (dataframe) : représente les coordonnées du point de départ
    arrive (dataframe) : représente les coordonnées du point d'arrivée
    """
def gain(i , j , depart, arrivee) : 
    return distance(i,arrivee) + distance(depart,j) - distance(i,j)



    """_summary_
    Calcule le temps de parcours si on fusionne deux tournées
    @Parameters:
    t1 (Tournee) : tournée 1
    t2 (Tournee) : tournée 2
    @Returns:
    float : le temps de parcours si on fusionne t1 et t2
    """
def calculTempsIfFusion(t1,t2):
    tmp_t1 = t1.longueur - distance(t1.points_df.iloc[t1.nb_clients],t1.points_df.iloc[-1]) # longueur de t1 sans le dernier arc
    tmp_t2 = t2.longueur - distance(t2.points_df.iloc[0],t2.points_df.iloc[1]) # longueur de t2 sans le premier arc
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


def opt_2(tours,tournee):
    points = tournee.points_df
    for i in range(1,len(points)-2): # parcours de tous les arcs de la tournée
        for j in range(i+1,len(points)-1):
            
            if distance(points.iloc[i-1],points.iloc[j]) + distance(points.iloc[i],points.iloc[j+1]) < distance(points.iloc[i-1],points.iloc[i]) + distance(points.iloc[j],points.iloc[j+1]):
                points.iloc[i:j+1] = points.iloc[j:i-1:-1].values
                tournee.longueur = tournee.calculer_longueur()
                tournee.total_profit = tournee.calculer_total_profit()
                return
            
    return  # si on ne trouve pas d'amélioration, on ne fait rien et on sort de la fonction

    """_summary_
    Parameters : 
    customers [dataframe] : contenant x y profit
    distance_matrix [numpy.ndarray] : Une matrice carrée de distance.
    
    Return : list de triplet trié par ordre croissant de gain
    
def calculate_savings_with_scores(customers: pd.DataFrame, distance_matrix : np.ndarray):
    savings = []
    for i, rowi in customers.iterrows():
        for j, rowj in customers.iterrows():
            if i != j:
                saving = rowi['profit']+  rowj['profit'] - distance_matrix[i][j]  # A REVOIR !!! [TODO]
                savings.append((saving.round(2), i, j))
    return sorted(savings, reverse=True)
"""



def team_orienteering_problem( customers, distance_matrix, max_distance, n):
    # Initialize routes and calculate savings with scores
    #depot = customers.iloc[0]
    #arrivee = customers.iloc[n]
    customers = customers.iloc[1:-1] # les clients 
    #print(customers)
    #sleep(5)
    
    routes = {customer: [0, customer, n-1] for customer in range(1,n)}
    savings = calculate_savings_with_scores(customers, distance_matrix)

    
    # Combine routes with consideration of scores and distance limits
    for saving, i, j in savings:
        route_i = next((route for route in routes.values() if i in route), None) # la première route (s'il y en a) qui inclut un client spécifique.
        route_j = next((route for route in routes.values() if j in route), None)

        if route_i != route_j and route_i[1] == i and route_j[-2] == j:
            combined_route = route_j[:-1] + route_i[1:]
            combined_distance = calculate_route_distance(combined_route, distance_matrix)
            #combined_score = calculate_route_score(combined_route, scores)
            if (combined_distance <= 2.5):
                print("COMBINED DISTANCE : ", combined_distance)
                
            if combined_distance <= max_distance:
                print("COMBINED ROUTE : ", combined_route)
                del routes[i]
                routes[j] = combined_route

    # Iterative improvement
    # ... (possibly rearranging nodes in routes for better score)
    # 
    return list(routes.values())


def calculate_route_distance(route, distance_matrix):
    distance = 0
    for i in range(len(route) - 1):
        #print("i = %d j = %d", route[i],route[i+1] )
        distance += distance_matrix[route[i]][route[i+1]]
    return distance


"""
def calculate_route_score(route, scores):
    return sum(scores[node] for node in route if node != depot)





dict = read_file("./data/Set_32_234/p1.2.a.txt")

df_points = dict['points']
#print(df_points)
dist = distance_matrix(df_points)
#print(dist)
res = calculate_savings_with_scores(df_points,dist)
print(res)

"""


###############################################################""

"""
    [NON UTILISE]
    Calcule le gain entre deux points i et j
    @Parameters :
    i (dataframe) : représente les coordonnées d'un client i 
    j (dataframe) : représente les coordonnées d'un client j 
    depart (dataframe) : 
    arrive (dataframe) :  
"""
def gain(i , j , depart, arrivee) : 
    return distance(i,depart) + distance(depart,j) - distance(j,arrivee)