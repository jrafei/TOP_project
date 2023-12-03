import csv
from utils import *
from clark_wright_class import *



# Nom du fichier CSV
nom_fichier_csv = 'output_1.csv'

# En-têtes des colonnes
en_tetes = ['instance', 'tmps_max', 'nombre_clients', 'nombre_tournees', 'profit_total']

#list = ['a','b','c','d','e','f']
list = ['g','h','i','j','k','l','m','n','o','p','q']

# Ouvrir un fichier CSV pour l'écriture
with open(nom_fichier_csv, mode='w', newline='') as fichier_csv:
    writer = csv.writer(fichier_csv,delimiter=';')

    # Écrire l'en-tête
    writer.writerow(en_tetes)

    
    for x in list:
        top = read_file("./data/Set_32_234/p1.2."+x+".txt")
        
        """ #ECRIRE SUR UN FICHIER TXT
        print("================================== TEST ",x ," ======================")
        print("1.2."+x+".txt")
        print_to_file(file, "Temps Max : ", top['tmax'])
        print_to_file(file, "Nombre de Tournees : ", top['m'])
        print_to_file(file, "Nombre de Clients : ", top['n'])
        """
        
        # Collecter les données à écrire
        routes = clarke_wright(top['points'], top['tmax'], top['m'])
        if routes == None :
            continue
        profit = sum_tournees_profit(routes)
        
        donnees = [x, top['tmax'], top['n'], top['m'], profit]
        #print_to_file(file,"Profit total : ", profit)
        writer.writerow(donnees)
        
        #for route in routes:            
        #    print(route)
        
        #print_plot(routes,top["points"])