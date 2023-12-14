import pygame , random ,time


#Definimos Valores constantes ----------------------------------------

#Definir tamaño de pantalla
WIDTH_SCREEN = 1100
HEIGHT_SCREEN = 700

#Definir colores 
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)



#Creacion de clases y metodos  ---------------------------------------

#Nave espacial con propulsores y variables para movimiento. Es necesario en el parametro screen , el nombre de ventana en el main
class NaveEspacial(pygame.sprite.Sprite) :
    def __init__(self,screen):
        super().__init__()
        self.image = pygame.image.load("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/img/znave_1_player.png").convert()
        self.image = pygame.transform.scale(self.image,(70,90)) #Redimensionamos la imagen
        self.image.set_colorkey(BLACK) #Quitamos el contorno negro
        self.rect = self.image.get_rect() #Obtenemos posicion
        self.vidas = 5
        self.screen = screen
        self.score = 0
        #Determinamos el movimiento
        self.speed_x = 0 
        self.speed_y = 0
        
        
        #Propulsores , cargamos 3 imagenes para generar efecto de movimiento
        self.images = ["/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/img/propulsores.png","/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/img/propulsores2.png","/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/img/propulsores3.png"]
        self.images = [pygame.image.load(nombre_archivo) for nombre_archivo in self.images]
        self.index_image = 0
        #Redimensionamos y quitamos contorno negro individualmente 
        self.images[0] = pygame.transform.scale(self.images[0], (30, 40))
        self.images[0].set_colorkey(BLACK)

        self.images[1] = pygame.transform.scale(self.images[1], (30, 40))
        self.images[1].set_colorkey(BLACK)

        self.images[2] = pygame.transform.scale(self.images[2], (30, 40))
        self.images[2].set_colorkey(BLACK)
    
    
    #Cambiamos el movimiento segun las teclas presionadas ,usando diccionarios obtenemos mas precision
    def adjust_speed(self, keys_pressed):   #Al trabajar con booleanos en Python, la resta de dos booleanos se traduce a 1 si el primer booleano es True y el segundo es False, y a -1 en caso contrario.(chat gpt)
        self.speed_x = (keys_pressed['right'] - keys_pressed['left']) * 5
        self.speed_y = (keys_pressed['down'] - keys_pressed['up']) * 5

    def update(self):
        # Logica necesaria para implementar la secuencia de imagenes como efecto de propulsores
        self.index_image = (self.index_image + 1) % len(self.images)
        if self.vidas > 0:
            self.screen.blit(self.images[self.index_image], (self.rect.x + 20, self.rect.y + 80))
        #Generamos el movimiento
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        #Mantenemos la nave dentro de la ventana , usando los margenes con top,bottom,left y right
        if self.rect.left < 0:
            self.rect.left = 0
        
        elif self.rect.right > WIDTH_SCREEN:
            self.rect.right = WIDTH_SCREEN

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT_SCREEN:
            self.rect.bottom = HEIGHT_SCREEN




#Laser para nave espacial 
class Laser (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/img/zlasernave.png").convert()
        self.image = pygame.transform.scale(self.image,(10,20))#Redimensionar imagen
        self.image.set_colorkey(BLACK) #Quita el contorno negro
        self.rect = self.image.get_rect() #Obtenemos posicion
        self.sound = pygame.mixer.Sound("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/sounds/zlaser.wav") #Efecto de sonido laser
        self.initial_x = 0
        self.initial_y = 0
        #Agregamos imagen para explosion
        self.explosion_laser =  pygame.image.load("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/img/zexplosionlaser.png").convert()
        self.explosion_laser = pygame.transform.scale(self.explosion_laser,(50,50))#Redimensionar imagen
        self.explosion_laser.set_colorkey(BLACK)
    
        
    def update(self):
        self.rect.y -= 4    #Velocidad de desplazamiento del laser
        if self.rect.y < 0:
            self.kill()
        self.initial_x = self.rect.x
        self.initial_y = self.rect.y



#Super nave con desplazamiento horizontal
class NaveSuperEnemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image =  pygame.image.load("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/img/zsuperenemigo.png").convert()
        self.image = pygame.transform.scale(self.image,(200,200))#Redimensionar imagen
        self.image.set_colorkey(BLACK) #Quita el contorno negro
        self.speed = 3
        self.vidas = 15
        self.rect = self.image.get_rect()#Obtenemos posicion
        self.rect.inflate_ip(40, 0) #Agrandamos el rectangulo para que se ajuste a su tamaño real

    def update (self):
        self.rect.x += self.speed
        #Definimos limites para desplazamiento horizontal
        if self.rect.x > 800 or self.rect.x < 100:
            self.speed *= -1        



#Misil para Super nave enemiga
class MisilSuperEnemigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/img/zlaserenemigo.png").convert()
        self.image = pygame.transform.scale(self.image, (30, 50)) #Redimensionamos imagen
        self.image.set_colorkey(BLACK) #Quitamos contorno negro
        self.rect = self.image.get_rect() #Obtenemos posicion
        self.sound = pygame.mixer.Sound("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/sounds/zmisil.wav") #Efecto de sonido al disparar
        self.tiempo_ultimo_disp = time.time() #Iniciamos timer para disparar cada 3 seg
        self.vida = 15
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 5 #Velocidad de desplazamiento





#Creamos efecto triple misil partiendo de 3 instancias de MisilSuperEnemigo
class TripleMisil(pygame.sprite.Sprite):
    def __init__(self, all_sprites_list, x, y): #Le pasamos como parametros la posicion de la nave enemiga
        super().__init__()
        self.sound = pygame.mixer.Sound("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/sounds/zmisil.wav") #Efecto sonido al disparar
        self.tiempo_ultimo_disp = time.time() #Iniciamos Timer para disparar cada 3 segundos
        self.all_sprites_list = all_sprites_list  #Agrega la referencia al grupo de sprites
        self.misiles = pygame.sprite.Group()  #Grupo para contener los misiles
        self.rect = pygame.Rect(x, y, 1,1)  #Crea un rectángulo ficticio para la posición inicial
        #Agregamos imagen para explosion
        self.explosion_misil =  pygame.image.load("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/img/zexplosionlaser.png").convert()
        self.explosion_misil = pygame.transform.scale(self.explosion_misil,(50,50))#Redimensionar imagen
        self.explosion_misil.set_colorkey(BLACK)
        
    
    def update(self,x,y):
        #Recibimos como parametros las coordenadas de la Super nave enemiga
        self.rect.x = x
        self.rect.y = y
        
        # Verificar si ha pasado el tiempo suficiente para disparar
        if time.time() - self.tiempo_ultimo_disp > 3:
            self.sound.play()
            self.tiempo_ultimo_disp = time.time()

            # Crear tres instancias de MisilSuperEnemigo y agregarlas al grupo de misiles y al grupo de sprites
            for offset in [-40, 0, 40]:
                misil = MisilSuperEnemigo(self.rect.x + offset, self.rect.y - 40)
                self.misiles.add(misil)
                self.all_sprites_list.add(misil)

        # Actualizar todos los misiles en el grupo
        self.misiles.update()
        if self.rect.y > HEIGHT_SCREEN:
            self.kill()



#Metodo para crear puntos blancos por toda la pantalla
def crearPuntos():
    coor_list = []
    for i in range(90):  #60 representa la cantidad de "estrellas" que se mostraran en la ventana
        x = random.randint(0,1100)
        y = random.randint(0,700)
        coor_list.append([x,y])
    return coor_list    


#Estrellas en movimiento, damos valores al eje Y para generar el movimiento
def moverPuntos(coor_list,screen):
        for coord in coor_list:
            x = coord[0]
            y =  coord[1]
            estrellas = pygame.draw.circle(screen,WHITE,(x,y),2)#Creamos los elemntos segun cantidad de cordenadas almacenadas en "coor_list"
            coord[1] += 4 #Velocidad de movimiento
            
            if coord[1] > 700 : #Condicional para que el efecto sea infinito
                coord[1] = 0
                
                
                
                
#Conjunto de naves enemigas 1
class NavesEnemigas(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image =  pygame.image.load("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/img/zenemigo.png").convert()
            self.image = pygame.transform.scale(self.image,(50,50))
            self.image.set_colorkey(BLACK) 
            self.rect = self.image.get_rect() #Obtenemos posicion
            self.vidas = 5
            #Agregamos imagen para explosion
            self.explosion =  pygame.image.load("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/img/zexplosionlaser.png").convert()
            self.explosion = pygame.transform.scale(self.explosion,(50,50))#Redimensionar imagen
            self.explosion.set_colorkey(BLACK)
            
            #Sonido para impacto con player           
            self.sound = pygame.mixer.Sound("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/sounds/zimpacto.wav") #Efecto de sonido laser

            
            #Velocidad a la que se movera el objeto "Nave enemigo"
            self.speed_x = 4
            self.speed_y = 4
        
        
        def update(self):
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            #Mantenemos la formacion al llegar a los limites de la ventana
            if self.rect.x > WIDTH_SCREEN or self.rect.x < 0:
                self.speed_x *= -1
        
            if self.rect.y > HEIGHT_SCREEN or self.rect.y < 0:
                self.speed_y *= -1



#Conjunto de naves enemigas 2
class NavesEnemigas2(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image =  pygame.image.load("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/img/zenemigo2.png").convert()
            self.image = pygame.transform.scale(self.image,(50,50))
            self.image.set_colorkey(BLACK) 
            self.rect = self.image.get_rect() #Obtenemos posicion
            self.vidas = 0
            #Agregamos imagen para explosion
            self.explosion =  pygame.image.load("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/img/zexplosionlaser.png").convert()
            self.explosion = pygame.transform.scale(self.explosion,(50,50))#Redimensionar imagen
            self.explosion.set_colorkey(BLACK)
            #Sonido para contacto con player           
            self.sound = pygame.mixer.Sound("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/sounds/zimpacto.wav") #Efecto de sonido laser

            
            #Velocidad a la que se movera el objeto "Nave enemigo"
            self.speed_x = 4
            self.speed_y = 4
        
        
        def update(self):
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            #Mantenemos la formacion al llegar a los limites de la ventana
            if self.rect.x > WIDTH_SCREEN or self.rect.x < 0 :
                self.rect.y = 0
                self.rect.x = random.randint(0, 950) #Usamos coordenadas random para aumentar la dificultad
                self.speed_x *= -1
            if self.rect.y > HEIGHT_SCREEN :
                self.rect.y = 0      
                
                        

#Explosion triple final para naves
class ExplosionFinal():
    def __init__(self,screen):
        self.image = pygame.image.load("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/img/zsuperexplosion.png").convert()
        self.image = pygame.transform.scale(self.image,(100,100))#Redimensionar imagen
        self.image.set_colorkey(BLACK)
        # Sonido explosion + sonido segun corresponda (win , lost)
        self.sound_win = pygame.mixer.Sound("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/sounds/zwin.wav") #Efecto de sonido laser
        self.sound_lost = pygame.mixer.Sound("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/sounds/zlost.wav") #Efecto de sonido laser
        
        self.screen = screen
        self.rect = self.image.get_rect() #Obtenemos posicion
    
    def explosionFinal(self,x,y): #Dibujamos las explosiones en las coordenadas pasadas como parametro
        self.screen.blit(self.image, [x-50, y+50])
        self.screen.blit(self.image, [x , y])
        self.screen.blit(self.image, [x + 50, y + 50])



#Menu start , win y game over

class MenuPrincipal():
    def __init__(self,screen):
        self.background = pygame.image.load("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/img/zstart.jpg").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH_SCREEN, HEIGHT_SCREEN))
        self.screen = screen
        #Sentencias para modificar el estado del objeto
        self.quit = False
        self.true = True
        
    def menu_principal(self):
            self.screen.blit(self.background, [0, 0])
            pygame.display.update()
            #Detectamos eventos mientras estamos en el menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #Necesario para poder cerrar la ventana
                    self.quit = True
                    return self.quit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.status = False
                        return self.status #Actualizamos valor para determinar el estado del objeto

            return self.true #Mamntenemos el menu en True hasta que se presione una tecla
        
        
        
class MenuLost():
    def __init__(self,screen):
        self.background = pygame.image.load("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/img/zgameover.jpg").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH_SCREEN, HEIGHT_SCREEN))
        self.screen = screen
        #Sentencias para modificar el estado del menu
        self.quit = False
        self.reset = False
        self.status = False

        
    def menu_lost(self):
                self.screen.blit(self.background, [0, 0])
                pygame.display.update()
                #Detectamos eventos mientras estamos en el menu
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: #Necesario para poder cerrar la ventana
                        self.quit = True
                        return self.quit
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                            self.status = False
                            self.reset = True
                            return self.reset   #Actualizamos estos valores para poder reiniciar
                        elif event.key == pygame.K_n:
                            self.quit = True
                        return self.quit


                            
class MenuWin():
    def __init__(self,screen):
        self.background = pygame.image.load("/home/marianolaclau/Documentos/Programacion/Programacion/PyGame/Star Galaxy 1.5 (POO)/img/zwin.jpg").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH_SCREEN, HEIGHT_SCREEN))
        self.screen = screen
        #Sentencias para modificar el estado del menu
        self.status = False
        self.quit = False
        self.reset = False
        
    def menu_win(self):
                self.screen.blit(self.background, [0, 0])
                pygame.display.update()
                #Detectamos eventos mientras estamos en el menu
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: #Necesario para poder cerrar la ventana
                        self.quit = True
                        return self.quit
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                            self.status = False 
                            self.reset = True 
                            return self.reset #Actualizamos estos valores para poder reiniciar
                        elif event.key == pygame.K_n:
                            self.quit = True
                        return self.quit                        