from utils import *
from route import *
from node import Node

class NodeBeam:

    next_id = 0
    
    def __init__(self, pp, pn, profit, t):
        """
        Parameters:
            pp List[Nodes] : listes des noeuds visités (avec le dépôt et l'arrivée)
            pn List[Nodes] : liste des noeuds non visités (sans le dépôt et l'arrivée)
            profit (float): Le profit associé au Node.
            t : temps de parcours des noeuds visités
        """
        self.id = Node.next_id  # Attribuer l'ID actuel à l'instance.
        Node.next_id += 1  # Incrémenter l'ID pour la prochaine instance.

        self.pplus = pp
        self.pneg = pn
        self.profit = profit
        self.time = t
        
    
    def getPplus(self):
        return self.pplus
    
    def getPneg(self):
        return self.pneg
    
    def getProfit(self):
        return self.profit
    
    def getTime(self):
        return self.time


    def distance_to(self, other):
        """ PAS UTILISER
        Calcule la distance euclidienne entre ce point et un autre point.

        Parameters:
            other (Point): L'autre point avec lequel calculer la distance.

        Returns:
            float: La distance euclidienne entre les deux points.
        """
        return (((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5).round(2)
    
    def addNode(self,node):
        self.Pplus.append(node)
        self.Pneg.remove(node)
        self.profit += node.profit
        self.time += node.distance_to(self.Pplus[-2]) + node.distance_to(self.Pplus[-1])
        
        
    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères du point.
        """
        #return f"Point(x={self.x}, y={self.y}, profit={self.profit})"
        return f"Point({self.id}, Point(x={self.x}, y={self.y})"
    
    def equal(self,other):
        return self.x == other.x and self.y == other.y and self.profit == other.profit

