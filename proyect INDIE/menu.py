import pygame
import sys
import constants
from caracteres import Caracteres
from mundo import Mundo
import random
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
ventana = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DEMO JUEGO DS")

# Cargar música de fondo
musica_ruta = "assets/img/Musica/sonido.wav"
if os.path.exists(musica_ruta):
    pygame.mixer.music.load(musica_ruta)
    pygame.mixer.music.set_volume(0.5)  # Ajustar volumen
    pygame.mixer.music.play(-1)  # Reproducir en bucle
else:
    print(f"Error: No se encontró el archivo de música en {musica_ruta}")


def Spawn_Personaje(mundo):
    while True:
        x = random.randint(0, constants.WIDTH - constants.PERSONAJE)
        y = random.randint(0, constants.HEIGHT - constants.PERSONAJE)
        overlap = False
        for arbol in mundo.arboles:
            if x < arbol.x + arbol.size and x + constants.PERSONAJE > arbol.x and y < arbol.y + arbol.size and y + constants.PERSONAJE > arbol.y:
                overlap = True
                break
        for piedra in mundo.piedras:
            if x < piedra.x + piedra.size and x + constants.PERSONAJE > piedra.x and y < piedra.y + piedra.size and y + constants.PERSONAJE > piedra.y:
                overlap = True
                break
        if not overlap:
            return x, y


def mostrar_menu_pausa():
    fuente = pygame.font.Font(None, 50)
    texto_continuar = fuente.render("Presiona ESC para continuar", True, (255, 255, 255))
    texto_salir = fuente.render("Presiona Q para salir", True, (255, 255, 255))
    
    ventana.fill((0, 0, 0))
    ventana.blit(texto_continuar, (WIDTH//2 - texto_continuar.get_width()//2, HEIGHT//2 - 50))
    ventana.blit(texto_salir, (WIDTH//2 - texto_salir.get_width()//2, HEIGHT//2 + 10))
    pygame.display.flip()

    pausado = True
    while pausado:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pausado = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def main():
    clock = pygame.time.Clock()
    mundo = Mundo(constants.WIDTH, constants.HEIGHT)

    safe_x, safe_y = Spawn_Personaje(mundo)
    caracteres = Caracteres(safe_x, safe_y)
    inventario = False

    status_update_timer = 0

    while True:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    caracteres.interact(mundo)
                if event.key == pygame.K_i:
                    inventario = not inventario
                if event.key == pygame.K_f:
                    caracteres.actualizar_Hambre(20)
                if event.key == pygame.K_t:
                    caracteres.actualizar_Sed(20)
                if event.key == pygame.K_ESCAPE:
                    mostrar_menu_pausa()

        keys = pygame.key.get_pressed()
        move_x = 0
        move_y = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move_x = -5
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move_x = 5
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move_y = -5
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move_y = 5
        caracteres.move(move_x, move_y, mundo)

        status_update_timer += dt
        if status_update_timer > constants.STATUS_UPDATE_TIME:
            caracteres.actualizar_Hambre(-1)
            caracteres.actualizar_Sed(-1)
            status_update_timer = 0

        if caracteres.energia == 0 or caracteres.hambre == 0 or caracteres.sed == 0:
            print("Has muerto")
            pygame.quit()
            sys.exit()

        ventana.fill(constants.WHITE)
        mundo.draw(ventana)
        caracteres.draw(ventana)

        if inventario:
            caracteres.draw_inventario(ventana)

        font = pygame.font.Font(None, 24)
        texto_energia = font.render(f"Energia: {int(caracteres.energia)}", True, constants.WHITE)
        texto_hambre = font.render(f"Hambre: {int(caracteres.hambre)}", True, constants.WHITE)
        texto_sed = font.render(f"Sed: {int(caracteres.sed)}", True, constants.WHITE)

        ventana.blit(texto_energia, (10, constants.HEIGHT - 70))
        ventana.blit(texto_hambre, (10, constants.HEIGHT - 45))
        ventana.blit(texto_sed, (10, constants.HEIGHT - 20))

        pygame.display.flip()


if __name__ == "__main__":
    main()
