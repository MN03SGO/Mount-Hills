import pygame, sys
from botones_menu import Button
import subprocess  # Para ejecutar el archivo de indicaciones

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/img/Menu/Background.png")

def get_font(size):
    return pygame.font.Font("assets/img/Fuente/font.ttf", size)

def play():
    pygame.quit()  # Cierra el menú antes de lanzar el juego
    import menu    # Importa y lanza el juego
    menu.main()

def options():
    # Ejecuta el archivo indicaciones.py en una nueva ventana
    subprocess.Popen(["python", "indicaciones.py"])

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/img/Menu/Play Rect.png"), pos=(640, 250), 
                            text_input="JUGAR", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/img/Menu/Options Rect.png"), pos=(640, 400), 
                            text_input="OPCIONES", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/img/Menu/Quit Rect.png"), pos=(640, 550), 
                            text_input="SALIR", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()  # Llama al juego
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()  # Abre la ventana de indicaciones
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()