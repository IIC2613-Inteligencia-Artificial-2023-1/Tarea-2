import parametros as p

"""En este archivo se definen las clases que representan a las entidades del juego."""

# Clase que define a un jugador
class Jugador:
    def __init__(self, color, mode, iq):
        self.color = color
        self.disponibilidad = {i: 0 for i in p.TAMANOS} # Si vale 0 es porque está disponible
        self.puntaje = 0
        self.entrada = 0 if color == "blanco" else -1
        self.mode = mode
        self.iq = iq

# Clase que define cada oveja del juego
class Oveja:
    def __init__(self, color, tamano):
        self.color = color
        self.tamano = tamano
        self.puntaje = p.PUNTAJES[tamano] # Puntaje que da esta oveja
        self.avanzado = True
        self.x = -1
        self.y = -1
    
    def __str__(self):
        return f"{self.color[0]}{self.tamano}"

# Clase que define y contiene toda la información sobre el juego
class Game:
    def __init__(self):
        self.tablero = [["*" for j in range(p.N_COLUMNAS)] for i in range(p.N_FILAS)]
        self.blanco = Jugador("blanco", p.MODE_BLANCO, p.IQ_BLANCO)
        self.negro = Jugador("negro", p.MODE_NEGRO, p.IQ_NEGRO)
        self.turno = self.blanco
        self.objetivo = p.PUNTAJE_OBJETIVO
    
    def nuevo_turno(self):
        if self.turno == self.blanco:
            self.turno = self.negro
        else:
            self.turno = self.blanco
    
    def ganador(self):
        if self.blanco.puntaje > self.negro.puntaje:
            return self.blanco.color
        elif self.blanco.puntaje < self.negro.puntaje:
            return self.negro.color
        else:
            return "Empate"