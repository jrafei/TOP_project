import matplotlib.pyplot as plt
from tournee import *
from clark_wright import *
from utils import *
"""
# Extraire les coordonnées x et y
x = df_points['x']
y = df_points['y']


# Créer un graphique de dispersion pour tous les points
plt.scatter(x, y, color='blue')  # Points intermédiaires en bleu

# Point de départ en rouge
plt.scatter(x.iloc[0], y.iloc[0], color='red', label='Départ')

# Point d'arrivée en vert
plt.scatter(x.iloc[-1], y.iloc[-1], color='green', label='Arrivée')

# Ajouter des titres, des étiquettes et une légende
plt.title("Affichage des Points")
plt.xlabel("Coordonnée X")
plt.ylabel("Coordonnée Y")
plt.legend()


# Afficher le graphique
plt.show()
"""

top = read_file("./data/Set_32_234/p1.4.q.txt")


""" TEST INIT_MARGUERITE
"""
#init = init_marguerite(top['points'], top['tmax'])

tours = clarke_wright(top)
print("==================================TOURS======================")
print_tournees(tours)
print("==================================FIN TOURS======================")
profit = sum_tournees_profit(tours)
print("Profit total : ", profit)
print_plot(tours)