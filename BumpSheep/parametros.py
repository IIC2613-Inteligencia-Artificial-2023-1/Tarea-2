"""En este archivo se definirán las constantes del juego."""

TAMANOS = [str(i) for i in range(1, 6)]
PUNTAJES = {i: (2*int(i)-1) for i in TAMANOS}
ENFRIAMIENTOS = {i: (2*int(i)) for i in TAMANOS}
N_FILAS = 5 # Con visualización dejar 5 filas
N_COLUMNAS = 13 # Con visualización dejar 13 columnas
PUNTAJE_OBJETIVO = 100

# Constantes que definen la forma de jugar de los jugadores (minimax, random o player)
MODE_BLANCO = "player"
MODE_NEGRO = "player"
IQ_BLANCO = 3
IQ_NEGRO = 3

# Mostrar o no mostrar la visualización del juego
VIS = True

WINDOWWIDTH = 1200
WINDOWHEIGHT = 600
FPS = 60
