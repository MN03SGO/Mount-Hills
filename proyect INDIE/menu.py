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
    
    inventario = False

    #INTERACCIONES
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    caracteres.interact(mundo)
                if event.key == pygame.K_i:
                    inventario = not inventario


        # iNTERACCION TECLAS DE MOVIMIENTO
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
    

        ventana.fill(constants.WHITE)
        mundo.draw(ventana)
        caracteres.draw(ventana)

        if inventario:
            caracteres.draw_inventario(ventana)
        


        

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()