import pygame
import constants
import os

class Arbol:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.wood = 5
        arboles_path = os.path.join('assets', 'img', 'Objetos', 'arbol.png')
        self.image = pygame.image.load(arboles_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.ARBOLES, constants.ARBOLES))
        self.size = self.image.get_width()


    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))