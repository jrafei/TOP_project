import csv
from utils import *
from clark_wright_class import *
import time


# Nom du fichier CSV
nom_fichier_csv = 'output_all_v2.csv'

# En-têtes des colonnes
en_tetes = ['instance', 'tmps_max', 'nombre_clients', 'nombre_tournees', 'profit_total', 'temps_execution']

#list = ['a','b','c','d','e','f']
set = ['Set_32_234/p1.','Set_21_234/p2.','Set_33_234/p3.', "Set_100_234/p4.",'Set_66_234/p5.','Set_64_234/p6.',"Set_102_234.p7."]
chiffre = ['2','3','4']
list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r']

# Ouvrir un fichier CSV pour l'écriture
with open(nom_fichier_csv, mode='w', newline='') as fichier_csv:
    writer = csv.writer(fichier_csv,delimiter=';')

    # Écrire l'en-tête
    writer.writerow(en_tetes)
    for s in set :
        for y in chiffre :
            for x in list:
                top = read_file("./data/"+s+y+"."+x+".txt")   
                if top == None :
                    print("fichier non trouvé")
                    continue
            
                """ #ECRIRE SUR UN FICHIER TXT
                print("================================== TEST ",x ," ======================")
                print("1.2."+x+".txt")
                print_to_file(file, "Temps Max : ", top['tmax'])
                print_to_file(file, "Nombre de Tournees : ", top['m'])
                print_to_file(file, "Nombre de Clients : ", top['n'])
                """
                
                # Collecter les données à écrire
                start_time = time.time()
                routes = clarke_wright(top['points'], top['tmax'], top['m'])
                end_time = time.time()
                if routes == None :
                    continue
                profit = sum_tournees_profit(routes)
                
                
                donnees = [y+"."+x, top['tmax'], top['n'], top['m'], profit, round((end_time - start_time),4)]
                #print_to_file(file,"Profit total : ", profit)
                writer.writerow(donnees)
                
                #for route in routes:            
                #    print(route)
                
                #print_plot(routes,top["points"])