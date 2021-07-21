#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 17:26:25 2021

@author: Catalina
"""

import arcade

#dimenciones pantalla
height=702
width=611
scaling= 1.0

ventana=None
#introducir variables
puntaje=6
contador=0
contador2=0
contador3=0



class MapaDemo(arcade.Window):
    def __init__(self):
        #ventana base
        #titulo en pantalla
        super().__init__(width, height, "CLASH OF ALIENS", False, True)
        
        self.estrellas=None
        self.planetas=None
        self.aliens=None
        self.disparos=None
        self.limite=None
        self.naves=None
        #introducir mucica de fondo
        self.musica = arcade.Sound ("/Users/Catalina/Desktop/proyecto.video/sonidos/sonidofondo.mp3.mp3", True)
        self.musica.play (volume = 0.5)
        
       
        
        
class GamePlay (arcade.View):
    def __init__(self):
        super().__init__()
        #introducir imagen inicio
        self.texture = arcade.load_texture("/Users/Catalina/Desktop/proyecto.video/menu.jpeg")
        
        arcade.set_viewport(0, width - 1, 0, height - 1)
    def on_draw(self):
        
        arcade.start_render() 
        
        self.texture.draw_sized(width / 2, height / 2, width, height)
        
    def on_key_release(self, key, _modifiers):
        #intoducir funcion de tecla 
        if key == arcade.key.MOTION_UP:
            mostrar_juego()       






class Juego(arcade.View): 
    
    def __init__(self):
        super ().__init__()
        #color de fondo N1
        arcade.set_background_color(arcade.color.BLUEBERRY)
        
    def setup(self):
        arcade.start_render()
        self.naves= arcade.SpriteList()
        #dibujar
        self.nave= arcade.Sprite("/Users/Catalina/Desktop/proyecto.video/1.png", scaling)
        self.nave.center_y= 50
        self.nave.center_x= 100
        self.naves.append(self.nave)    
       
        #leer el mapa
        self.map=arcade.tilemap.read_tmx("/Users/Catalina/Desktop/proyecto.video/MapaInfinito.tmx")
        #carga de layers
        self.limite=arcade.SpriteList(use_spatial_hash=True)
        self.limite.extend( arcade.tilemap.process_layer(self.map, "limite"))
        #movimientos gravitatorios
        self.estrellas = arcade.tilemap.process_layer(self.map, "estrellas")
        for estrella in self.estrellas:
            estrella.change_y=-1
        self.planetas = arcade.tilemap.process_layer(self.map, "planetas")
        for planeta in self.planetas:
            planeta.change_y=-1
        self.aliens = arcade.tilemap.process_layer(self.map, "aliens")
        for alien in self.aliens:
            alien.change_y=-2

            
        self.disparos=arcade.SpriteList()
        
        #generar motor
        self.motor_fisica=arcade.PhysicsEnginePlatformer(self.nave, self.limite)
        
        # sonidos
        
        
        self.sonido_disparo = arcade.Sound ("/Users/Catalina/Desktop/proyecto.video/sonidos/laser.wav.wav", False)
        self.sonido_disparo.play(volume = 0.4)
   
    def on_draw(self):
        #dibujo
        arcade.start_render()                 
        self.estrellas.draw()
        self.planetas.draw()
        self.aliens.draw()
        self.disparos.draw()
        self.limite.draw()
        self.naves.draw() 
        
        #puntaje
        arcade.draw_text(f"Puntaje:{puntaje}", 50, height-100, arcade.color.BLUE, 30)
       
    
    def on_update(self, delta_time):
        
        global puntaje
        global contador
        #actualiza motor de fisica
        self.motor_fisica.update()
        
        self.estrellas.update()
        self.planetas.update()
        self.naves.update_animation()
        self.aliens.update()
        #condiciones/bucles para choques entre objetos, puntos y desapariciones    
        for disparo in self.disparos:
            choque = arcade.check_for_collision_with_list(disparo, self.aliens)
            if len(choque)!=0:
                for choque in choque: 
                    contador += 1
                    puntaje += 10
                    self.aliens.remove(choque)
                self.disparos.remove(disparo)
        self.disparos.update()             
        
        for aliens in self.aliens:
            colision= arcade.check_for_collision_with_list(aliens, self.limite)
            if len(colision)!=0:
                contador +=1
                puntaje -=2
                self.aliens.remove(aliens)
                
        #condiciones para que aparezca el menu correspondiente cuando termine el juego
        if contador==27:
            mostrar_puntaje_1()
            contador-=27
    def on_key_press(self, key, modifiers):
        #movimiento nave y disparos
        if key == arcade.key.LEFT:
            self.nave.change_x = -10
        elif key == arcade.key.RIGHT:
            self.nave.change_x=10
        elif key == arcade.key.SPACE:
            disparo=arcade.SpriteSolidColor(5, 3, arcade.color.BLACK)
            disparo.center_x=self.nave.center_x
            disparo.center_y=self.nave.center_y
            if self.nave.change_x<0:
                disparo.change_y=-5
            else:
                disparo.change_y=5

            self.disparos.append(disparo)
            self.sonido_disparo.play()
            
       

    
    def on_key_release(self, key, modifiers):
        #condiciones para cambio de nivel al terminar el juego, mostrando menu correspondiente
        if contador==27 :
            mostrar_puntaje_1()
        
        
        if key == arcade.key.LEFT or key==arcade.key.RIGHT:
            self.nave.change_x = 0
        elif key == arcade.key.RIGHT:
            self.nave.change_x = 0
        
class Juego2(arcade.View): 
    
    def __init__(self):
        super ().__init__()
        arcade.set_background_color(arcade.color.APPLE_GREEN)
        
    def setup(self):
        arcade.start_render()
        self.naves= arcade.SpriteList()
        #dibujar
        self.nave= arcade.Sprite("/Users/Catalina/Desktop/proyecto.video/1.png", scaling)
        self.nave.center_y= 100
        self.nave.center_x= 100
        self.naves.append(self.nave)    
       
        #leer el mapa
        self.map=arcade.tilemap.read_tmx("/Users/Catalina/Desktop/proyecto.video/MapaInfinito.tmx")
        #carga de layers
        self.limite=arcade.SpriteList(use_spatial_hash=True)
        self.limite.extend( arcade.tilemap.process_layer(self.map, "limite"))
        
        self.estrellas = arcade.tilemap.process_layer(self.map, "estrellas")
        for estrella in self.estrellas:
            estrella.change_y=-1
        self.planetas = arcade.tilemap.process_layer(self.map, "planetas")
        for planeta in self.planetas:
            planeta.change_y=-1
        self.aliens = arcade.tilemap.process_layer(self.map, "aliens")
        for alien in self.aliens:
            alien.change_y=-2
        self.aliens2 = arcade.tilemap.process_layer(self.map, "alien2")
        for alien2 in self.aliens2:
            alien2.change_y=-3
          
        self.bomba1 = arcade.tilemap.process_layer(self.map, "bomba1")
        for bomba1 in self.bomba1:
            bomba1.change_y=-2   
         
        self.disparos=arcade.SpriteList()
        
        #generar motor
        self.motor_fisica=arcade.PhysicsEnginePlatformer(self.nave, self.limite)
        
        # sonidos
        
        self.sonido_disparo = arcade.Sound ("/Users/Catalina/Desktop/proyecto.video/sonidos/laser.wav.wav", False)
        self.sonido_disparo.play(volume = 0.4)
   
    def on_draw(self):
        #dibujo
        arcade.start_render()                 
        self.estrellas.draw()
        self.planetas.draw()
        self.aliens.draw()
        self.disparos.draw()
        self.limite.draw()
        self.naves.draw() 
        self.aliens2.draw()
        self.bomba1.draw()
        
        
        #puntaje
        arcade.draw_text(f"Puntaje:{puntaje}", 50, height-100, arcade.color.GREEN_YELLOW, 30)
       
    
    def on_update(self, delta_time):
        global puntaje
        global contador2
        
        #actualiza motor de fisica
        self.motor_fisica.update()
 
        self.estrellas.update()
        self.planetas.update()
        self.naves.update_animation()
        self.aliens.update()
        self.aliens2.update()
        self.bomba1.update()
           
        for disparo in self.disparos:
            choque = arcade.check_for_collision_with_list(disparo, self.aliens)
            if len(choque)!=0:
                for choque in choque: 
                    contador2 += 1
                    puntaje += 10
                    self.aliens.remove(choque)
                self.disparos.remove(disparo)
        self.disparos.update()             
        
        for disparo in self.disparos:
            choque = arcade.check_for_collision_with_list(disparo, self.aliens2)
            if len(choque)!=0:
                for choque in choque: 
                    contador2 += 1
                    puntaje += 15
                    self.aliens2.remove(choque)
                self.disparos.remove(disparo)
        self.disparos.update()
        
        for disparo in self.disparos:
            choque = arcade.check_for_collision_with_list(disparo, self.bomba1)
            if len(choque)!=0:
                for choque in choque: 
                    contador2 += 1
                    puntaje += 30
                    self.bomba1.remove(choque)
                self.disparos.remove(disparo)
        self.disparos.update()
        
        
        for aliens in self.aliens:
            colision= arcade.check_for_collision_with_list(aliens, self.limite)
            if len(colision)!=0:
                contador2 +=1
                puntaje -=2
                self.aliens.remove(aliens)
        
            
        for aliens2 in self.aliens2:
            colision= arcade.check_for_collision_with_list(aliens2, self.limite)
            if len(colision)!=0:
                contador2 +=1
                puntaje -=5
                self.aliens2.remove(aliens2)
        
        for bomba in self.bomba1:
            colision= arcade.check_for_collision_with_list(bomba, self.limite)
            if len(colision)!=0:
                contador2 +=1
                puntaje -=60
                self.bomba1.remove(bomba)
        
        ##pendiente
        if contador2==41:
            mostrar_puntaje_2()      
            contador2-=41
        
    def on_key_press(self, key, modifiers):
        
        if key == arcade.key.LEFT:
            self.nave.change_x = -10
        elif key == arcade.key.RIGHT:
            self.nave.change_x=10
        elif key == arcade.key.SPACE:
            disparo=arcade.SpriteSolidColor(5, 3, arcade.color.BLACK)
            disparo.center_x=self.nave.center_x
            disparo.center_y=self.nave.center_y
            if self.nave.change_x<0:
                disparo.change_y=-5
            else:
                disparo.change_y=5

            self.disparos.append(disparo)
            self.sonido_disparo.play()
            
       

    
    def on_key_release(self, key, modifiers):
        ##pendiente
        if contador2==41:
            mostrar_puntaje_2()
            
                 
        
        if key == arcade.key.LEFT or key==arcade.key.RIGHT:
            self.nave.change_x = 0
        elif key == arcade.key.RIGHT:
            self.nave.change_x = 0
        
            



class Juego3(arcade.View): 
    
    def __init__(self):
        super ().__init__()
        arcade.set_background_color(arcade.color.PURPLE_MOUNTAIN_MAJESTY)
        
    def setup(self):
        arcade.start_render()
        self.naves= arcade.SpriteList()
        #dibujar
        self.nave= arcade.Sprite("/Users/Catalina/Desktop/proyecto.video/1.png", scaling)
        self.nave.center_y= 100
        self.nave.center_x= 100
        self.naves.append(self.nave)    
       
        #leer el mapa
        self.map=arcade.tilemap.read_tmx("/Users/Catalina/Desktop/proyecto.video/MapaInfinito.tmx")
        #carga de layers
        self.limite=arcade.SpriteList(use_spatial_hash=True)
        self.limite.extend( arcade.tilemap.process_layer(self.map, "limite"))
        
        self.estrellas = arcade.tilemap.process_layer(self.map, "estrellas")
        for estrella in self.estrellas:
            estrella.change_y=-1
        self.planetas = arcade.tilemap.process_layer(self.map, "planetas")
        for planeta in self.planetas:
            planeta.change_y=-1
        self.aliens = arcade.tilemap.process_layer(self.map, "aliens")
        for alien in self.aliens:
            alien.change_y=-3
        self.aliens3 = arcade.tilemap.process_layer(self.map, "alien3")
        for alien3 in self.aliens3:
            alien3.change_y=-3
          
        self.bomba2 = arcade.tilemap.process_layer(self.map, "bomba2")
        for bomba2 in self.bomba2:
            bomba2.change_y=-4   
         
        self.disparos=arcade.SpriteList()
        
        #generar motor
        self.motor_fisica=arcade.PhysicsEnginePlatformer(self.nave, self.limite)
        
        # sonidos
        
        self.sonido_disparo = arcade.Sound ("/Users/Catalina/Desktop/proyecto.video/sonidos/laser.wav.wav", False)
        self.sonido_disparo.play(volume = 0.4)
   
    def on_draw(self):
        #dibujo
        arcade.start_render()                 
        self.estrellas.draw()
        self.planetas.draw()
        self.aliens.draw()
        self.disparos.draw()
        self.limite.draw()
        self.naves.draw() 
        self.aliens3.draw()
        self.bomba2.draw()
        
        
        #puntaje
        arcade.draw_text(f"Puntaje:{puntaje}", 50, height-100, arcade.color.PURPLE_HEART, 30)
       
    
    def on_update(self, delta_time):
        global puntaje
        global contador3
        
        #actualiza motor de fisica
        self.motor_fisica.update()
 
        self.estrellas.update()
        self.planetas.update()
        self.naves.update_animation()
        self.aliens.update()
        self.aliens3.update()
        self.bomba2.update()
           
        for disparo in self.disparos:
            choque = arcade.check_for_collision_with_list(disparo, self.aliens)
            if len(choque)!=0:
                for choque in choque: 
                    contador3 += 1
                    puntaje += 10
                    self.aliens.remove(choque)
                self.disparos.remove(disparo)
        self.disparos.update()             
        
        for disparo in self.disparos:
            choque = arcade.check_for_collision_with_list(disparo, self.aliens3)
            if len(choque)!=0:
                for choque in choque: 
                    contador3 += 1
                    puntaje += 20
                    self.aliens3.remove(choque)
                self.disparos.remove(disparo)
        self.disparos.update()
        
        for disparo in self.disparos:
            choque = arcade.check_for_collision_with_list(disparo, self.bomba2)
            if len(choque)!=0:
                for choque in choque: 
                    contador3 += 1
                    puntaje += 35
                    self.bomba2.remove(choque)
                self.disparos.remove(disparo)
        self.disparos.update()
        
        
        for aliens in self.aliens:
            colision= arcade.check_for_collision_with_list(aliens, self.limite)
            if len(colision)!=0:
                contador3 +=1
                puntaje -=2
                self.aliens.remove(aliens)
        
            
        for aliens3 in self.aliens3:
            colision= arcade.check_for_collision_with_list(aliens3, self.limite)
            if len(colision)!=0:
                contador3 +=1
                puntaje -=10
                self.aliens3.remove(aliens3)
        
        for bomba2 in self.bomba2:
            colision= arcade.check_for_collision_with_list(bomba2, self.limite)
            if len(colision)!=0:
                contador3 +=1
                puntaje -=70
                self.bomba2.remove(bomba2)
        
        ##pendiente
        if contador3==41:
            mostrar_puntaje_3()
            contador3-=41
                    
        
        
    def on_key_press(self, key, modifiers):
        
        if key == arcade.key.LEFT:
            self.nave.change_x = -10
        elif key == arcade.key.RIGHT:
            self.nave.change_x=10
        elif key == arcade.key.SPACE:
            disparo=arcade.SpriteSolidColor(5, 3, arcade.color.BLACK)
            disparo.center_x=self.nave.center_x
            disparo.center_y=self.nave.center_y
            if self.nave.change_x<0:
                disparo.change_y=-5
            else:
                disparo.change_y=6

            self.disparos.append(disparo)
            self.sonido_disparo.play()
            
       

    
    def on_key_release(self, key, modifiers):
        
        ##pendiente
        if contador3==41:
            mostrar_puntaje_3()
            
        if key == arcade.key.LEFT or key==arcade.key.RIGHT:
            self.nave.change_x = 0
        elif key == arcade.key.RIGHT:
            self.nave.change_x = 0
        
            


class GameOver (arcade.View):
    
    def __init__(self):
        #ventana base
        super().__init__()
        self.texture = arcade.load_texture("/Users/Catalina/Desktop/proyecto.video/game_over.jpeg")
        
    def on_draw(self):
        arcade.start_render()
     
        arcade.set_viewport(0, width, 0, height)
        self.texture.draw_sized(width / 2, height / 2, width, height)
    def on_update(self, delta_time):
        global puntaje
        puntaje=puntaje-puntaje+6
            
    def on_key_release(self,  key, _modifiers) :
        if key == arcade.key.MOTION_DOWN:
            mostrar_inicio()
        
class GameOver2 (arcade.View):
    
    def __init__(self):
        #ventana base
        super().__init__()
        self.texture = arcade.load_texture("/Users/Catalina/Desktop/proyecto.video/menu2.jpeg")
        
    def on_draw(self):
        arcade.start_render()
        
   
        arcade.set_viewport(0, width, 0, height)
        self.texture.draw_sized(width / 2, height / 2, width, height)
   
    def on_key_release(self,  key, _modifiers) :
        if key == arcade.key.KEY_1:
            mostrar_juego()            
        elif key==arcade.key.KEY_2:
            mostrar_juego2()

            
class GameOver3 (arcade.View):
    
    def __init__(self):
        #ventana base
        super().__init__()
        self.texture = arcade.load_texture("/Users/Catalina/Desktop/proyecto.video/menu3.jpeg")
        
    def on_draw(self):
        arcade.start_render()
        
        arcade.set_viewport(0, width, 0, height)
        self.texture.draw_sized(width / 2, height / 2, width, height)
        
    
   
    def on_key_release(self,  key, _modifiers) :
        
        if key == arcade.key.KEY_1:
            mostrar_juego()            
        elif key==arcade.key.KEY_2:
            mostrar_juego2()
        elif key==arcade.key.KEY_3:
            mostrar_juego3()
            
class puntaje1 (arcade.View):
    
    def __init__(self):
        #ventana base
        super().__init__()

        
    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_text(f"Tu puntaje final fue de : {puntaje}", 70, height//2-100, arcade.color.BLACK,25) 
        arcade.draw_text("presione tecla '4' para continuar", 70, height//2-200, arcade.color.BLACK,15)
        arcade.draw_text("presione tecla 'ENTER' para finalizar", 70, height//2-300, arcade.color.BLACK,15)
    def on_key_release(self, key, modifiers):
        #condiciones para cambio de nivel al terminar el juego, mostrando menu correspondiente
        if key== arcade.key.KEY_4:
            if puntaje>600:
                mostrar_fin3()
                
            elif  puntaje>230:
                mostrar_fin2()
                
            elif  puntaje<=230:
                mostrar_juego() 
               
        elif key==arcade.key.ENTER:
                mostrar_fin()
class puntaje2 (arcade.View):
    
    def __init__(self):
        #ventana base
        super().__init__()

        
    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_text(f"Tu puntaje final fue de : {puntaje}", 70, height//2-100, arcade.color.BLACK,25) 
        arcade.draw_text("presione tecla '5' para continuar", 70, height//2-200, arcade.color.BLACK,15)
        arcade.draw_text("presione tecla 'ENTER' para finalizar", 70, height//2-300, arcade.color.BLACK,15)
    def on_key_release(self, key, modifiers):
        #condiciones para cambio de nivel al terminar el juego, mostrando menu correspondiente
        if key == arcade.key.KEY_5:
            if puntaje>600:
                mostrar_fin3()
    
            elif  puntaje>230 :
                mostrar_fin2()
              
            elif  puntaje<=230:
                mostrar_juego() 
        elif key==arcade.key.ENTER:

                mostrar_fin()
class puntaje3 (arcade.View):
    
    def __init__(self):
        #ventana base
        super().__init__()

        
    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_text(f"Tu puntaje final fue de : {puntaje}", 70, height//2-100, arcade.color.BLACK,25) 
        arcade.draw_text("presione tecla '6' para continuar", 70, height//2-200, arcade.color.BLACK,15)
        arcade.draw_text("presione tecla 'ENTER' para finalizar", 70, height//2-300, arcade.color.BLACK,15)
    def on_key_release(self, key, modifiers):
        #condiciones para cambio de nivel al terminar el juego, mostrando menu correspondiente
        if key== arcade.key.KEY_6:
            if contador3==0 :
                mostrar_fin3()
        elif key==arcade.key.ENTER:
                mostrar_fin()


def mostrar_inicio():
    global ventana
    inicio = GamePlay()
    ventana.show_view(inicio) 
          
def mostrar_juego():
    global ventana
    juego=Juego()
    juego.setup()
    ventana.show_view(juego)
    
def mostrar_juego2():
    global ventana
    juego2=Juego2()
    juego2.setup()
    ventana.show_view(juego2)
    
def mostrar_juego3():
    global ventana
    juego3=Juego3()
    juego3.setup()
    ventana.show_view(juego3)    

def mostrar_puntaje_1():
    global ventana 
    puntaje_1= puntaje1()
    ventana.show_view(puntaje_1)    
 
def mostrar_puntaje_2():
    global ventana 
    puntaje_2= puntaje2()
    ventana.show_view(puntaje_2)


def mostrar_puntaje_3():
    global ventana 
    puntaje_3= puntaje3()
    ventana.show_view(puntaje_3) 
    
def mostrar_fin():
    global ventana 
    fin= GameOver()
    ventana.show_view(fin)
    
def mostrar_fin2():
    global ventana
    fin2 = GameOver2()
    ventana.show_view(fin2)
    
def mostrar_fin3():
    global ventana
    fin3 = GameOver3()
    ventana.show_view(fin3)
       


def main():
    global ventana
    ventana = MapaDemo()
    mostrar_inicio()

    #mostrar todo en pantalla
    arcade.run()  
main()