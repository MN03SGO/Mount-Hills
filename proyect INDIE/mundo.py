import pygame
import constants
from elementos import Arbol
import random
import os

class Mundo:
    def __init__(self, width, height): 
        #tamaño del mundo
        self.width = width
        self.height = height
        self.arboles = [ Arbol(random.randint(0, width-40), random.randint(0, height-40)) for _ in range(20) ] #Se crean 20 arboles aleatoriamente en el mundo
        
        pasto_path = os.path.join('assets', 'img', 'Objetos', 'pasto.png')
        self.pasto_image = pygame.image.load(pasto_path).convert()
        self.pasto_image = pygame.transform.scale(self.pasto_image,( constants.PASTO, constants.HEIGHT))
    



    def draw(self, screen):
        for y in range(0, self.width, constants.PASTO):
            for x in range(0, self.height, constants.PASTO):
                screen.blit(self.pasto_image, (x, y))




        for arbol in self.arboles:
            arbol.draw(screen)
