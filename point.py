class Point:
    """
    Représente un point dans un espace bidimensionnel avec un profit associé.

    Attributes:
        x (float): L'abscisse du point.
        y (float): L'ordonnée du point.
        profit (float): Le profit associé au point.
    """

    def __init__(self, x, y, profit):
        """
        Initialise un nouveau point avec les coordonnées et le profit fournis.

        Parameters:
            x (float): L'abscisse du point.
            y (float): L'ordonnée du point.
            profit (float): Le profit associé au point.
        """
        self.x = x
        self.y = y
        self.profit = profit

    def distance_to(self, other):
        """
        Calcule la distance euclidienne entre ce point et un autre point.

        Parameters:
            other (Point): L'autre point avec lequel calculer la distance.

        Returns:
            float: La distance euclidienne entre les deux points.
        """
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    
    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères du point.
        """
        return f"Point(x={self.x}, y={self.y}, profit={self.profit})"

    def afficher(self):
        """
        Affiche les attributs du point.
        """
        print(self.__str__())