import matplotlib.pyplot as plt
from tournee import *
#from clark_wright import *
from utils import *
from clark_wright_class import *
from clark_wright import *


top = read_file("./data/Set_32_234/p1.4.k.txt")


"""
print("TEST SANS CLASSES V2 ")
tours = clarke_wright_sans_classe(top)
if tours == None :
    print("Aucune tournée n'a été générée !")
    exit()
print("==================================TOURS======================")
print_tournees(tours)
print("==================================FIN TOURS======================")
profit = sum_tournees_profit_sans_classe(tours)
print("Profit total : ", profit)
print_plot_sans_classe(top["points"],tours)
"""



print(" TEST AVEC DES CLASSES")


routes = clarke_wright(top)
profit = sum_tournees_profit(routes)
print("Temps Max : ", top['tmax'])
print("Nombre de Tournees : ", top['m'])
print("Nombre de Clients : ", top['n'])
print("Profit total : ", profit)



for route in routes:
    #color_name = mcolors.get_named_colors_mapping().get(color, "Inconnu")
    print(route)
print_plot(routes,top["points"])