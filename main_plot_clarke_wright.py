import csv
from utils import *
from clark_wright import *


"""
    Ce fichier main permet de tester l'algorithme clarke and wright sur les instances du problème de tournées de véhicules.
    Il génère aussi, grace au bibliothèque matplotlib, le graphe pour visualiser les tournées trouvées.
"""

       
#x = 't'
x='i'
def main() : 
    
    #top = read_file("./data/Set_33_234/p3.4."+x+".txt")  
    top = read_file("./data/Set_32_234/p1.3."+x+".txt")   
    print("Temps Max : ", top['tmax'])
    print( "Nombre de Tournees : ", top['m'])
    print( "Nombre de Clients : ", top['n'])    
    
    # Collecter les données à écrire
    
    routes = clarke_wright(top['points'], top['tmax'], top['m'])
    if routes == None :
        return None
    profit = sum_tournees_profit(routes)

    print("Profit total : ", profit)

    for route in routes:            
        print(route)

    print_plot(routes,top["points"])
    
main()