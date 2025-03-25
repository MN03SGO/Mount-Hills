import pygame
import constants
import os

class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wood = 5

        tree_path = os.path.join('assets', 'images', 'objects', 'tree.png')
        self.image = pygame.image.load(tree_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.TREE, constants.TREE))
        self.size = self.image.get_width()


    def draw(self, screen, camera_x, camera_y):
        # Calcular posición en pantalla relativa a la cámara
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y

        # Solo dibujar si está en la pantalla
        if (screen_x + self.size >= 0 and screen_x <= constants.WIDTH and
                screen_y + self.size >= 0 and screen_y <= constants.HEIGHT):
            screen.blit(self.image, (screen_x, screen_y))


    def chop(self, with_axe=False):
        if self.wood > 0:
            if with_axe:
                self.wood -= 2
                if self.wood < 0:
                    self.wood = 0
            else:        
                self.wood -= 1
            return True
        return False

    def is_depleted(self):
        return self.wood <= 0

class SmallStone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stone = 1

        small_stone_path = os.path.join('assets', 'images', 'objects', 'small_stone.png')
        self.image = pygame.image.load(small_stone_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.SMALL_STONE, constants.SMALL_STONE))
        self.size = self.image.get_width()

    def draw(self, screen, camera_x, camera_y):
        # Calcular posición en pantalla relativa a la cámara
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y

        # Solo dibujar si está en la pantalla
        if (screen_x + self.size >= 0 and screen_x <= constants.WIDTH and
                screen_y + self.size >= 0 and screen_y <= constants.HEIGHT):
            screen.blit(self.image, (screen_x, screen_y))

    def collect(self):
        if self.stone > 0:
            self.stone -= 1
            return True
        return False

    def is_depleted(self):
        return self.stone <= 0

class FarmLand:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        farmland_path = os.path.join('assets', 'images', 'objects', 'FarmLand.png')
        self.image = pygame.image.load(farmland_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.GRASS, constants.GRASS))
        self.size = self.image.get_width()

    def draw(self, screen, camera_x, camera_y):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        if (screen_x + self.size >= 0 and screen_x <= constants.WIDTH and
                screen_y + self.size >= 0 and screen_y <= constants.HEIGHT):
            screen.blit(self.image, (screen_x, screen_y))
