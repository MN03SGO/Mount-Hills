import pygame
import constants
from elementos import Arbol, Piedras
import random
import os


class WorldChunk:
    """Representa un segmento del mundo con sus propios elementos."""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Crear una semilla aleatoria
        chunk_seed = hash(f"{x},{y}")
        old_state = random.getstate()
        random.seed(chunk_seed)
        
        # Generar elementos de chunk
        self.arboles = [
            Arbol(
                self.x + random.randint(0, width - constants.ARBOLES),
                self.y + random.randint(0, height - constants.ARBOLES)
            ) for _ in range(5)
        ]
        
        self.piedras = [
            Piedras(
                self.x + random.randint(0, width - constants.PIEDRAS),
                self.y + random.randint(0, height - constants.PIEDRAS)
            ) for _ in range(10)
        ]
        
        random.setstate(old_state)
    
    def draw(self, screen, pasto_image, camera_x, camera_y):
        chunk_screen_x = self.x - camera_x
        chunk_screen_y = self.y - camera_y
        
        # Calcular rango de tiles de pasto
        start_x = max(0, (camera_x - self.x - constants.PASTO) // constants.PASTO)
        end_x = min(self.width // constants.PASTO + 1,
                     (camera_x + constants.WIDTH - self.x + constants.PASTO) // constants.PASTO)
        
        start_y = max(0, (camera_y - self.y - constants.PASTO) // constants.PASTO)
        end_y = min(self.height // constants.PASTO + 1,
                     (camera_y + constants.HEIGHT - self.y + constants.PASTO) // constants.PASTO)

        for y in range(int(start_y), int(end_y)):
            for x in range(int(start_x), int(end_x)):
                screen_x = self.x + x * constants.PASTO - camera_x
                screen_y = self.y + y * constants.PASTO - camera_y
                screen.blit(pasto_image, (screen_x, screen_y))
                
        for piedra in self.piedras:
            piedra_screen_x = piedra.x - camera_x
            piedra_screen_y = piedra.y - camera_y
            if (piedra_screen_x + piedra.size >= 0 and piedra_screen_x <= constants.WIDTH and
                piedra_screen_y + piedra.size >= 0 and piedra_screen_y <= constants.HEIGHT):
                piedra.draw(screen, camera_x, camera_y)

class Mundo:
    def __init__(self, width, height):
        self.chunk_size = constants.WIDTH
        self.active_chunks = {}  
        
          
        
        # Tamaño del mundo
        self.view_width = width
        self.view_height = height
        
        pasto_path = os.path.join('assets', 'img', 'Objetos', 'pasto.png')
        self.pasto_image = pygame.image.load(pasto_path).convert()
        self.pasto_image = pygame.transform.scale(self.pasto_image, (constants.PASTO, constants.PASTO))
    
        self.generate_chunk(0, 0)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                self.generate_chunk(dx, dy)
    
    
    def get_chunk_key(self, x, y):
        chunk_x = x // self.chunk_size
        chunk_y = y // self.chunk_size
        return (chunk_x, chunk_y)
        
    def generate_chunk(self, chunk_x, chunk_y):
        key = (chunk_x, chunk_y)
        if key not in self.active_chunks:
            x = chunk_x * self.chunk_size
            y = chunk_y * self.chunk_size   
            self.active_chunks[key] = WorldChunk(x, y, self.chunk_size, self.chunk_size)
            
    def update_chunks(self, player_x, player_y):
        current_chunk = self.get_chunk_key(player_x, player_y)
        
        # Generar chunks adyacentes
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                chunk_x = current_chunk[0] + dx
                chunk_y = current_chunk[1] + dy
                self.generate_chunk(chunk_x, chunk_y)
                
        # Eliminar chunks lejanos
        chunks_to_remove = []
        for chunk_key in list(self.active_chunks.keys()):
            distance_x = abs(chunk_key[0] - current_chunk[0])
            distance_y = abs(chunk_key[1] - current_chunk[1])
            if distance_x > 2 or distance_y > 2:
                chunks_to_remove.append(chunk_key)
                 
        for chunk_key in chunks_to_remove:
            del self.active_chunks[chunk_key]
        
    def draw(self, ventana, camera_x, camera_y):
        for chunk in self.active_chunks.values():
            chunk.draw(ventana, self.pasto_image, camera_x, camera_y)
            
    @property
    def trees(self):
        all_trees = []
        for chunk in self.active_chunks.values():
            all_trees.extend(chunk.trees)
        return all_trees
        
    @property
    def piedras(self):
        all_piedras = []
        for chunk in self.active_chunks.values():
            all_piedras(chunk.piedras)
            return all_piedras