import pygame
import constants
import os
from constants import *


class Caracteres:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventario = {"Madera": 0, "Piedra":0}



        # Cargar la hoja de animaciones
        image_path = os.path.join('assets', 'img', 'Caracteres', 'Personaje.png')
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.PERSONAJE, constants.PERSONAJE))
        self.sprite_sheet = self.image  # Asignar sprite_sheet correctamente
        self.size = constants.PERSONAJE  

        # Cargar imágenes de objetos del inventario
        self.item_images = {
            "madera": self.load_item_images("madera.png"),
            "piedra": 
            self.load_item_images("piedra.png")
        }
        self.sed = constants.MAX_SED
        self.energia = constants.MAX_ENERGIA
        self.hambre = constants.MAX_HABRE


    # IMAGENES DEL INVENTARIO
    def load_item_images(self, filename ):
        path = os.path.join('assets', 'img', 'Objetos', filename)
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (40, 40))
        return image
    # MOSTRAR EN PANTALLA
    def draw(self, ventana):
        ventana.blit(self.image, (self.x, self.y))
        self.draw_estado_barra(ventana)

    # Movimiento del personaje
    def move(self, dx, dy, mundo):
        self.moving = dx != 0 or dy != 0
        
        new_x = self.x + dx
        new_y = self.y + dy

        for arbol in mundo.arboles:
            if self.check_collision(new_x, new_y, arbol):
                return
        self.x = new_x
        self.y = new_y

        self.x = max(0, min(self.x, constants.WIDTH - self.size))
        self.y = max(0, min(self.y, constants.HEIGHT - self.size))


        # Perdida de energia por movimiento
        if dx != 0 or dy != 0: 
            self.actualizar_Energia(-0.05)
        

#Evento de colision con los arboles
    def check_collision(self, x, y, obj):
        if x < obj.x + obj.size*.75 and x + self.size*.75 > obj.x and y < obj.y + obj.size and y + self.size > obj.y:
            return True
        return False  
    def is_near(self, obj):
        return (abs(self.x - obj.x) <= max(self.size, obj.size)+5 and
                abs(self.y - obj.y) <= max(self.size, obj.size)+5)
    
    def interact(self, mundo):
        for arbol in mundo.arboles:
            if self.is_near(arbol):
                if arbol.cortar():
                    self.inventario["Madera"] += 1
                    if arbol.madera == 0:
                        mundo.arboles.remove(arbol)
                        return

        for piedra in mundo.piedras:
            if self.is_near(piedra):
                self.inventario["Piedra"] += piedra.piedra
                mundo.piedras.remove(piedra)
# INVENTARIO
    def draw_inventario(self, ventana):
        background = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
        background.fill((0, 0, 0, 128)) 
        ventana.blit(background, (0, 0))
        font = pygame.font.Font(None, 36)
        title = font.render("Inventario", True, constants.WHITE)
        ventana.blit(title, (constants.WIDTH//2 - title.get_width()//2, 20))

        item_fuente = pygame.font.Font(None, 30)
        y_offset = 80 
        items_per_column = 5 
    
        for idx, (item, cantidad) in enumerate(self.inventario.items()):
            if cantidad > 0:
                row = idx % items_per_column  
                col = idx // items_per_column  
                item_y = y_offset + row * 50 
                item_x = constants.WIDTH // 2 - 60 + col * 150# separacion entre columnas

                ventana.blit(self.item_images[item.lower()], (item_x, item_y))
                texto = item_fuente.render(f"{item.capitalize()}: {cantidad}", True, constants.WHITE)
                ventana.blit(texto, (item_x + 40, item_y))
        
        cerrar_texto = font.render("Presiona 'i' para cerrar", True, constants.WHITE)
        ventana.blit(cerrar_texto, (constants.WIDTH//2 - cerrar_texto.get_width()//2, constants.HEIGHT - 50))




    def actualizar_Energia(self, aumento):
        self.energia = max(0, min(self.energia + aumento, constants.MAX_ENERGIA))

    def actualizar_Hambre(self, aumento):
        self.hambre = max(0, min(self.hambre + aumento, constants.MAX_HABRE))

    def actualizar_Sed(self, aumento):
        self.sed = max(0, min(self.sed + aumento, constants.MAX_SED))


    def draw_estado_barra(self, ventana):
        bar_width = 100
        bar_height = 10
        x_offset = 10
        y_offset = 10

        #BARRA
        
        # BARRA DE ENERGIA
        pygame.draw.rect(ventana, constants.BAR_BACKGROUND_COLOR, 
                    (x_offset, y_offset, bar_width, bar_height))
    
        pygame.draw.rect(ventana, constants.ENERGIA_COLOR,
                    (x_offset, y_offset, bar_width*(self.energia/ constants.MAX_ENERGIA),bar_height))
        # BARRA DE HAMBRE
        y_offset += 15
        pygame.draw.rect(ventana, constants.BAR_BACKGROUND_COLOR,
                    (x_offset, y_offset, bar_width, bar_height))
        
        pygame.draw.rect(ventana, constants.HAMBRE_COLOR,
                    (x_offset, y_offset, bar_width*(self.hambre/ constants.MAX_HABRE),bar_height))
        # BARRA DE SED
        
        y_offset += 15
        pygame.draw.rect(ventana, constants.BAR_BACKGROUND_COLOR,
                    (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(ventana, constants.SED_COLOR,
                    (x_offset, y_offset, bar_width*(self.sed/ constants.MAX_SED),bar_height))
        
    def actualizar_estado(self):
        self.actualizar_Hambre(-0.01)
        self.actualizar_Sed(-0.02)

        if self.hambre < constants.MAX_HABRE * 0.2 or self.sed <    constants.MAX_SED * 0.2:
            self.actualizar_Energia(-0.05)