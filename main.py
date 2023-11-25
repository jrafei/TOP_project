import matplotlib.pyplot as plt
from tournee import *
from clark_wright import *

dict = read_file("./data/Set_32_234/p1.2.a.txt")

df_points = dict['points']

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

"""_summary_
    affichage des tournées
"""
# Exemple d'utilisation
point1 = df_points.iloc[[0]]  # Premier point
point2 = df_points.iloc[[1]]  # Deuxième point

distance = distance(point1, point2)
print("Distance:", round(distance,2))