from point import Point

class Tournee:
    """
    Représente une tournée avec un point de départ, un point d'arrivée, une liste de clients, 
    la longueur de la tournée et la totale des profits.

    Attributes:
        pt_depart (Point): Le point de départ de la tournée.
        pt_arrivee (Point): Le point d'arrivée de la tournée.
        clients (List[Point]): Liste des clients (points) visités pendant la tournée.
        longueur (float): Distance totale parcourue pendant la tournée.
        total_profit (float) : profits de toutes les clients visité
    """

    def __init__(self, pt_depart, pt_arrivee, clients):
        """
        Initialise une nouvelle tournée.
        """
        self.pt_depart = pt_depart
        self.pt_arrivee = pt_arrivee
        self.clients = clients
        self.longueur = self.calculer_longueur()
        self.total_profit = self.calculer_total_profit()

    def calculer_longueur(self):
        """
        Calcule la longueur totale de la tournée.
        """
        longueur = 0
        point_precedent = self.pt_depart

        # Parcourir tous les clients
        for client in self.clients:
            longueur += point_precedent.distance_to(client)
            point_precedent = client

        # Ajouter la distance du dernier client à l'arrivée
        longueur += point_precedent.distance_to(self.pt_arrivee)

        return longueur
    

    def calculer_total_profit(self):
        """
        Calcule le profit total de la tournée en additionnant le profit de chaque client visité.

        Returns:
            float: Le profit total de la tournée.
        """
        return sum(client.profit for client in self.clients)
    
    
    def fusion(self, t):
        """
        Fusionne cette tournée avec une autre tournée.

        Parameters:
            t (Tournee): La tournée à fusionner avec celle-ci.
        """
        # Fusionner les listes de clients
        self.clients.extend(t.clients)

        # Mettre à jour le point d'arrivée
        self.pt_arrivee = t.pt_arrivee

        # Recalculer la longueur et le profit total
        self.longueur = self.calculer_longueur()
        self.total_profit = self.calculer_total_profit()



# Exemple d'utilisation :
pt_depart = Point(0, 0, 0)
pt_arrivee = Point(10, 10, 0)
clients = [Point(1, 2, 30), Point(3, 4, 40), Point(5, 6, 50)]

tournee = Tournee(pt_depart, pt_arrivee, clients)
print(f"Longueur de la tournée: {tournee.longueur}")
print(f"Profit total de la tournée: {tournee.total_profit}")

# Exemple d'utilisation :
tournee1 = Tournee(pt_depart, pt_arrivee, [Point(1, 2, 30), Point(3, 4, 40)])
tournee2 = Tournee(Point(10, 10, 0), Point(20, 20, 0), [Point(6, 7, 50), Point(8, 9, 60)])

tournee1.fusion(tournee2)
print(f"Longueur de la tournée fusionnée: {tournee1.longueur}")
print(f"Profit total de la tournée fusionnée: {tournee1.total_profit}")

