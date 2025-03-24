import pygame
import constants
import os

class Arbol:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.madera = 5

        arboles_path = os.path.join('assets', 'img', 'Objetos', 'arbol.png')
        self.image = pygame.image.load(arboles_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.ARBOLES, constants.ARBOLES))
        self.size = self.image.get_width()

    def draw(self, ventana):
        ventana.blit(self.image, (self.x, self.y))

    def cortar(self):
        if self.madera > 0:
            self.madera -= 1
            return True

class Piedras:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.piedra = 1

        piedras_path = os.path.join('assets', 'img', 'Objetos', 'piedra.png')
        self.image = pygame.image.load(piedras_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.PIEDRAS, constants.PIEDRAS))
        self.size = self.image.get_width()

    def draw(self, ventana):
        ventana.blit(self.image, (self.x, self.y))
