import pygame
import constants

class Caracteres:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 28

    def draw(self, screen):
        pygame.draw.rect(screen, constants.BLUE, (self.x, self.y, self.size, self.size))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy