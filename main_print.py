import csv
from utils import *
from clark_wright_class import *


       
x = 'p'

def main() : 
    print("================================== TEST ",x ," ======================")
    print("1.2."+x+".txt")
    
    top = read_file("./data/Set_32_234/p1.2."+x+".txt")   
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