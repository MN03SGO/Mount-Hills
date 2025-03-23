import pygame
import constants
import os


class Caracteres:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.iventory = {"Madera": 0, "Piedra":0}
        image_path = os.path.join('assets', 'img', 'Caracteres', 'personaje.png')
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.PERSONAJE, constants.PERSONAJE))
        self.size = constants.PERSONAJE  # <- Forzar tamaño correcto

    def draw(self, ventana):
        ventana.blit(self.image, (self.x, self.y))





    def move(self, dx, dy, mundo):
        new_x = self.x + dx
        new_y = self.y + dy

        for arbol in mundo.arboles:
            if self.check_collision(new_x, new_y, arbol):
                return
            
    

            
        self.x = new_x
        self.y = new_y

        self.x = max(0, min(self.x, constants.WIDTH - self.size))
        self.y = max(0, min(self.y, constants.HEIGHT - self.size))


    def check_collision(self, x, y, obj):
        if x < obj.x + obj.size and x + self.size > obj.x and y < obj.y + obj.size and y + self.size > obj.y:
            return True
        return False  #Evento de colision con los arboles
    
    def is_near(self, obj):
        return (abs(self.x - obj.x) <= self.size + obj.size and
                abs(self.y - obj.y) <= self.size + obj.size)
    
    def interact(self, mundo):
        for arbol in mundo.arboles:
            if self.is_near(arbol):
                print("Estas cerca de un arbol")

        for piedra in mundo.piedras:
            if self.is_near(piedra):
                print("Estas cerca de una piedra")
    
            
        
