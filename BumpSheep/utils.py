from entidades import Oveja
from parametros import ENFRIAMIENTOS

"""Este archivo contiene funciones importantes para el funcionamiento del juego."""

# Función que permite ver hacia donde va a avanzar un choque de ovejas
def calcular_fuerza(fila, inicio, fin):
    fuerza_intervalo1 = sum([int(i.tamano) for i in fila[inicio:fin+1]])
    fuerza_intervalo2 = 0
    final_intervalo2 = fin+1
    for i in range(fin+1, len(fila)):
        if fila[i] != "*" and fila[i].avanzado == False:
            fuerza_intervalo2 += int(fila[i].tamano)
            if i == len(fila)-1:
                final_intervalo2 = i
        elif fila[i] == "*" or fila[i].avanzado == True:
            final_intervalo2 = i-1
            break
    if fuerza_intervalo1 > fuerza_intervalo2:
        return "blanco", final_intervalo2
    elif fuerza_intervalo1 < fuerza_intervalo2:
        return "negro", final_intervalo2
    else:
        return False, final_intervalo2


# Función que avanza las ovejas del tablero
def avanzar_ovejas(game):
    intervalos = []
    for fila in game.tablero:
        inicio = 0 # inicio de intervalo de ovejas del mismo color consecutivas
        fin = 0 # fin de intervalo de ovejas del mismo color consecutivas
        color = "" # color del intervalo de ovejas

        # Se buscan intervalos de ovejas del mismo color
        for j, elem in enumerate(fila):
            if elem != "*" and color == "" and elem.avanzado == False:
                inicio = j
                color = elem.color
                if j == len(fila)-1:
                    fin = j
                    intervalos.append((fila, inicio, fin, color))
            elif color != "" and (elem == "*" or (j == len(fila)-1 and elem.avanzado == True)):
                fin = j-1
                intervalos.append((fila, inicio, fin, color))
                color = ""
            elif color != "" and color != elem.color:
                fin = j-1
                intervalos.append((fila, inicio, fin, color))
                inicio = j
                color = elem.color
            elif color != "" and j == len(fila)-1 and elem.avanzado == False:
                fin = j
                intervalos.append([fila, inicio, fin, color])

    # Se mueven las ovejas
    for intervalo in reversed(intervalos):
        fila = intervalo[0]
        inicio = intervalo[1]
        fin = intervalo[2]
        color = intervalo[3]

        if color == "blanco":
            # Caso borde
            if fin == len(fila)-1:
                game.blanco.puntaje += fila[fin].puntaje
                fila[fin] = "*"
                fin -= 1
            
            elif fila[fin+1] == "*":
                for i in reversed(range(inicio, fin+1)):
                    fila[i].avanzado = True
                    fila[i+1] = fila[i]
                    fila[i] = "*"
            
            # Si hay un choque de intervalos se ve cual gana
            elif fila[fin+1] != "*" and fila[fin+1].avanzado == False:
                ganador, final_intervalo = calcular_fuerza(fila, inicio, fin)

                # Se avanza hacia el lado del intervalo más débil
                if ganador == "blanco":
                    if final_intervalo == len(fila)-1:
                        game.blanco.puntaje += fila[final_intervalo].puntaje # Si una oveja contraria se devuelve, se obtiene el puntaje
                        fila[final_intervalo] = "*"
                        final_intervalo -= 1
                    if fila[final_intervalo+1] == "*":
                        for i in reversed(range(inicio, final_intervalo+1)):
                            fila[i+1] = fila[i]
                            fila[i].avanzado = True
                            fila[i] = "*"
                if ganador == "negro":
                    if inicio == 0:
                        game.negro.puntaje += fila[0].puntaje # Si una oveja contraria se devuelve, se obtiene el puntaje
                        fila[0] = "*"
                        inicio += 1
                    if fila[inicio-1] == "*":
                        for i in range(inicio, final_intervalo+1):
                            fila[i-1] = fila[i]
                            fila[i].avanzado = True
                            fila[i] = "*"
        
        elif color == "negro":
            # Caso borde
            if inicio == 0:
                game.negro.puntaje += fila[inicio].puntaje
                fila[inicio] = "*"
                inicio += 1
            
            elif fila[inicio-1] == "*":
                for i in range(inicio, fin+1):
                    fila[i].avanzado = True
                    fila[i-1] = fila[i]
                    fila[i] = "*"
        
        intervalos.pop(intervalos.index(intervalo))


# Función que retorna todas las filas que no pueden ingresar ovejas
def filas_no_disponibles(game):
    filas_no_disponibles = []
    for fila in range(len(game.tablero)):

        # Si la entrada está tapada puede que la fila no pueda ingresar ovejas por ese lado
        if game.tablero[fila][game.turno.entrada] != "*":
            if game.turno.color == "blanco":
                # Si en la entrada de una oveja blanca hay una negra, no puede ingresar
                if game.tablero[fila][game.turno.entrada].color == "negro":
                    filas_no_disponibles.append(fila+1)

                # Si hay un choque de ovejas y están ganando las negras, no se puede ingresar
                else:
                    for index, elem in enumerate(game.tablero[fila]):
                        if elem != "*" and elem.color == "negro":
                            ganador, f = calcular_fuerza(game.tablero[fila], 0, index-1)
                            if ganador == "negro" or ganador == False:
                                filas_no_disponibles.append(fila+1)
                            break
                                
            else:
                # Si en la entrada de una oveja negra hay una blanca, no puede ingresar
                if game.tablero[fila][game.turno.entrada].color == "blanco":
                    filas_no_disponibles.append(fila+1)

                # Si hay un choque de ovejas y están ganando las blancas, no se puede ingresar
                else:
                    final_intervalo = -1
                    reversed_fila = reversed(list(enumerate(game.tablero[fila])))
                    for index, elem in reversed_fila:
                        if elem != "*" and elem.color == "blanco" and final_intervalo == -1:
                            final_intervalo = index
                        if (elem == "*" and final_intervalo != -1) or (elem != "*" and index == 0):
                            if elem != "*" and index == 0:
                                index = -1
                            ganador, f = calcular_fuerza(game.tablero[fila], index+1, final_intervalo)
                            if ganador == "blanco" or ganador == False:
                                filas_no_disponibles.append(fila+1)
                            break

    return filas_no_disponibles


# Función que retorna las ovejas y filas disponibles para ingresar
def disponibilidades(game):
    ovejas_disponibles = list(filter(lambda x: game.turno.disponibilidad[x] == 0, game.turno.disponibilidad.keys()))
    ovejas_disponibles.append("0")
    filas_excluidas = filas_no_disponibles(game)
    filas_disponibles = [str(i) for i in range(1, len(game.tablero)+1) if i not in filas_excluidas]
    return ovejas_disponibles, filas_disponibles


# Función que ejecuta una jugada y prepara el tablero para el siguiente turno
def ejecutar_jugada(game, oveja, fila):
    if oveja == "0":
        # Si no se ingresa una oveja, solo se avanzan las que ya están
        avanzar_ovejas(game)
    else:
        # Se avanzan las ovejas y se ingresa la nueva
        fila = int(fila)-1
        game.tablero[fila][game.turno.entrada] = Oveja(game.turno.color, oveja)
        avanzar_ovejas(game)
        game.turno.disponibilidad[oveja] = ENFRIAMIENTOS[oveja]
    
    game.nuevo_turno()

    # Todos las ovejas del tablero se marcan como no avanzadas
    for fila in game.tablero:
        for elem in fila:
            if elem != "*":
                elem.avanzado = False

    # Todos los enfriamientos del jugador del turno se reducen en 1
    for key in game.turno.disponibilidad.keys():
        if game.turno.disponibilidad[key] > 0:
            game.turno.disponibilidad[key] -= 1
