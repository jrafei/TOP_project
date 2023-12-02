class Route:
    """
    Représente une route constituée de segments entre des points.

    Attributes:
        arcs (list of tuple of Point): Liste des couples de points formant les segments de la route.
        longueur (float): Longueur totale de la route.
        profit (float): Profit associé à la route.
    """

    def __init__(self, arcs):
        """
        Initialise une nouvelle route avec la liste des couples de arcs fournie.

        Parameters:
            arcs (list of tuple of Point): Liste des couples de points formant les segments de la route.
        """
        self.arcs = arcs
        self.longueur = self.calculer_longueur()
        self.profit = self.calculer_profit()  # Profit total de la route

    def calculer_longueur(self):
        """
        Calcule la longueur totale de la route en sommant les distances entre chaque couple de points.

        Returns:
            float: La longueur totale de la route.
        """
        longueur_totale = 0.0
        for (point1, point2) in self.arcs:
            longueur_totale += point1.distance_to(point2)
        return longueur_totale.round(2)


    def calculer_profit(self):
        """
        Calcule le profit total de la route en sommant le profit de chaque point qui la constitue.

        Returns:
            float: Le profit total de la route.
        """
        profit_total = 0.0
        points_vus = set()  

        for segment in self.arcs:
            for point in segment:
                # Vérifie si ce point a déjà été compté
                if point not in points_vus:
                    profit_total += point.profit
                    points_vus.add(point)

        return profit_total
    
    
    
    def fusion(self, autre_route):
        """
        Ajoute les segments de l'autre route à la fin de cette route, à condition que 
        le dernier client de cette route est le même que le premier client de l'autre route.
        Met à jour la longueur et le profit de la route.
        
        Parameters:
            autre_route (Route): L'autre route à fusionner avec cette route.
        """
        dernier_arc_t1 = self.arcs[-1]
        premier_arc_t2 = autre_route.arcs[0]
        
        if (dernier_arc_t1[0] != premier_arc_t2[0]):
            raise Exception("Le dernier client de la route ne correspond pas au premier client de départ du nouveau arc.")
        
        # On remplace le dernier arc de la route par l'arc qui relie le dernier client au premier client de l'autre route
        self.arcs[-1] = (dernier_arc_t1[0], premier_arc_t2[1])
        # On enlève le premier arc de l'autre route
        autre_route.arcs.pop(0)
        # On ajoute les arcs de l'autre route à la fin de la route
        self.arcs.extend(autre_route.arcs)
        
        self.longueur = self.calculer_longueur()
        self.profit = self.calculer_profit()


    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de la route.
        """
        return f"Route(longueur={self.longueur}, profit={self.profit})"

