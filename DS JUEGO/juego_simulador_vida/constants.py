#tamaños
WIDTH, HEIGHT = 1280, 720
PLAYER = 100
GRASS = 64
TREE = 64
SMALL_STONE = 32

#animaciones
BASIC_FRAMES = 6
IDLE_DOWN = 0
IDLE_RIGHT = 1
IDLE_UP = 2
WALK_DOWN = 3
WALK_RIGHT = 4
WALK_UP = 5
FRAME_SIZE = 32
ACTION_FRAME_SIZE = 48
ANIMATION_DELAY = 100
RUNNING_ANIMATION_DELAY = 50

#colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

#barras de estado
MAX_ENERGY = 100
MAX_FOOD = 100
MAX_THIRST = 100
MAX_STAMINA = 100

# Colores para las barras de estado
ENERGY_COLOR = (255, 255, 0)  # Amarillo
FOOD_COLOR = (255, 165, 0)    # Naranja
THIRST_COLOR = (0, 191, 255)  # Azul claro
STAMINA_COLOR = (124, 252, 0) # Verde claro
BAR_BACKGROUND = (100, 100, 100)  # Gris oscuro

# Intervalo de tiempo
STATUS_UPDATE_INTERVAL = 1000


# Sistema día/noche
DAY_LENGTH = 2400000     # Duración del día completo en milisegundos (24 segundos)
DAWN_TIME = 600000      # Amanecer a las 6:00
MORNING_TIME = 800000   # Mañana completa a las 8:00
DUSK_TIME = 1800000     # Atardecer a las 18:00
MIDNIGHT = 2400000      # Medianoche (00:00)
MAX_DARKNESS = 210    # Nivel máximo de oscuridad (0-255)

# Colores para iluminación
NIGHT_COLOR = (20, 20, 50)    # Color azul oscuro para la noche
DAY_COLOR = (255, 255, 255)   # Color blanco para el día
DAWN_DUSK_COLOR = (255, 193, 137)  # Color anaranjado para amanecer/atardecer

# Velocidades de disminución de estados
FOOD_DECREASE_RATE = 0.01      # Velocidad de disminución de comida
THIRST_DECREASE_RATE = 0.02    # Velocidad de disminución de sed
ENERGY_DECREASE_RATE = 0.005  # Velocidad de disminución de energía en estado crítico
ENERGY_INCREASE_RATE = 0.001  # Velocidad de recuperación de energía en estado normal
MOVEMENT_ENERGY_COST = 0.001  # Energía consumida por movimiento

# Nuevas constantes para correr
WALK_SPEED = 5
RUN_SPEED = 8
STAMINA_DECREASE_RATE = 0.05
STAMINA_INCREASE_RATE = 0.02
RUN_FOOD_DECREASE_MULTIPLIER = 2.0
RUN_THIRST_DECREASE_MULTIPLIER = 2.0

# Inventory constants
SLOT_SIZE = 64
HOTBAR_SLOTS = 8
INVENTORY_ROWS = 4
INVENTORY_COLS = 5
MARGIN = 10

# Hotbar position (siempre visible abajo)
HOTBAR_Y = HEIGHT - SLOT_SIZE - MARGIN
HOTBAR_X = (WIDTH - (SLOT_SIZE * HOTBAR_SLOTS)) // 2

# Main inventory position (en el centro cuando está abierto)
INVENTORY_X = (WIDTH - (SLOT_SIZE * INVENTORY_COLS)) // 2
INVENTORY_Y = (HEIGHT - (SLOT_SIZE * INVENTORY_ROWS)) // 2

# Crafting constants
CRAFTING_GRID_SIZE = 2
CRAFTING_RESULT_SLOT_X = INVENTORY_X + (SLOT_SIZE * (INVENTORY_COLS + 1))
CRAFTING_RESULT_SLOT_Y = INVENTORY_Y
CRAFTING_GRID_X = INVENTORY_X + (SLOT_SIZE * (INVENTORY_COLS + 1))
CRAFTING_GRID_Y = INVENTORY_Y + SLOT_SIZE * 2

# Hand slots constants
LEFT_HAND_SLOT_X = HOTBAR_X - SLOT_SIZE - MARGIN
LEFT_HAND_SLOT_Y = HOTBAR_Y
RIGHT_HAND_SLOT_X = HOTBAR_X + (SLOT_SIZE * HOTBAR_SLOTS) + MARGIN
RIGHT_HAND_SLOT_Y = HOTBAR_Y

# Tools animation settings
AXE_COLS = 2   
AXE_FRAMES = 2 
AXE_ANIMATION_DELAY = 200
HOE_COLS = 2
HOE_FRAMES = 2
HOE_ANIMATION_DELAY = 200

# Colors for inventory
SLOT_COLOR = (139, 139, 139)  # Gray
SLOT_BORDER = (100, 100, 100)  # Darker gray
SLOT_HOVER = (160, 160, 160)   # Lighter gray