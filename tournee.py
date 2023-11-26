class Tournee:
    """
    Représente une tournée qui contient un DataFrame de points incluant le point de départ,
    les clients, et le point d'arrivée.

    Attributes:
        points_df (pandas.DataFrame): DataFrame contenant les points de la tournée.
        longueur (float): Distance totale parcourue pendant la tournée.
        total_profit (float): Profit total accumulé pendant la tournée.
    """

    def __init__(self, points_df):
        """
        Initialise une nouvelle tournée avec un DataFrame de points.
        """
        self.points_df = points_df
        self.longueur = self.calculer_longueur()
        self.total_profit = self.calculer_total_profit()
        self.nb_clients = len(points_df) - 2

    def calculer_longueur(self):
        """
        Calcule la longueur totale de la tournée.
        """
        longueur = 0
        for i in range(len(self.points_df) - 1):
            point_actuel = self.points_df.iloc[i]
            point_suivant = self.points_df.iloc[i + 1]
            longueur += ((point_actuel['x'] - point_suivant['x']) ** 2 + (point_actuel['y'] - point_suivant['y']) ** 2) ** 0.5
        return longueur.round(2)

    def calculer_total_profit(self):
        """
        Calcule le profit total de la tournée.
        """
        return self.points_df['profit'].sum()

    def __repr__(self):
        """
        Affiche la tournée.
        """
        return f"Tournee(longueur={self.longueur}, total_profit={self.total_profit})"

"""
# Exemple d'utilisation :
import pandas as pd

# Création d'un DataFrame pour représenter les points de la tournée
df = pd.DataFrame({'x': [0, 1, 2, 10], 'y': [0, 2, 3, 10], 'profit': [0, 30, 40, 0]})

tournee = Tournee(df)
print(f"Longueur de la tournée: {tournee.longueur}")
print(f"Profit total de la tournée: {tournee.total_profit}")
"""