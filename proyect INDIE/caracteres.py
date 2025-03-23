import pygame
import constants
import os


class Caracteres:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventario = {"Madera": 0, "Piedra":0}
        image_path = os.path.join('assets', 'img', 'Caracteres', 'personaje.png')
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.PERSONAJE, constants.PERSONAJE))
        self.size = constants.PERSONAJE  # <- Forzar tamaño correcto

        self.item_images = {
            "madera": self.load_item_images("madera.png"),
            "piedra": self.load_item_images("piedra.png")
        }

    def load_item_images(self, filename ):
        path = os.path.join('assets', 'img', 'Objetos', filename)
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (40, 40))
        return image

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
        if x < obj.x + obj.size*.75 and x + self.size*.75 > obj.x and y < obj.y + obj.size and y + self.size > obj.y:
            return True
        return False  #Evento de colision con los arboles
    
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



    
            
        
