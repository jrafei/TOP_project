from utils import *
from route import *
from node import Node
from nodeBeam import NodeBeam
from copy import deepcopy


"""
    @Parameters:
        points : un dataFrame contenant les coordonnées et les profits des clients avec les coordonnées de départ
        en tete de dataFrame et les coordonnées d'arrivé en fin du dataFrame 
        tmax : float : le temps de parcours maximal
        m : int : le nombre de tournées à retourner
        @Returns:
        list[Tournee] : Retourne une liste des noeuds.
        
"""
def getNode_respect_time(points,tmax) :     
    # Extraction du point de départ
    depart = points.iloc[0] 
    pt_depart = Node(depart['x'],depart['y'],depart['profit'])
    
    # Extraction du point d'arrivee
    arrivee = points.iloc[-1]
    pt_arrivee = Node(arrivee['x'],arrivee['y'],arrivee['profit'] )
    
    # Extraction des clients
    clients = points.iloc[1:-1]
    liste_noeuds = []
    for _,row in clients.iterrows():
        client = Node(row['x'],row['y'],row['profit'])
        test_time = client.distance_to(pt_depart) + client.distance_to(pt_arrivee)
        if test_time <= tmax :
            liste_noeuds.append(client)
    
    #liste_noeuds.append(pt_arrivee)
    
    return liste_noeuds, pt_depart, pt_arrivee


"""_summary_
    points : list[Node] = listes des clients (pourlesquels leurs tourné marguerite respectent la contrainte de temps)
    tmax : float : le temps de parcours maximal
    m : int : le nombre de tournées à retourner
    beam_width : int : le nombre de noeuds à garder à chaque itération
    @Returns:
    list[NodeBeam] : Retourne une liste de tournées.
"""
def beam(clients,depart, arrive, tmax, m, beam_width) :
    liste_tournee = [] #Type : list[NodeBeam]
    
    b_off = []
    k = 0
    while k<m : # Construction des m tournées
        mu_zero = NodeBeam([depart],clients,0,0) # mu_zero : NodeBeam
        b = [mu_zero] # liste des noeuds à chaque niveau de l'arbre
        l = 0
        bestK = mu_zero 
        
        # creation des noeuds fils des noeuds de b
        while b != [] : # tant que les sommets courants ne sont pas vide
            # creation des noeuds fils de mu respectant la contrainte de temps
            b_off = [] 
            l += 1 # on est dans le niveau suivant de l'arbre
            
            pn = None
            pp = None
            for mu in b :
                pn = (mu.getPneg()) # pn : liste des noeuds non visités sans le dépôt et l'arrivée
                pp = (mu.getPplus()) # pp : liste des noeuds visités avec le dépôt et l'arrivée
                t = mu.getTime() # temps de parcours de pplus (liste des noeuds visités avec le dépôt et SANS [] l'arrivée) 
                p = mu.getProfit()
                for i in range(0,len(pn)) : # rappel : Pneg est une liste des noeuds non visités sans le dépôt et l'arrivée
                    b_off.append(NodeBeam(pp + [pn[i]], pn[:i] + pn[i+1:], p + pn[i].profit, t + pn[i].distance_to(pp[-1])))
            
            # appel au 2-opt pour chaque noeud de b_off
            for mu in b_off :
                two_opt(mu)
            
            # supprimer les noeuds de b_off qui ne respectent pas la contrainte de temps si on ajoute l'arc entre le dernier noeud de mu et le point d'arrivée
            b_off = [mu for mu in b_off if mu.time + mu.pplus[-1].distance_to(arrive) <= tmax]
            
            
            # verifier si les fils sont des feuilles
            if b_off == [] :
                for mlj in b :
                    # mlj est une feuille
                    # on ajoute l'arc entre le dernier noeud de mlj et le point d'arrivée
                    mlj.add_ending_point(arrive) # modifie le temps de parcours, le profit de mlj et pplus de mlj
                    profit_mlj = mlj.getProfit()
                    if profit_mlj > bestK.profit :
                        bestK = mlj #muetoile = mulj
                        

            b_off = sorted(b_off, key=lambda node: (-node.time, node.profit), reverse=True) # trier les noeuds de b_off par ordre décroissant de profit            
            b = b_off[:beam_width]
            b_off = []
        
        # on a trouvé un bestk pour la k-ième tournée    

        # on ajoute la tournée ayant le plus de profit à la liste des tournées
        two_opt(bestK)
        liste_tournee.append(bestK)
        
        # on supprime les noeuds de la tournée de la liste des noeuds
        clients = [node for node in clients if node not in bestK.pplus]
        k += 1
            
    return liste_tournee


def two_opt(mu) :
    improved = True
    noeuds = mu.pplus
    modified = False
    
    while improved :  
        imin = -1
        jmin = -1
        deltamin = float('inf') 
        for i in range(0, len(noeuds) - 3):
            for j in range(i + 2, len(noeuds)-1):
                x = noeuds[i]
                v = noeuds[j]
                u = noeuds[i+1]
                y = noeuds[j+1]
                
                # si l'arc (v,y) est avant l'arc (x,u) dans la tournée et ils sont contigus
                if (x.equal(y)):
                    continue
                
                delta = x.distance_to(v) + u.distance_to(y) - x.distance_to(u) - v.distance_to(y)
                if delta < deltamin :
                    deltamin = delta
                    imin = i
                    jmin = j
        
        deltamin = round(deltamin,2)
        
        if deltamin < 0 and imin != -1 and jmin != -1:
            new_nodes = noeuds[:imin+1] + noeuds[jmin:imin:-1] + noeuds[jmin+1:]
            mu.pplus = new_nodes
            noeuds = mu.pplus
            modified = True
            improved = True
        else :
            improved = False
    
    # mettre à jours le temps de parcours de mu si la liste des noeuds de mu a été modifié
    if modified :
        mu.calcul_temps()
        
    

"""
    trier par ordre croissant de distance entre le sommet courant et les sommets fils,
    si ils ont la meme distance on prend celle qui en a le plus de profit
                      
def trier_b_off(b_off) :
    for mu in b_off :
        
"""
                         
def print_plot_beam(routes, points_df):
    # Extraire les coordonnées x et y pour tous les points
    x_points = points_df['x']
    y_points = points_df['y']

    # Tracer tous les points
    plt.scatter(x_points, y_points, color='blue', label='Points')

    # Générer une palette de couleurs
    colors = plt.cm.viridis(np.linspace(0, 1, len(routes)))

    # Pour chaque route, tracer la trajectoire avec une couleur unique
    for mu, color in zip(routes, colors):
        x = [node.x for node in mu.pplus]
        y = [node.y for node in mu.pplus]

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