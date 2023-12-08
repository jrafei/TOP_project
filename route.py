class Route:
    """
    Représente une route constituée des arcs orienté entre les clients.

    Attributes:
        nodes (list of Node): Liste des noeuds visités dans la tournée.
        longueur (float): Longueur totale de la tournée.
        profit (float): Profit associé à la tournée.
    """

    def __init__(self, nodes):
        """
        Initialise une nouvelle tournée avec la liste des couples de arcs fournie.

        Parameters:
            nodes (list of Node): Liste des noeuds visités.
        """
        self.nodes = nodes
        self.longueur = self.calculer_longueur()
        self.profit = self.calculer_profit()  # Profit total de la route

    def calculer_longueur(self):
        """
        Calcule la longueur totale de la tournée en sommant les distances entre chaque couple de noeud.
        Returns:
            float: La longueur totale de la route.
        """
        longueur_totale = 0.0
        for indx in range(len(self.nodes)-1):
            indy = indx + 1
            point1 = self.nodes[indx]
            point2 = self.nodes[indy]
            longueur_totale += point1.distance_to(point2)
        return longueur_totale.round(2)


    def calculer_profit(self):
        """
        Calcule le profit total de la tournée en sommant le profit de chaque client.

        Returns:
            float: Le profit total de la tournée.
        """
        profit_total = 0.0
        
        for noeud in self.nodes : 
            profit_total += noeud.profit

        return profit_total.round(2)


    
    def fusion(self, autre_route):
        """
        Ajoute les segments de nouveau route à la fin de cet route, 
        Met à jour la longueur et le profit de la route.
        Parameters:
            autre_route (Route): route à fusionner avec.
        """
       
        # Ajouter les noeuds de nouveau tournée à la fin de cette tournée
        self.nodes = self.nodes[:-1] + autre_route.nodes[1:]
        self.longueur = self.calculer_longueur()
        self.profit = self.profit + autre_route.profit
        return None
    
    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de la route.
        """
        return f"Route(longueur={self.longueur}, profit={self.profit})"
    
    def print_nodes(self):
        """
        Retourne une représentation en chaîne de caractères de la route.
        """
        print("Route : ")
        for node in self.nodes :
            print(node.__str__())
        return None

