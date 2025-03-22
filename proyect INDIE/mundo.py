import pygame
import constants

class Mundo:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, screen):
        screen.fill(constants.GREEN)