import pygame
import sys
import constants
from caracteres import Caracteres
from mundo import Mundo

pygame.init()
WIDTH, HEIGHT = 800, 600

ventana = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DEMO JUEGO DS")

def main():
    clock = pygame.time.Clock()
    mundo = Mundo(constants.WIDTH, constants.HEIGHT)
    caracteres = Caracteres(constants.WIDTH // 2, constants.HEIGHT // 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        ventana.fill(constants.WHITE)
        mundo.draw(ventana)
        caracteres.draw(ventana)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()