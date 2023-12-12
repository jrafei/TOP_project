import csv
from beam import *

"""
    Ce fichier main permet de tester l'algorithme beam search sur les instances du problème de tournées de véhicules.
    Il génère aussi, grace au bibliothèque matplotlib, le graphe pour visualiser les tournées trouvées.
"""

      
#x = 't'
x='i'
def main() : 
    print("================================== TEST ",x ," ======================")
    
    
    #top = read_file("./data/Set_33_234/p3.4."+x+".txt")  
    top = read_file("./data/Set_66_234/p5.4."+x+".txt")   
    print("Temps Max : ", top['tmax'])
    print( "Nombre de Tournees : ", top['m'])
    print( "Nombre de Clients : ", top['n'])    
    
    # Collecter les données à écrire
    best_mus = None
    best_profit = 0
    wmax = 0
    for w in range (1,10) : 
        liste_clients, pt_depart, pt_arrivee = getNode_respect_time(top['points'],top['tmax'])
        mus = beam(liste_clients,pt_depart,pt_arrivee, top['tmax'], top['m'], w)
        profit = 0
        for mu in mus:
            profit += mu.profit
        
        if profit > best_profit :
            best_profit = profit
            best_mus = mus
            wmax = w
    
    if best_mus == None :
        return None    

    print("Profit total : ", best_profit)
    print("wmax : ", wmax)
    print_plot_beam(mus,top["points"])
    
main()
