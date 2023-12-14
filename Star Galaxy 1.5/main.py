import pygame , class_methods 


#Creamos clase principal Game
class Game(object):
    
    #ATRIBUTOS  ---------------------------------------------------
    def __init__(self, screen):
        #Definimos elementos del juego
        self.all_sprites_list = pygame.sprite.Group()#Lista donde se agregaran todos los sprites
        self.list_laser = pygame.sprite.Group() #Grupo para contener los lasers
        self.list_naves_enemigas = pygame.sprite.Group() #Grupo para contener las naves enemigas

        self.player1 = class_methods.NaveEspacial(screen)
        self.player1.rect.x = 500 #Fijamos posiciones iniciales
        self.player1.rect.y = 600
        self.all_sprites_list.add(self.player1)

        self.super_nave_enemiga = class_methods.NaveSuperEnemigo()
        self.super_nave_enemiga.rect.x = 500 #Fijamos posiciones iniciales
        self.super_nave_enemiga.rect.y = 30
        self.all_sprites_list.add(self.super_nave_enemiga)

        self.misiles = class_methods.TripleMisil(self.all_sprites_list,500, 30)
        self.all_sprites_list.add(self.misiles.misiles) 
        
        #Dicionario para implementar movimiento del jugador
        self.keys_pressed = {'left': False, 'right': False, 'up': False, 'down': False} 

        #Implementamos un timer para retrasar las imagenes de explosion
        self.explosion_start_time = 0    
        self.explosion_duration = 15000  
        
        #Definimos las posiciones de las naves enemigas antes de crearlas , definiendo su posicion y la cantidad de naves
        self.posiciones_enemigos = [(0, 0), (50, 50), (100, 100),(150,150),(200,200),(250,250),(300,200),(350,150),(400,100),(450,50),(500,0)]
        self.nave_enemigas = class_methods.NavesEnemigas() #Creamos instancia para usar recursos

        self.posiciones_enemigos2 = [(1000, 0), (950, 50), (900, 100),(850,150),(800,200),(750,250),(700,300),(650,350),(600,400),(550,450)]
        self.nave_enemigas2 = class_methods.NavesEnemigas() #Creamos instancia para usar recursos

        #Creamos las explosiones finales y las mantenemos en False
        self.explosion = None
        self.explosion2 = None
        
        #Creamos instancias de menu y creamos un temporizador que podra ser util
        self.menu_win = class_methods.MenuWin(screen)
        self.menu_game_over = class_methods.MenuLost(screen)
        self.temporizador_game_over = None 
        
        

    #METODOS ---------------------------------------------------------
    
    #RESETEO DEL JUEGO
    def reset(self,screen):
        # Reiniciamos todas las variables del juego a su estado inicial.
        self.all_sprites_list.empty()
        self.list_laser.empty()
        self.list_naves_enemigas.empty()

        self.player1 = class_methods.NaveEspacial(screen)
        self.player1.rect.x = 500
        self.player1.rect.y = 600
        self.all_sprites_list.add(self.player1)

        self.super_nave_enemiga = class_methods.NaveSuperEnemigo()
        self.super_nave_enemiga.rect.x = 500
        self.super_nave_enemiga.rect.y = 30
        self.all_sprites_list.add(self.super_nave_enemiga)

        self.misiles = class_methods.TripleMisil(self.all_sprites_list, 500, 30)
        self.all_sprites_list.add(self.misiles.misiles)

        self.explosion = False
        self.explosion2 = False
    
        self.keys_pressed = {'left': False, 'right': False, 'up': False, 'down': False}
    
    
    
    #PROCESAMOS EVENTOS
    def proces_events(self):
        for event in pygame.event.get():
            #Eventos externos
            if event.type == pygame.QUIT:
                 return False

            #Movimientos del jugador
            if event.type == pygame.KEYDOWN: #Con el uso de diccionarios y booleanos podemos lograr un mejor desplazamiento del jugador1 incluyendo movimiento diagonal
                if event.key == pygame.K_LEFT:
                    self.keys_pressed['left'] = True
                if event.key == pygame.K_RIGHT:
                    self.keys_pressed['right'] = True
                if event.key == pygame.K_UP:
                    self.keys_pressed['up'] = True
                if event.key == pygame.K_DOWN:
                    self.keys_pressed['down'] = True
                
                #Al presionar la tecla space creamos una instancia de Laser , reproducimos sonido y guardamos coordenadas .    
                if event.key == pygame.K_SPACE:
                    self.laser = class_methods.Laser()
                    self.laser.sound.play()
                    self.laser.rect.x = self.player1.rect.x +30
                    self.laser.rect.y = self.player1.rect.y -25

                    self.all_sprites_list.add(self.laser)  
                    self.list_laser.add(self.laser)   #Agregamos las instancias creadas a la lista para detectar colisiones
           
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.keys_pressed['left'] = False
                if event.key == pygame.K_RIGHT:
                    self.keys_pressed['right'] = False
                if event.key == pygame.K_UP:
                    self.keys_pressed['up'] = False
                if event.key == pygame.K_DOWN:
                    self.keys_pressed['down'] = False
                       
        return True

    
    
    #DEFINIMOS LA PARTE LOGICA DEL JUEGO
    def run_logic(self,screen):
        self.player1.adjust_speed(self.keys_pressed) #Actualizamos la posicion del player1
        self.misiles.update(self.super_nave_enemiga.rect.x+100,self.super_nave_enemiga.rect.y+200) #Actualizamos la posicion de los misiles por iteracion
        self.all_sprites_list.update() #Actualizamos los update() de los sprites
        self.list_laser.update() #Actualizamos la lista de lasers para mayor precision
        
        #Detectamos colisiones y las guardamos en una lista -------------------------------
        colision_laser_supernave = pygame.sprite.spritecollide(self.super_nave_enemiga,self.list_laser,False)
        colision_laser_nave = pygame.sprite.groupcollide(self.list_naves_enemigas, self.list_laser, False, True)
        colision_misil = pygame.sprite.spritecollide(self.player1,self.misiles.misiles,False)
        colision_nave_enemiga = pygame.sprite.spritecollide(self.player1,self.list_naves_enemigas,False)
        
        colisiones_list = colision_laser_supernave,colision_laser_nave,colision_misil,colision_nave_enemiga #Guardamos todas las colisiones en una lista
        
        #Creamos explosion cuando se acaben las vidas de la supernave ,creamos la instancia de explosion y activamos el menu game over
        if self.player1.vidas == 0:
            self.explosion = class_methods.ExplosionFinal(screen)
            self.explosion.sound_lost.play()
            self.menu_game_over.status = True
            self.temporizador_game_over = pygame.time.get_ticks()
            self.player1.kill()

        #Creamos explosion cuando se acaben las vidas de la supernave ,creamos la instancia de explosion y activamos el menu win
        if self.super_nave_enemiga.vidas == 0:
            self.explosion2 = class_methods.ExplosionFinal(screen)
            self.explosion2.sound_win.play()
            self.menu_win.status = True
            self.temporizador_game_over = pygame.time.get_ticks()
            self.super_nave_enemiga.kill()
        
        
        return colisiones_list #Retornamos una lista con las colisiones para luego dibujarlas
    
    
    
    
    #DIBUJAMOS LOS ELEMENTOS EN LA VENTANA Y ACTUALIZAMOS VALORES
    
    #Dibujamos naves enemigas en metodos----------------------
    def naves_enemigas(self):
         for i in self.posiciones_enemigos:
            self.nave_enemiga = class_methods.NavesEnemigas()
            self.nave_enemiga.rect.x =  i[0]
            self.nave_enemiga.rect.y =  i[1]
            self.all_sprites_list.add(self.nave_enemiga) #Agregamos todas las instancias al grupo de sprites
            self.list_naves_enemigas.add(self.nave_enemiga)
    
    def naves_enemigas2(self):
         for i in self.posiciones_enemigos2:
            self.nave_enemiga2 = class_methods.NavesEnemigas2()
            self.nave_enemiga2.rect.x =  i[0]
            self.nave_enemiga2.rect.y =  i[1]
            self.all_sprites_list.add(self.nave_enemiga2) #Agregamos todas las instancias al grupo de sprites
            self.list_naves_enemigas.add(self.nave_enemiga2)    
    
   
    def display_frame(self, screen, lista_colisiones):
            #Dibujamos Sprites--------------------------------
            self.all_sprites_list.draw(screen)

            
            #Dibujamos las explosiones al colisionar-------------------
            colision_laser, colision_laser_nave, colision_misil, colision_nave_enemiga = lista_colisiones #Desempaquetamos la lista en variables locales

            #Colisiones del laser con naves enemigas 
            for laser in colision_laser:
                screen.blit(self.laser.explosion_laser, [self.super_nave_enemiga.rect.x + 80, self.super_nave_enemiga.rect.y + 130])
                self.super_nave_enemiga.vidas -= 1
                self.player1.score += 200
                laser.kill() #Eliminamos instancia
                
            for nave in colision_laser_nave:
                screen.blit(self.nave_enemigas.explosion, [nave.rect.x + 15, nave.rect.y + 20])
                nave.vidas -=1
                self.player1.score += 50
                if nave.vidas <= 0 : #Eliminamos la instancia solo si pierde las 5 vidas
                    nave.kill() #Eliminamos instancia
                
                
            
            #Colision misiles de la supernave con player1 
            tiempo_transcurrido = pygame.time.get_ticks() - self.explosion_start_time
            for misil in colision_misil:
                if tiempo_transcurrido < self.explosion_duration:
                    screen.blit(self.misiles.explosion_misil, [self.player1.rect.x + 30, self.player1.rect.y + 20])
                    screen.blit(self.misiles.explosion_misil, [self.player1.rect.x, self.player1.rect.y + 10])
                    self.player1.vidas -= 3
                    self.player1.score -= 100
                else:
                    self.explosion_start_time = pygame.time.get_ticks()

                    for misil in self.misiles.misiles:
                        misil.kill() #Eliminamos instancia
            
            
            #Colision naves enemigas con player1
            for nave_enemiga in colision_nave_enemiga:
                screen.blit(self.nave_enemigas.explosion, [self.player1.rect.x + 15, self.player1.rect.y + 20])
                self.nave_enemigas.sound.play()
                self.player1.vidas -= 1
                self.player1.score -= 50
                nave_enemiga.kill() #Eliminamos instancia

            if self.player1.vidas <= 0: #Mantenemos las vidas en 0 en caso de ser negativo
                self.player1.vidas = 0
        
            if self.player1.score < 0: #Mantenemos el score en 0 en caso de ser negativo
                self.player1.score = 0   
            
            
            #Verificamos el estado de las explosiones finales antes de dibujarlas------------------------
            if self.explosion:
                self.explosion.explosionFinal(self.player1.rect.x,self.player1.rect.y)    
            
            if self.explosion2:
                self.explosion2.explosionFinal(self.super_nave_enemiga.rect.x,self.super_nave_enemiga .rect.y)      





#Funcion principal del juego  -------------------------------------------------------------------------------------
def main():
    pygame.init()
    
    #Incluimos la sentencias necesarias para poder mostrar textos en la ventana (score , vidas)
    fuente = pygame.font.Font(None, 36)  #Ajustar el tamaño de la fuente 
    color_texto = (class_methods.WHITE)  # Color del texto 

    screen = pygame.display.set_mode([class_methods.WIDTH_SCREEN,class_methods.HEIGHT_SCREEN])#Definimos dimensiones
    
    pygame.display.set_caption("Star Galaxy") #Nombre de la ventana
    
    #Backgraound principal
    background_principal = pygame.image.load("PyGame/Star Galaxy 1.5 (POO)/img/zackground_principal.jpg").convert()
    background_principal = pygame.transform.scale(background_principal, (1100, 700))#Redimensionar imagen
    
    stars = class_methods.crearPuntos() #Usamos este metodo para crear estrellas
    
    clock = pygame.time.Clock()

    game = Game(screen) #Instancia de Game
    
    
    #Creamos las instancias de las naves enemigas antes del bucle principal
    game.naves_enemigas()
    game.naves_enemigas2()
    
    
    #Instanciamos el menu start aqui porque solo aparecera una sola vez durante la ejecucion
    menu_principal = class_methods.MenuPrincipal(screen)
    start = True
    
    #Bucle principal
    done =True
    while done:
        #Comprobamos estados de menu con condicionales, para avanzar de pantalla segun corresponda
        if start:
            start = menu_principal.menu_principal()
            if menu_principal.quit:
                break
        
       
        elif game.menu_game_over.status:
                tiempo_transcurrido = pygame.time.get_ticks() - game.temporizador_game_over #Retrasamos la aparicion de la pantalla final 3 segundos
                if tiempo_transcurrido > 3000:
                    game.menu_game_over.menu_lost()
                    game.temporizador_game_over = pygame.time.get_ticks()
                    if game.menu_game_over.reset: 
                        game.reset(screen)
                        game.naves_enemigas()
                        game.naves_enemigas2()
                    if game.menu_game_over.quit:
                        break
        
        
        elif game.menu_win.status:
                tiempo_transcurrido = pygame.time.get_ticks() - game.temporizador_game_over #Retrasamos la aparicion de la pantalla final 3 segundos
                if tiempo_transcurrido > 3000:
                    game.menu_win.menu_win()
                    game.temporizador_game_over = pygame.time.get_ticks()
                    if game.menu_win.reset:
                        game.reset(screen)
                        game.naves_enemigas()
                        game.naves_enemigas2()
                    if game.menu_win.quit:
                        break
        
        
        else :
            #Comprobamos eventos
            done = game.proces_events() 

            #Agregamos primero el background para que luego no se superponga
            screen.blit(background_principal,[0,0]) 
            
            #Agregamos el Score y las vidas en la pantalla
            texto_puntaje = fuente.render(f"SCORE: {game.player1.score}", True, color_texto)
            screen.blit(texto_puntaje, (50, 10))  # Ajusta las coordenadas según la posición deseada
            
            texto_vidas = fuente.render(f"VIDAS: {game.player1.vidas}",True,color_texto)
            screen.blit(texto_vidas, (850, 10))  # Ajusta las coordenadas según la posición deseada
            
            #Aplicamos la animacion de estrellas en movimiento
            class_methods.moverPuntos(stars,screen)
            
            #Ejecutamos la logica , y guardamos colisiones en una lista para poder dibujarlas luego
            lista_colisiones = game.run_logic(screen)

            #Hacemos los dibujos en la pantalla y pasamos como argumento las colisiones
            game.display_frame(screen,lista_colisiones) 
            
            #Actuaizamos la pantalla
            pygame.display.flip()  
            
            #Determinamos los FPS del juego
            clock.tick(60) 

    pygame.quit()
    
   
   

if __name__ == "__main__":
    main()    
    