import pygame
import constants
from elements import Tree, SmallStone, FarmLand
import random
import os
from pygame import Surface

class WorldChunk:
    """Representa un segmento del mundo con sus propios elementos"""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.farmland_tiles = {} 

        # Crear una semilla única basada en las coordenadas del chunk
        chunk_seed = hash(f"{x},{y}")
        # Guardar el estado actual del generador random
        old_state = random.getstate()
        # Establecer la semilla para este chunk
        random.seed(chunk_seed)

        # Generar elementos del chunk
        self.trees = [
            Tree(
                self.x + random.randint(0, width-constants.TREE),
                self.y + random.randint(0, height-constants.TREE)
            ) for _ in range(5)
        ]

        self.small_stones = [
            SmallStone(
                self.x + random.randint(0, width - constants.SMALL_STONE),
                self.y + random.randint(0, height - constants.SMALL_STONE)
            ) for _ in range(10)
        ]

        # Restaurar el estado anterior del generador random
        random.setstate(old_state)

    def draw(self, screen, grass_image, camera_x, camera_y):
        # Dibujar el pasto en este chunk con offset de cámara
        chunk_screen_x = self.x - camera_x
        chunk_screen_y = self.y - camera_y

        # Calcular el rango de tiles de pasto visibles con un tile extra para evitar líneas
        start_x = max(0, (camera_x - self.x - constants.GRASS) // constants.GRASS)
        end_x = min(self.width // constants.GRASS + 1,
                    (camera_x + constants.WIDTH - self.x + constants.GRASS) // constants.GRASS + 1)
        start_y = max(0, (camera_y - self.y - constants.GRASS) // constants.GRASS)
        end_y = min(self.height // constants.GRASS + 1,
                   (camera_y + constants.HEIGHT - self.y + constants.GRASS) // constants.GRASS + 1)

        for y in range(int(start_y), int(end_y)):
            for x in range(int(start_x), int(end_x)):
                tile_x = self.x + x * constants.GRASS
                tile_y = self.y + y * constants.GRASS
                screen_x = tile_x - camera_x
                screen_y = tile_y - camera_y


                tile_key = (tile_x, tile_y)                                
                if tile_key in self.farmland_tiles:
                    self.farmland_tiles[tile_key].draw(screen, camera_x, camera_y)
                else:
                    screen.blit(grass_image, (screen_x, screen_y))

        # Remover elementos agotados
        self.trees = [tree for tree in self.trees if not tree.is_depleted()]
        self.small_stones = [stone for stone in self.small_stones if not stone.is_depleted()]

        # Dibujar elementos solo si están en pantalla
        for stone in self.small_stones:
            stone_screen_x = stone.x - camera_x
            stone_screen_y = stone.y - camera_y
            if (stone_screen_x + stone.size >= 0 and stone_screen_x <= constants.WIDTH and
                stone_screen_y + stone.size >= 0 and stone_screen_y <= constants.HEIGHT):
                stone.draw(screen, camera_x, camera_y)

        for tree in self.trees:
            tree_screen_x = tree.x - camera_x
            tree_screen_y = tree.y - camera_y
            if (tree_screen_x + tree.size >= 0 and tree_screen_x <= constants.WIDTH and
                tree_screen_y + tree.size >= 0 and tree_screen_y <= constants.HEIGHT):
                tree.draw(screen, camera_x, camera_y)


class World:
    def __init__(self, width, height):
        self.chunk_size = constants.WIDTH
        self.active_chunks = {}
        self.inactive_chunks = {}  # Almacena chunks inactivos para persistencia

        self.view_width = width
        self.view_height = height

        # Cargar imagen del pasto
        grass_path = os.path.join('assets', 'images', 'objects', 'grass.png')
        self.grass_image = pygame.image.load(grass_path).convert()
        self.grass_image = pygame.transform.scale(self.grass_image,
                                                  (constants.GRASS, constants.GRASS))

        # Sistema día/noche
        self.current_time = constants.MORNING_TIME  # Comenzar a las 8:00
        self.day_overlay = Surface((width, height))
        self.day_overlay.fill(constants.DAY_COLOR)
        self.day_overlay.set_alpha(0)

        # Generar chunk inicial y adyacentes
        self.generate_chunk(0, 0)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                self.generate_chunk(dx, dy)


    def get_chunk_key(self, x, y):
        """Obtiene la llave del chunk basada en coordenadas globales"""
        chunk_x = x // self.chunk_size
        chunk_y = y // self.chunk_size
        return (chunk_x, chunk_y)

    def generate_chunk(self, chunk_x, chunk_y):
        """Genera un nuevo chunk en las coordenadas especificadas o recupera uno existente"""
        key = (chunk_x, chunk_y)
        if key not in self.active_chunks:
            # Verificar si el chunk existe en inactive_chunks
            if key in self.inactive_chunks:
                # Recuperar el chunk inactivo
                self.active_chunks[key] = self.inactive_chunks[key]
                del self.inactive_chunks[key]
            else:
                # Crear un nuevo chunk si no existe
                x = chunk_x * self.chunk_size
                y = chunk_y * self.chunk_size
                self.active_chunks[key] = WorldChunk(x, y, self.chunk_size, self.chunk_size)

    def update_chunks(self, player_x, player_y):
        """Actualiza los chunks basado en la posición del jugador"""
        current_chunk = self.get_chunk_key(player_x, player_y)

        # Generar chunks adyacentes
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                chunk_x = current_chunk[0] + dx
                chunk_y = current_chunk[1] + dy
                self.generate_chunk(chunk_x, chunk_y)

        # Mover chunks lejanos a inactive_chunks en lugar de eliminarlos
        chunks_to_move = []
        for chunk_key in self.active_chunks:
            distance_x = abs(chunk_key[0] - current_chunk[0])
            distance_y = abs(chunk_key[1] - current_chunk[1])
            if distance_x > 2 or distance_y > 2:  # Aumentado el rango de eliminación
                chunks_to_move.append(chunk_key)

        for chunk_key in chunks_to_move:
            # Mover el chunk a inactive_chunks en lugar de eliminarlo
            self.inactive_chunks[chunk_key] = self.active_chunks[chunk_key]
            del self.active_chunks[chunk_key]


    def update_time(self, dt):
        self.current_time = (self.current_time + dt) % constants.DAY_LENGTH
        alpha = 0
        # Calcular el color y la intensidad basados en la hora del día
        if constants.MORNING_TIME <= self.current_time < constants.DUSK_TIME:
            # Durante el día (8:00 - 18:00)
            self.day_overlay.fill(constants.DAY_COLOR)
            alpha = 0
        elif constants.DAWN_TIME <= self.current_time < constants.MORNING_TIME:
            # Entre 6:00 y 8:00 - Amanecer
            self.day_overlay.fill(constants.NIGHT_COLOR)
            morning_progress = (self.current_time - constants.DAWN_TIME) / (
                        constants.MORNING_TIME - constants.DAWN_TIME)
            alpha = int(constants.MAX_DARKNESS * (1 - morning_progress))
        elif constants.DUSK_TIME <= self.current_time <= constants.MIDNIGHT:
            # Entre 18:00 y 00:00 - Atardecer
            self.day_overlay.fill(constants.NIGHT_COLOR)
            night_progress = (self.current_time - constants.DUSK_TIME) / (constants.MIDNIGHT - constants.DUSK_TIME)
            alpha = int(constants.MAX_DARKNESS * night_progress)
        else:
            # Entre 00:00 y 06:00 - Noche
            self.day_overlay.fill(constants.NIGHT_COLOR)
            alpha = constants.MAX_DARKNESS


        self.day_overlay.set_alpha(alpha)


    def draw(self, screen, camera_x, camera_y):
        # Dibujar todos los chunks activos con offset de cámara
        for chunk in self.active_chunks.values():
            chunk.draw(screen, self.grass_image, camera_x, camera_y)


        # Aplicar el overlay día/noche
        screen.blit(self.day_overlay, (0, 0))

    def draw_inventory(self, screen, character):
        font = pygame.font.Font(None, 24)
        instruction_text = font.render("Press 'I' to open inventory", True, constants.WHITE)
        screen.blit(instruction_text, (10, 10))

    @property
    def trees(self):
        """Retorna todos los árboles de todos los chunks activos"""
        all_trees = []
        for chunk in self.active_chunks.values():
            all_trees.extend(chunk.trees)
        return all_trees

    @property
    def small_stones(self):
        """Retorna todas las piedras de todos los chunks activos"""
        all_stones = []
        for chunk in self.active_chunks.values():
            all_stones.extend(chunk.small_stones)
        return all_stones

    def add_farmland(self, x, y):
        """Añade un tile de tierra cultivada en la posición especificada"""
        # Obtener el chunk correspondiente a la posición
        chunk_key = self.get_chunk_key(x, y)
        chunk = self.active_chunks.get(chunk_key)
        
        if chunk:
            # Alinear la posición a la cuadrícula
            grid_x = (x // constants.GRASS) * constants.GRASS
            grid_y = (y // constants.GRASS) * constants.GRASS
            
            # Verificar si hay árboles o piedras en esta posición
            for tree in chunk.trees:
                if (grid_x < tree.x + tree.size and grid_x + constants.GRASS > tree.x and
                    grid_y < tree.y + tree.size and grid_y + constants.GRASS > tree.y):
                    return False
                    
            for stone in chunk.small_stones:
                if (grid_x < stone.x + stone.size and grid_x + constants.GRASS > stone.x and
                    grid_y < stone.y + stone.size and grid_y + constants.GRASS > stone.y):
                    return False
            
            # Si no hay obstáculos, crear el tile de farmland
            from elements import FarmLand
            tile_key = (grid_x, grid_y)
            if tile_key not in chunk.farmland_tiles:
                chunk.farmland_tiles[tile_key] = FarmLand(grid_x, grid_y)
            return True
        return False
