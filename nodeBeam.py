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
        self.id = NodeBeam.next_id  # Attribuer l'ID actuel à l'instance.
        NodeBeam.next_id += 1  # Incrémenter l'ID pour la prochaine instance.

        self.pplus = pp # liste des noeuds visités (avec le dépôt et l'arrivée)
        self.pneg = pn # liste des noeuds non visités (sans le dépôt et l'arrivée)
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


        """_summary_
        
        """
    def add_ending_point(self,end_point):
        self.pplus.append(end_point)
        self.profit += end_point.profit
        self.time += end_point.distance_to(self.pplus[-1])
    
    
    def calcul_temps(self) :
        t = 0
        for i in range(0,len(self.pplus)-1) :
            t += self.pplus[i].distance_to(self.pplus[i+1])
        return t
    
    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de la route.
        """
        return f"Route(longueur={self.time}, profit={self.profit})"   
    
    def print_nodebeam(self):
        print("list noeud visités :")
        for node in self.pplus :
            print("     ",node)
        
        print("list noeud  non visités :")
        for node in self.pneg :
            print("     ",node)
        
        print("profit : ", self.profit)
        print("time : ", self.time)
        print("id : ", self.id)
        