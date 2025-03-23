import pygame
import constants
from elementos import Arbol, Piedras
import random
import os

class Mundo:
    def __init__(self, width, height): 
        #tamaño del mundo
        self.width = width
        self.height = height
        self.arboles = [ Arbol(random.randint(0, width-constants.ARBOLES), random.randint(0, height-constants.ARBOLES)) for _ in range(20) ] #Se crean 20 arboles aleatoriamente en el mundo
        self.piedras = [ Piedras(random.randint(0, width-constants.PIEDRAS), random.randint(0, height-constants.PIEDRAS)) for _ in range(20) ] #Se crean 20 piedras aleatoriamente en el mundo

        
        pasto_path = os.path.join('assets', 'img', 'Objetos', 'pasto.png')
        self.pasto_image = pygame.image.load(pasto_path).convert()
        self.pasto_image = pygame.transform.scale(self.pasto_image,( constants.PASTO, constants.HEIGHT))
    



    def draw(self, ventana):
        for y in range(0, self.width, constants.PASTO):
            for x in range(0, self.height, constants.PASTO):
                ventana.blit(self.pasto_image, (x, y))

        for piedra in self.piedras:
            piedra.draw(ventana)

        for arbol in self.arboles:
            arbol.draw(ventana)

        
