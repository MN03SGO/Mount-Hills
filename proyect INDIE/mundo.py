import pygame
import constants
from elementos import Arbol
import random

class Mundo:
    def __init__(self, width, height): 
        #tamaño del mundo
        self.width = width
        self.height = height
        self.arboles = [ Arbol(random.randint(0, width), random.randint(0, height)) for _ in range(30) ] #Se crean 30 arboles aleatoriamente en el mundo
        
    def draw(self, screen):
        screen.fill(constants.GREEN)
        for arbol in self.arboles:
            arbol.draw(screen)
