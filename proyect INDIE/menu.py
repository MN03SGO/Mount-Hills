import pygame
import sys
import constants
from caracteres import Caracteres
from mundo import Mundo


pygame.init()

info = pygame.display.Info()


WIDTH, HEIGHT = info.current_w, info.current_h  #-Pantalla completa)
ventana = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("DEMO JUEGO DS")

def main():
    clock = pygame.time.Clock()
    mundo = Mundo(constants.WIDTH, constants.HEIGHT)
    caracteres = Caracteres(constants.WIDTH // 2, constants.HEIGHT // 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
        #SECCION DE MOVIMIENTO DE PERSONAJE
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            caracteres.move(-5, 0)
        if keys[pygame.K_RIGHT]:
            caracteres.move(5, 0)
        if keys[pygame.K_UP]:
            caracteres.move(0, -5)
        if keys[pygame.K_DOWN]:
            caracteres.move(0, 5)
        # ------------


        ventana.fill(constants.WHITE)
        mundo.draw(ventana)
        caracteres.draw(ventana)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()



# BY SIGARAN