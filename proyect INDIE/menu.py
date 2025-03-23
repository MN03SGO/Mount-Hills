import pygame
import sys
import constants
from caracteres import Caracteres
from mundo import Mundo
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
ventana = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DEMO JUEGO DS")

def Spawn_Personaje(mundo):
    #Spawnea personae en liugar libre de arbol

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

def main():
    clock = pygame.time.Clock()
    mundo = Mundo(constants.WIDTH, constants.HEIGHT)

    #Para que aparesca el personaje
    safe_x, safe_y = Spawn_Personaje(mundo)
    caracteres = Caracteres(safe_x, safe_y)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            caracteres.move(-5, 0, mundo)
        if keys[pygame.K_d]:
            caracteres.move(5, 0, mundo)
        if keys[pygame.K_w]:
            caracteres.move(0, -5, mundo)
        if keys[pygame.K_s]:
            caracteres.move(0, 5, mundo)

        ventana.fill(constants.WHITE)
        mundo.draw(ventana)
        caracteres.draw(ventana)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
