import pygame
import sys
import constants
from caracteres import Caracteres
from mundo import Mundo

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = 800, 600 #PANTALLA EN RECUADRO DE 800 x 600


#WIDTH, HEIGHT = info.current_w, info.current_h  # (1-Pantalla completa)
#ventana = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN) # (1-Pantalla completa, para acitvar solo descomenta esta linea y comenta la  otra de 800 x 600)

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





            # (salir del modo pantalla completa con la tecla ESC)
            #if event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_ESCAPE:
                    #pygame.quit()
                    #sys.exit()

        ventana.fill(constants.WHITE)
        mundo.draw(ventana)
        caracteres.draw(ventana)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()


# LINEAS COMENTADAS PARA PANTALLA COMPLETA
# -- Si queres trabajar en modo pantalla completa y probar los designe en mejor vision descomenta las lineas y comentas las lineas relacionadas a 800 x 600
# --Tambien el evento de salir en pantalla completa con ESC
# CUALQUIER, INTEGRACION O OTRA POR EL ESTILO ME AVISAS.
# by sigaran