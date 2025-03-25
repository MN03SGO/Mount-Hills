import pygame
import constants
from constants import *
import os
from inventory import Inventory

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = Inventory()

        # Cargar la hoja de sprite
        image_path = os.path.join('assets', 'images', 'character', 'Player.png')
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()
        # Cargar hoja de sprites de animación del hacha
        self.action_sprite_sheet = pygame.image.load(
            os.path.join('assets', 'images', 'character', 'Player_Actions.png')).convert_alpha()

        # Animation properties
        self.frame_size = FRAME_SIZE
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_delay = ANIMATION_DELAY
        self.current_state = IDLE_DOWN
        self.moving = False
        self.facing_left = False
        self.is_running = False

        # Agregar propiedades de animación del hacha y azada
        self.is_chopping = False
        self.chop_timer = 0
        self.chop_frame = 0
        self.is_hoeing = False
        self.hoe_timer = 0
        self.hoe_frame = 0

        # Load all animation frames
        self.animations = self.load_animations()
        self.axe_animations = self.load_axe_animations()
        self.hoe_animations = self.load_hoe_animations()

        self.item_images = {
            "wood": self.load_item_image("wood.png"),
            "stone": self.load_item_image("small_stone.png")
        }

        self.energy = constants.MAX_ENERGY
        self.food = constants.MAX_FOOD
        self.thirst = constants.MAX_THIRST
        self.stamina = constants.MAX_STAMINA

    def load_animations(self):
        animations = {}
        for state in range(6): # 6 animation states
            frames = []
            for frame in range(BASIC_FRAMES): # 6 frames per animation
                temp_surface = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
                temp_surface.blit(self.sprite_sheet, (0,0),
                             (frame * self.frame_size,
                             state * self.frame_size,
                             self.frame_size,
                             self.frame_size))

                # Create final surface at PLAYER size
                surface = pygame.Surface((constants.PLAYER, constants.PLAYER), pygame.SRCALPHA)
                # Scale and blit the temp surface onto the final surface
                scaled_temp = pygame.transform.scale(temp_surface, (constants.PLAYER, constants.PLAYER))
                surface.blit(scaled_temp, (0, 0))
                
                frames.append(surface)
            animations[state] = frames
        return animations

    def load_axe_animations(self):
        animations = {}
        # Map the sprite sheet rows to animation states
        # Row 4 (index 3) for right-facing
        # Row 5 (index 4) for down-facing
        # Row 6 (index 5) for up-facing
        row_mapping = {
            3: 3,  # Right-facing animations in row 4
            4: 4,  # Down-facing animations in row 5
            5: 5   # Up-facing animations in row 6
        }

        for state, row in row_mapping.items():
            frames = []
            for frame in range(AXE_FRAMES):
                # Create a temporary surface to hold the frame
                temp_surface = pygame.Surface((constants.ACTION_FRAME_SIZE, constants.ACTION_FRAME_SIZE), pygame.SRCALPHA) 
                # Calculate x position based on frame number and columns
                x = (frame % AXE_COLS) * constants.ACTION_FRAME_SIZE
                # Get the frame from the correct position in the sprite sheet
                frame_rect = pygame.Rect(x, row * constants.ACTION_FRAME_SIZE,
                                       constants.ACTION_FRAME_SIZE,
                                       constants.ACTION_FRAME_SIZE)  

                # Draw the frame onto the temporary surface
                temp_surface.blit(self.action_sprite_sheet, (0, 0), frame_rect) 

                # Calculate the proper size for action frames
                action_scale = constants.ACTION_FRAME_SIZE / constants.FRAME_SIZE
                action_size = int(constants.PLAYER * action_scale)

                # Create the final surface at the scaled action size
                surface = pygame.Surface((action_size, action_size), pygame.SRCALPHA)

                # Scale and blit the temp surface onto the final surface
                scaled_temp = pygame.transform.scale(temp_surface, (action_size, action_size))
                surface.blit(scaled_temp, (0, 0))

                frames.append(surface)
            animations[state] = frames
        return animations
    
    def load_hoe_animations(self):
        animations = {}
        # Map the sprite sheet rows to animation states
        # Row 7 (index 6) for right-facing
        # Row 8 (index 7) for down-facing
        # Row 9 (index 8) for up-facing
        row_mapping = {
            6: 6,  # Right-facing animations in row 7
            7: 7,  # Down-facing animations in row 8
            8: 8   # Up-facing animations in row 9
        }

        for state, row in row_mapping.items():
            frames = []
            for frame in range(HOE_FRAMES):
                # Create a temporary surface to hold the frame
                temp_surface = pygame.Surface((constants.ACTION_FRAME_SIZE, constants.ACTION_FRAME_SIZE), pygame.SRCALPHA) 
                # Calculate x position based on frame number and columns
                x = (frame % HOE_COLS) * constants.ACTION_FRAME_SIZE
                # Get the frame from the correct position in the sprite sheet
                frame_rect = pygame.Rect(x, row * constants.ACTION_FRAME_SIZE,
                                       constants.ACTION_FRAME_SIZE,
                                       constants.ACTION_FRAME_SIZE)  

                # Draw the frame onto the temporary surface
                temp_surface.blit(self.action_sprite_sheet, (0, 0), frame_rect) 

                # Calculate the proper size for action frames
                action_scale = constants.ACTION_FRAME_SIZE / constants.FRAME_SIZE
                action_size = int(constants.PLAYER * action_scale)

                # Create the final surface at the scaled action size
                surface = pygame.Surface((action_size, action_size), pygame.SRCALPHA)

                # Scale and blit the temp surface onto the final surface
                scaled_temp = pygame.transform.scale(temp_surface, (action_size, action_size))
                surface.blit(scaled_temp, (0, 0))

                frames.append(surface)
            animations[state] = frames
        return animations

    def update_animation(self):
        current_time = pygame.time.get_ticks()

        if self.is_chopping:
            if current_time - self.chop_timer > AXE_ANIMATION_DELAY:
                self.chop_timer = current_time
                self.chop_frame = (self.chop_frame + 1) % AXE_FRAMES
                if self.chop_frame == 0:  # Animation completed
                    self.is_chopping = False
        elif self.is_hoeing:
            if current_time - self.hoe_timer > HOE_ANIMATION_DELAY:
                self.hoe_timer = current_time
                self.hoe_frame = (self.hoe_frame + 1) % HOE_FRAMES
                if self.hoe_frame == 0:  # Animation completed
                    self.is_hoeing = False
        else:
            # Ajustar la velocidad de animación según si está corriendo o caminando
            animation_speed = RUNNING_ANIMATION_DELAY if self.is_running else ANIMATION_DELAY
            if current_time - self.animation_timer > animation_speed:
                self.animation_timer = current_time
                self.animation_frame = (self.animation_frame + 1) % 6

    def load_item_image(self, filename):
        path = os.path.join('assets', 'images', 'objects', filename)
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (40, 40))

    def draw(self, screen, camera_x, camera_y):
        # Calcular posición en pantalla relativa a la cámara
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y

        if self.is_chopping:
            if self.current_state in [IDLE_RIGHT, WALK_RIGHT]:
                current_frame = self.axe_animations[3][self.chop_frame]  
                if self.facing_left:
                    current_frame = pygame.transform.flip(current_frame, True, False)
            elif self.current_state in [IDLE_DOWN, WALK_DOWN]:
                current_frame = self.axe_animations[4][self.chop_frame]              
            elif self.current_state in [IDLE_UP, WALK_UP]:
                current_frame = self.axe_animations[5][self.chop_frame]  
        elif self.is_hoeing:
            if self.current_state in [IDLE_RIGHT, WALK_RIGHT]:
                current_frame = self.hoe_animations[6][self.hoe_frame]  
                if self.facing_left:
                    current_frame = pygame.transform.flip(current_frame, True, False)
            elif self.current_state in [IDLE_DOWN, WALK_DOWN]:
                current_frame = self.hoe_animations[7][self.hoe_frame]              
            elif self.current_state in [IDLE_UP, WALK_UP]:
                current_frame = self.hoe_animations[8][self.hoe_frame]  
        else:
            current_frame = self.animations[self.current_state][self.animation_frame]
            if self.facing_left:
                current_frame = pygame.transform.flip(current_frame, True, False)
       
        if self.is_chopping or self.is_hoeing:
            action_scale = constants.ACTION_FRAME_SIZE / constants.FRAME_SIZE
            size_diff = int(constants.PLAYER * (action_scale - 1))
            screen.blit(current_frame, (screen_x - size_diff // 2, screen_y - size_diff // 2))
        else:
            screen.blit(current_frame, (screen_x, screen_y))
        self.draw_status_bars(screen)

    def move(self, dx, dy, world):
        self.moving = dx != 0 or dy != 0

        if self.moving:
            # Ajustar velocidad según si está corriendo o caminando
            speed_multiplier = RUN_SPEED if self.is_running and self.stamina > 0 else WALK_SPEED
            dx *= speed_multiplier / WALK_SPEED
            dy *= speed_multiplier / WALK_SPEED
            if dy > 0:
                self.current_state = WALK_DOWN
                self.facing_left = False
            elif dy < 0:
                self.current_state = WALK_UP
                self.facing_left = False
            elif dx > 0:
                self.current_state = WALK_RIGHT
                self.facing_left = False
            elif dx < 0:
                self.current_state = WALK_RIGHT
                self.facing_left = True
        else:
            if self.current_state == WALK_DOWN:
                self.current_state = IDLE_DOWN
            elif self.current_state == WALK_UP:
                self.current_state = IDLE_UP
            elif self.current_state == WALK_RIGHT:
                self.current_state = IDLE_RIGHT


        new_x = self.x + dx
        new_y = self.y + dy

        for tree in world.trees:
            if self.check_collision(new_x, new_y, tree):
                self.moving = False
                return

        self.x = new_x
        self.y = new_y

        self.update_animation()

        # Cuando se mueve pierde energía
        if self.moving:
            if self.is_running and self.stamina > 0:
                self.update_stamina(-STAMINA_DECREASE_RATE)
                self.update_energy(-MOVEMENT_ENERGY_COST * 2)
            else:
                self.update_energy(-MOVEMENT_ENERGY_COST)
                if not self.moving:
                    self.update_stamina(STAMINA_INCREASE_RATE)

    def check_collision(self, x, y, obj):
        return (x < obj.x + obj.size*.75 and x + constants.PLAYER*.75 > obj.x and y < obj.y + obj.size*.75 and
                y + constants.PLAYER*.75 > obj.y)

    def is_near(self, obj):
        return (abs(self.x - obj.x) <= max(constants.PLAYER, obj.size)+5 and
                abs(self.y - obj.y) <= max(constants.PLAYER, obj.size)+5)

    def interact(self, world):
        # Check if 'e' key is pressed and hoe is equipped
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and self.inventory.has_hoe_equipped():
            self.is_hoeing = True
            self.hoe_timer = pygame.time.get_ticks()
            self.hoe_frame = 0
            # Intentar crear tierra de cultivo en la posición actual
            world.add_farmland(self.x, self.y)
            return

        for tree in world.trees:
            if self.is_near(tree):
                has_axe = self.inventory.has_axe_equipped()
                if has_axe:
                    self.is_chopping = True
                    self.chop_timer = pygame.time.get_ticks()
                    self.chop_frame = 0
                if tree.chop(with_axe=has_axe):
                    self.inventory.add_item('wood')
                return

        for stone in world.small_stones:
            if self.is_near(stone):
                if stone.collect():
                    self.inventory.add_item('stone')
                return

    def draw_inventory(self, screen, show_inventory=False):
        # Dibujar el inventario
        self.inventory.draw(screen, show_inventory)

        # Texto de cierre si el inventario está abierto
        if show_inventory:
            font = pygame.font.Font(None, 24)
            close_text = font.render("Press 'I' to close inventory", True, constants.WHITE)
            screen.blit(close_text, (constants.WIDTH // 2 - close_text.get_width() // 2, constants.HEIGHT - 40))



    def update_energy(self, amount):
        self.energy = max(0, min(self.energy + amount, constants.MAX_ENERGY))

    def update_food(self, amount):
        self.food = max(0, min(self.food + amount, constants.MAX_FOOD))

    def update_thirst(self, amount):
        self.thirst = max(0, min(self.thirst + amount, constants.MAX_THIRST))

    def update_stamina(self, amount):
        self.stamina = max(0, min(self.stamina + amount, constants.MAX_STAMINA))

    def draw_status_bars(self, screen):
        bar_width = 100
        bar_height = 10
        x_offset = 10
        y_offset = 10

        # Energy bar
        pygame.draw.rect(screen, constants.BAR_BACKGROUND,
                         (x_offset, y_offset, bar_width, bar_height))

        pygame.draw.rect(screen, constants.ENERGY_COLOR,
                         (x_offset, y_offset, bar_width * (self.energy / constants.MAX_ENERGY), bar_height))

        # Food bar
        y_offset += 15
        pygame.draw.rect(screen, constants.BAR_BACKGROUND, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, constants.FOOD_COLOR,
                                  (x_offset, y_offset, bar_width * (self.food / constants.MAX_FOOD), bar_height))

        # Thirst bar
        y_offset += 15
        pygame.draw.rect(screen, constants.BAR_BACKGROUND, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, constants.THIRST_COLOR,
                            (x_offset, y_offset,
                             bar_width * (self.thirst / constants.MAX_THIRST), bar_height))

        # Stamina bar
        y_offset += 15
        pygame.draw.rect(screen, constants.BAR_BACKGROUND, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, constants.STAMINA_COLOR,
                         (x_offset, y_offset,
                          bar_width * (self.stamina / constants.MAX_STAMINA), bar_height))

    def update_status(self):
        # Aplicar multiplicadores si está corriendo
        food_rate = FOOD_DECREASE_RATE * (RUN_FOOD_DECREASE_MULTIPLIER if self.is_running else 1)
        thirst_rate = THIRST_DECREASE_RATE * (RUN_THIRST_DECREASE_MULTIPLIER if self.is_running else 1)

        self.update_food(-constants.FOOD_DECREASE_RATE)
        self.update_thirst(-constants.THIRST_DECREASE_RATE)

        if self.food < constants.MAX_FOOD * 0.2 or self.thirst < constants.MAX_THIRST * 0.2:
            self.update_energy(-constants.ENERGY_DECREASE_RATE)
        else:
            self.update_energy(constants.ENERGY_INCREASE_RATE)

        # Recuperar stamina cuando no está corriendo
        if not self.is_running:
            self.update_stamina(STAMINA_INCREASE_RATE)
