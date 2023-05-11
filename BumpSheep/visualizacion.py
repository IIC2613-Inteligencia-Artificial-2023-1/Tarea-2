import pygame
from main import juego
import os
import threading

# creamos los botones
class Button:
    def __init__(self, x, y, width, height, pista, screen, onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.disabled = False
        self.pista = pista
        self.screen = screen

        # creamos las imágenes que representan nuestros botones
        self.image = pygame.image.load(os.path.join('img','go_button.png'))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.image_hovered = pygame.image.load(os.path.join('img','go_button_hover.png'))
        self.image_hovered = pygame.transform.scale(self.image_hovered, (self.width, self.height))

        self.image_disabled = pygame.image.load(os.path.join('img','go_button_disabled.png'))
        self.image_disabled = pygame.transform.scale(self.image_disabled, (self.width, self.height))

        self.image_pressed = pygame.image.load(os.path.join('img','go_button_pressed.png'))
        self.image_pressed = pygame.transform.scale(self.image_pressed, (self.width, self.height))

        self.images = {
            'normal': self.image,
            'hovered': self.image_hovered,
            'pressed': self.image_pressed,
            'disabled': self.image_disabled,
        }

        self.buttonRect = self.image.get_rect()
        self.buttonRect.x = self.x
        self.buttonRect.y = self.y

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.alreadyPressed = False


    def process(self, vis):
        hay_seleccion = False
        for s in vis.seleccion_ovejas:
            if s.seleccionado:
                hay_seleccion = True

        mousePos = pygame.mouse.get_pos()
        if self.disabled or not hay_seleccion:
            self.buttonSurface = self.images['disabled']
        else:
            self.buttonSurface = self.images['normal']
            if self.buttonRect.collidepoint(mousePos):
                self.buttonSurface = self.images['hovered']
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self.buttonSurface = self.images['pressed']

                    if self.onePress:
                        self.onclickFunction(vis, self.pista)

                    elif not self.alreadyPressed:
                        self.onclickFunction(vis, self.pista)
                        self.alreadyPressed = True

                else:
                    self.alreadyPressed = False

        self.screen.blit(self.buttonSurface, self.buttonRect)

class OvejaSelection:

    def __init__(self, color, tamano, x, y, height, width, screen):
        self.color = color
        self.tamano = tamano
        self.disponible = True
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.disabled = False
        self.seleccionado = False
        self.screen = screen

        # creamos las imágenes que representan nuestros botones
        if self.tamano != "0":
            self.image = pygame.image.load(os.path.join('img','sheep',f'{self.color}{self.tamano}.png'))
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

            self.image_disabled = pygame.image.load(os.path.join('img','sheep',f'{self.color}{self.tamano}_disabled.png'))
            self.image_disabled = pygame.transform.scale(self.image_disabled, (self.width, self.height))

            self.image_pressed = pygame.image.load(os.path.join('img','sheep',f'selected_{self.color}{self.tamano}.png'))
            self.image_pressed = pygame.transform.scale(self.image_pressed, (self.width, self.height))
        
        elif self.tamano == "0":
            self.image = pygame.image.load(os.path.join('img', 'skip.png'))
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

            self.image_disabled = pygame.image.load(os.path.join('img', 'skip.png'))
            self.image_disabled = pygame.transform.scale(self.image_disabled, (self.width, self.height))

            self.image_pressed = pygame.image.load(os.path.join('img', 'skip_pressed.png'))
            self.image_pressed = pygame.transform.scale(self.image_pressed, (self.width, self.height))


        self.images = {
            'normal': self.image,
            'hovered': self.image_pressed,
            'pressed': self.image_pressed,
            'disabled': self.image_disabled,
        }

        self.sheepRect = self.image.get_rect()
        self.sheepRect.x = self.x
        self.sheepRect.y = self.y

        self.sheepSurface = pygame.Surface((self.width, self.height))
        self.alreadyPressed = False

        
    def process(self, vis):

        mousePos = pygame.mouse.get_pos()
        if self.disabled:
            self.sheepSurface = self.images['disabled']
        elif self.seleccionado:
            self.sheepSurface = self.images['pressed']
        else:
            self.sheepSurface = self.images['normal']
            if self.sheepRect.collidepoint(mousePos):
                self.sheepSurface = self.images['hovered']
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self.sheepSurface = self.images['pressed']

                    if not self.alreadyPressed:
                        for s in vis.seleccion_ovejas:
                            s.seleccionado = False      
                        self.seleccionado = True
                        self.alreadyPressed = True
                        if self.tamano == "0":
                            boton_presionado(vis, "0")
                else:
                    self.alreadyPressed = False

        self.screen.blit(self.sheepSurface, self.sheepRect)


class Visualizacion:

    def __init__(self, screen):
        self.screen = screen

        self.botones = []
        self.seleccion_ovejas = []
        self.actualizar_botones("blanco")

        # labels para mostrar los puntajes
        self.font = pygame.font.SysFont('Arial', 20)

        self.label_b = self.font.render('puntaje blanco', True, (0,0,0))
        self.label_n = self.font.render('puntaje negro', True, (0,0,0))
        self.puntaje_b = self.font.render('0', True, (0,0,0))
        self.puntaje_n = self.font.render('0', True, (0,0,0))

        self.rect_label_b = self.label_b.get_rect()
        self.rect_label_n = self.label_n.get_rect()
        self.rect_b = self.puntaje_b.get_rect()
        self.rect_n = self.puntaje_n.get_rect()

        self.rect_label_b.center = (100, 40)
        self.rect_label_n.center = (1120, 40)
        self.rect_b.center = (100, 70)
        self.rect_n.center = (1120, 70)


        self.ovejas = []

        self.images = {} # diccionario de la forma:
        #                     # llave: tupla (tamano, color)
        #                     # valor: imagen de la oveja

        self.pos_x = range(88, 1200, 82)
        self.pos_y = [115, 210, 305, 410, 500]
        
        self.tamanos = [55,55,55,55,55] # tamaño de cada tamaño de oveja (cuadrado)

        for tamano in range(1,6): # tamano de la oveja
            img_b = pygame.image.load(os.path.join('img','sheep',f'blanco{tamano}.png'))
            self.images[(str(tamano), "blanco")] = pygame.transform.scale(img_b, (self.tamanos[tamano-1], self.tamanos[tamano-1]))
            img_n = pygame.image.load(os.path.join('img','sheep',f'negro{tamano}.png'))
            self.images[(str(tamano), "negro")] = pygame.transform.scale(img_n, (self.tamanos[tamano-1], self.tamanos[tamano-1]))

        self.respondido = False

    def actualizar_botones(self, color):
        
        if color == "blanco":
            boton_x = 10
        else:
            boton_x = 1135

        x_skip = 210 if color == "blanco" else 910

        boton1 = Button(boton_x, 115, 60, 80, "1", self.screen, boton_presionado)
        boton2 = Button(boton_x, 210, 60, 80, "2", self.screen, boton_presionado)
        boton3 = Button(boton_x, 305, 60, 80, "3", self.screen, boton_presionado)
        boton4 = Button(boton_x, 400, 60, 80, "4", self.screen, boton_presionado)
        boton5 = Button(boton_x, 495, 60, 80, "5", self.screen, boton_presionado)

        sel0 = OvejaSelection(color, "0", x_skip, 35, 47, 118, self.screen)
        sel1 = OvejaSelection(color, "1", 370, 35, 50, 50, self.screen)
        sel2 = OvejaSelection(color, "2", 480, 30, 55, 55, self.screen)
        sel3 = OvejaSelection(color, "3", 585, 25, 60, 60, self.screen)
        sel4 = OvejaSelection(color, "4", 690, 25, 60, 60, self.screen)
        sel5 = OvejaSelection(color, "5", 790, 15, 75, 75, self.screen)

        self.botones = [boton1, boton2, boton3, boton4, boton5]
        self.seleccion_ovejas = [sel0, sel1, sel2, sel3, sel4, sel5]

    def mostrar_puntajes(self):
        self.screen.blit(self.label_b, self.rect_label_b)
        self.screen.blit(self.label_n, self.rect_label_n)
        self.screen.blit(self.puntaje_b, self.rect_b)
        self.screen.blit(self.puntaje_n, self.rect_n)
        pass
    
    def actualizar_puntajes(self, game):
        self.puntaje_b = self.font.render(str(game.blanco.puntaje), True, (0,0,0))
        self.puntaje_n = self.font.render(str(game.negro.puntaje), True, (0,0,0))
        pass

    def ovejas_disponibles(self, ovejas_disponibles):
        for s in self.seleccion_ovejas:
            if str(s.tamano) in ovejas_disponibles:
                s.disabled = False
            else:
                s.disabled = True

    def pistas_disponibles(self, pistas_disponibles):
        for b in self.botones:
            if str(b.pista) in pistas_disponibles:
                b.disabled = False
            else:
                b.disabled = True
    
    def posicionar_ovejas(self, game):
        self.ovejas = []
        for i, fila in enumerate(game.tablero):
            for j, celda in enumerate(fila):
                if celda != "*":
                    if celda not in self.ovejas:
                        self.ovejas.append(celda)
                    celda.x = self.pos_x[j]
                    celda.y = self.pos_y[i]
    
    def procesar_ovejas(self):
        for o in self.ovejas:
            img = self.images[(o.tamano, o.color)]
            sheepRect = img.get_rect()
            sheepRect.x = o.x
            sheepRect.y = o.y
            self.screen.blit(img, sheepRect)

    def agregar_oveja(self, oveja):
        oveja.image = pygame.image.load(os.path.join('img','sheep',f'{oveja.color}{oveja.tamano}.png'))
        oveja.image = pygame.transform.scale(oveja.image, (self.tamanos[int(oveja.tamano)-1], self.tamanos[int(oveja.tamano)-1]))
        self.ovejas.append(oveja)
        
    def actualizar(self, ovejas_disponibles, pistas_disponibles, game):
        self.actualizar_botones(game.turno.color)

        # Actualizar disponibilidades
        self.ovejas_disponibles(ovejas_disponibles)
        self.pistas_disponibles(pistas_disponibles)

        # Actualizar posicion ovejas
        self.posicionar_ovejas(game)

        # Actualizar los puntajes del juego
        self.actualizar_puntajes(game)
        

                    




def boton_presionado(vis, pista): # indica la pista/fila seleccionada (para poner la oveja)
    vis.respondido = pista