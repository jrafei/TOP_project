import csv
from beam import *
import time

      
#x = 't'
x='k'
def main() : 
    print("================================== TEST ",x ," ======================")
    
    
    #top = read_file("./data/Set_33_234/p3.4."+x+".txt")  
    top = read_file("./data/Set_21_234/p2.3."+x+".txt")   
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
            #print("TEMPS : ", mu.time)
            #for node in mu.pplus : 
            #    print(node.__str__())
            profit += mu.profit
        
        if profit > best_profit :
            best_profit = profit
            best_mus = mus
            wmax = w
    
    
    #print("DANS MAIN : ")
    #print(mus)
    
    if best_mus == None :
        return None    
    for mu in best_mus:
        print(mu.time)

    print("Profit total : ", best_profit)
    print("wmax : ", wmax)

    """
    for mu in mus:
        print(mu.pplus)            
        print(mu)
    """
    print_plot_beam(mus,top["points"])
    
main()
