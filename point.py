class Point:
    """
    Représente un point dans un espace bidimensionnel avec un profit associé.

    Attributes:
        x (float): L'abscisse du point.
        y (float): L'ordonnée du point.
        profit (float): Le profit associé au point.
        depart (bool): Le Node est un Node de départ ou non.
        arrive (bool): Le Node est un Node d'arrivée ou non.
    """
   
    def __init__(self, x, y, profit,dep,arriv):
        """
        Initialise un nouveau Node avec les coordonnées et le profit fournis.

        Parameters:
            x (float): L'abscisse du Node.
            y (float): L'ordonnée du Node.
            profit (float): Le profit associé au Node.
            depart (bool): Le Node est un Node de départ ou non.
            arrive (bool): Le Node est un Node d'arrivée ou non.
        """
        self.x = x
        self.y = y
        self.profit = profit
        self.depart = dep
        self.arrive = arriv
        
        
    def distance_to(self, other):
        """
        Calcule la distance euclidienne entre ce point et un autre point.

        Parameters:
            other (Point): L'autre point avec lequel calculer la distance.

        Returns:
            float: La distance euclidienne entre les deux points.
        """
        return (((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5).round(2)
    
    
    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères du point.
        """
        return f"Point(x={self.x}, y={self.y}, profit={self.profit})"

