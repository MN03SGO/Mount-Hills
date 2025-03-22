import pygame
import constants

class Caracteres:
    def __init__(self, x, y): #posicion inicial
        self.x = x
        self.y = y
        self.size = 28 # tamaño del personaje
        self.inventory = {"wood": 0}# inventario

    def draw(self, screen):
        pygame.draw.rect(screen, constants.BLUE, (self.x, self.y, self.size, self.size))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.x = max(0, min(self.x, constants.WIDTH - self.size)) # limites de la pantalla x,y
        self.y = max(0, min(self.y, constants.HEIGHT - self.size))