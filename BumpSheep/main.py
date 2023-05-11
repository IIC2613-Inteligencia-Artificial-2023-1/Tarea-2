import random
import utils
from entidades import Game
from minimax import minimax
import parametros as p
import pygame
import os
import time


"""Archivo donde se maneja el funcionamiento del juego"""

# Función que maneja el juego
def juego(game, vis=False):
    # Adaptación del juego por turnos
    if vis:
        # Se usa para establecer cuan rápido se actualiza la pantalla
        reloj = pygame.time.Clock()
        windowSurface = pygame.display.set_mode((p.WINDOWWIDTH, p.WINDOWHEIGHT))

        # creamos las imagenes
        backgroundImage = pygame.image.load(os.path.join('img','background.png'))
        rescaledBackground = pygame.transform.scale(backgroundImage, (p.WINDOWWIDTH, p.WINDOWHEIGHT))

        windowSurface.blit(rescaledBackground, (0, 0))

    hecho = False
    
    while not hecho:
        print(f"Puntaje Blanco: {game.blanco.puntaje}")
        print(f"Puntaje Negro: {game.negro.puntaje}")
        print(f"Turno {game.turno.color}")

        # Revisamos la disponibilidad de ovejas y filas
        ovejas_disponibles, filas_disponibles = utils.disponibilidades(game)

        if not vis: # SIN la visualización de pygame
            # Mostrar el tablero
            for i, fila in enumerate(game.tablero):
                print(f"{i+1} [{' '.join([str(i) for i in fila])}]")

            # Mostramos la disponibilidad de ovejas y filas
            print(f"Ovejas disponibles: {' '.join(ovejas_disponibles[:-1])}")
            print(f"Filas disponibles: {' '.join(filas_disponibles)}")

            # Poner oveja manualmente (si corresponde)
            if game.turno.mode == "player":
                fila = "0"
                while fila == "0":
                    tamano = input("Selecciona una oveja disponible o 0 para no jugar este turno: ")
                    while tamano not in ovejas_disponibles:
                        tamano = input("Oveja inválida, selecciona una oveja disponible o 0 para no jugar este turno: ")
                    
                    if tamano == "0":
                        break

                    fila = input("Selecciona una fila o 0 para seleccionar otra oveja: ")
                    while fila not in filas_disponibles and fila != "0":
                        fila = input("Fila invalida, introduce una fila o 0 para seleccionar otra oveja: ")

        else: # CON la visualización de pygame
            # Actualizamos la visualizacion
            vis.actualizar(ovejas_disponibles, filas_disponibles, game)
            # Repetir hasta que el usuario ingrese una movida 
            # (a menos que no se esté jugando en modo "player")
            while not vis.respondido:
                # Salir del loop si no se está jugando manualmente
                if game.turno.mode != "player":
                    vis.respondido = True
                
                # borramos todo (volvemos a dibujar el fondo)
                screen.blit(rescaledBackground, (0, 0))
                
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT: 
                        hecho = True
                if hecho: 
                    break
                
                # revisamos los botones y los dibujamos
                for b in vis.botones:
                    b.process(vis)
                for s in vis.seleccion_ovejas:
                    s.process(vis)
                vis.mostrar_puntajes()

                # dibujamos las ovejas
                vis.procesar_ovejas()
                
                # Avanzamos y actualizamos la pantalla con lo que hemos dibujado.
                pygame.display.flip()

                # Limitamos a 60 fotogramas por segundo (frames per second)
                reloj.tick(p.FPS)
            
            # Descomentar si quieren ver el juego corriendo más lentamente para poder entenderlo
            # time.sleep(2)
            fila = vis.respondido
            vis.respondido = False

            for s in vis.seleccion_ovejas:
                if s.seleccionado:
                    tamano = s.tamano
                s.seleccionado = False
        
        # Poner oveja automáticamente (cuando corresponda)
        if game.turno.mode == "random":
                tamano = random.choice(ovejas_disponibles)
                fila = random.choice(filas_disponibles)
            
        elif game.turno.mode == "minimax":
            move, score = minimax(game, game.turno.iq)
            tamano, fila = move

        # Se ejecuta la jugada y se prepara la siguiente
        utils.ejecutar_jugada(game, tamano, fila)

        if (game.blanco.puntaje >= game.objetivo or game.negro.puntaje >= game.objetivo):
            hecho = True
    
    
    # Se muestran los puntajes y al ganador
    print(f"Puntaje Blanco: {game.blanco.puntaje}")
    print(f"Puntaje Negro: {game.negro.puntaje}")
    print(f"Ganador: {game.ganador()}")

if __name__ == "__main__":
    # Se corre el juego
    if not p.VIS:
        juego(Game())
    else:
        pygame.init()
        dimensiones = [p.WINDOWWIDTH, p.WINDOWHEIGHT]
        screen = pygame.display.set_mode(dimensiones) 
        pygame.display.set_caption("Bump Sheep")

        import visualizacion as vis_file
        vis = vis_file.Visualizacion(screen)
        juego(Game(), vis)

        pygame.quit()