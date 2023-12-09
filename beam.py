from utils import *
from route import *
from node import Node
from nodeBeam import NodeBeam


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
    liste_noeuds = [pt_depart]
    for _,row in clients.iterrows():
        client = Node(row['x'],row['y'],row['profit'])
        test_time = client.distance_to(pt_depart) + client.distance_to(pt_arrivee)
        if test_time <= tmax :
            liste_noeuds.append(client)
    
    liste_noeuds.append(pt_arrivee)
    
    return liste_noeuds, pt_depart, pt_arrivee


"""_summary_
    points : list[Node] = listes des clients (pourlesquel leurs tourné marguerite respectent la contrainte de temps)
    tmax : float : le temps de parcours maximal
    m : int : le nombre de tournées à retourner
    beam_width : int : le nombre de noeuds à garder à chaque itération
    @Returns:
    list[NodeBeam] : Retourne une liste de tournées.
"""
def beam (points,depart, arrive, tmax, m, beam_width) :
    liste_tournee = [] #Type : list[NodeBeam]
    
    k = 0
    while k<m : # Construction des m tournées
        mu_zero = NodeBeam([depart],points,0,0) # mu_zero : NodeBeam
        b = [mu_zero]
        l = 0
        bestK = mu_zero #muetoile
        
        # creation des noeuds fils des noeuds de b
        while b != [] : # tant que les sommets courants ne sont pas vide
            
            # creation des noeuds fils de mu
            b_off = [] 
            for mu in b :
                pn = mu.getPneg()
                pp = mu.getPplus()
                t = mu.getTime()
                p = mu.getProfit()
                for i in range(0,len(pn)) : # rappel : Pneg est liste des noeuds non visités sans le dépôt et l'arrivée
                    # Verifier que les noeuds fils de mu respectent la contrainte de temps
                    if t + pn[i].distance_to(pp[-1]) + pn[i].distance_to(arrive) <= tmax :
                        b_prime.append(NodeBeam(pp + [pn[i]],pn[:i] + pn[i+1:],p + pn[i].getProfit(), t + pn[i].distance_to(pp[-1])))
            
            
            l += 1 # on est dans le niveau suivant de l'arbre
            
            # appel au 3-opt pour chaque noeud de b_off
            for mu in b_off :
                mu = three_opt(mu)
            
            # supprimer les noeuds de b_off qui ne respectent pas la contrainte de temps si on ajoute l'arc entre le dernier noeud de mu et le point d'arrivée
            b_off = [mu for mu in b_off if mu.time + mu.Pplus[-1].distance_to(arrive) <= tmax]
            
            # verifier si il existe un noeud feuille -> si le noeud n'a pas de fils noeuds aveclesquel on peut les fusionner
            for nlj in b_off :
                pn_nlj = nlj.getPneg()
                if pn_nlj == [] :
                    # si oui on ajoute l'arc entre le dernier noeud de nlj et le point d'arrivée
                    nlj.add(arrive) # modifie le temps de parcours, le profit de nlj et pplus de nlj
                    p_nlj = nlj.getProfit()
                    if p_nlj > bestK.profit :
                        bestK = nlj #muetoile = mulj
            
            
            b_prime = sorted(b_prime, key=lambda node: node.profit, reverse=True) # trier les noeuds de b_prime par ordre décroissant de profit
            b = b_prime[:beam_width]
            b_off = []

        # on ajoute la tournée ayant le plus de profit à la liste des tournées
        liste_tournee.append(bestK)
        # on supprime les noeuds de la tournée de la liste des noeuds
        points = [node for node in points if node not in bestK.Pplus]
        k += 1
    
    return liste_tournee
        


    """_summary_
    A REVOIR PAS FINI , NOUBLIEZ PAS DE MODIFIER LE TEMPS DE PARFCOURS 0A LA FIN
    """
def three_opt(mu) :
    improve = True
    while improve:
        improve = False
        for i in range(0,len(mu.Pplus)) :
            for j in range(0,len(mu.Pplus)) :
                for k in range(0,len(mu.Pplus)) :
                    if (j != i-1 and j != i+1 and k != i-1 and k != i+1 and k != j-1 and k != j+1) :
                        new_time = mu.Pplus[i].distance_to(mu.Pplus[j]) + mu.Pplus[i+1].distance_to(mu.Pplus[k]) + mu.Pplus[j+1].distance_to(mu.Pplus[k+1])
                        if (mu.Pplus[i].distance_to(mu.Pplus[i+1]) + mu.Pplus[j].distance_to(mu.Pplus[j+1]) + mu.Pplus[k].distance_to(mu.Pplus[k+1]) > new_time) : 
                            mu.Pplus[i+1:j+1] = mu.Pplus[j:i:-1]
                            improve = True
        