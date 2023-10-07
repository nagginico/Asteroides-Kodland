import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Asteroides")

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
GrisPlata = (192, 192, 192)

# Cargar la imagen de la nave y redimensionarla
nave_img = pygame.image.load('img/naveUsuario.png')  # Asegúrate de que el archivo 'nave.png' esté en el mismo directorio
nave_img = pygame.transform.scale(nave_img, (60, 40))  # Redimensionar a 50x30 píxeles

# Cargar imagen de asteroide y redimensionar
asteroide_img = pygame.image.load('img/asteroide.png')
asteroide_img = pygame.transform.scale(asteroide_img, (50, 50))

# Función para dibujar
def dibujar_nave(x, y):
    pantalla.blit(nave_img, (x, y))

def dibujar_asteroide(x, y):
    pantalla.blit(asteroide_img, (x, y))

def dibujar_vidas(vidas):
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render(f'Vidas: {vidas}', True, BLANCO)
    pantalla.blit(texto, (10, 10))
    
# Funcion para respetar un espacio entre ellos
def generar_asteroide_con_espacio(espacio):
    x = ANCHO
    y = random.randint(50, ALTO - 50)
    return x, y - espacio
# Limitaciones x ventana
def limitar_nave( y):
    if y < 0:
        y = 0
    elif y > ALTO - 50:  # Alto de la nave
        y = ALTO - 50
    return  y

# Función para parpadear la nave cuando está en modo invencible
def parpadear_nave(nave_x, nave_y):
    if pygame.time.get_ticks() % 500 < 250:  # Cambia cada 250 milisegundos (parpadeo rápido)
        dibujar_nave(nave_x, nave_y)
#Funcion para el sistema de puntaje
def otorgar_puntos(tiempo):
    # Por ejemplo, se pueden otorgar 10 puntos por cada segundo
    return int(tiempo // 1000 * 10) # Convertir milisegundos a segundos y otorgar 10 puntos por segundo

# Función para dibujar texto
def dibujar_texto(texto, fuente, color, x, y):
    superficie = fuente.render(texto, True, color)
    pantalla.blit(superficie, (x, y))

# Función para mostrar el menú
def mostrar_menu():
    fuenteM = pygame.font.Font(None, 80)
    fuente = pygame.font.Font(None, 50)
    opciones = ["Empezar", "Salir"]
    seleccion = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if opciones[seleccion] == "Empezar":
                        return "juego"
                    elif opciones[seleccion] == "Salir":
                        pygame.quit()
                        sys.exit()

        # Limpiar pantalla
        pantalla.fill(NEGRO)
        
        # Dibujar texto seleccionables del menú
        for i, opcion in enumerate(opciones):
            color = VERDE if i == seleccion else NEGRO
            dibujar_texto(opcion, fuente, GrisPlata, 300, 200 + i * 50)
        # Dibujar texto Menu
        dibujar_texto("Menú", fuenteM, GrisPlata, 300, 50)
        # Encerrar la opción seleccionada en un cuadrado
        pygame.draw.rect(pantalla, GrisPlata, (280, 190 + seleccion * 50, 250, 50), 3)


        
        

        # Actualizar pantalla
        pygame.display.flip()

# Función para el juego
def empezar_juego():
    nave_x, nave_y = ANCHO // 8, ALTO // 2
    reloj = pygame.time.Clock()
    vidas = 3
    tiempo_inicial = pygame.time.get_ticks()
    n = 1
    espacio_entre_asteroides = 200
    asteroides = []
    
    
    invencible = False
    invencible_tiempo = 0
     
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            nave_y -= 5
        if teclas[pygame.K_DOWN]:
            nave_y += 5
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - tiempo_inicial
            
        # Calcular puntos
        puntos = otorgar_puntos(tiempo_transcurrido)  
        # Aplicar restricciones de movimiento a la nave
        nave_y = limitar_nave(nave_y)
        # Generar asteroide aleatorio con espacio
        if random.randint(1, 20) == 1:  # Probabilidad de generación de asteroide (1/20)
            asteroides.append(generar_asteroide_con_espacio(espacio_entre_asteroides))
            
        # Mover asteroides
        for i in range(len(asteroides)):
            asteroides[i] = (asteroides[i][0] - 5, asteroides[i][1])  # Mover en dirección negativa en x
            
        # Verificar colisión con asteroide
        if not invencible:  # Solo si no está en modo invencible
            for asteroide in asteroides:
                if nave_x < asteroide[0] + 50 and nave_x + 50 > asteroide[0] and nave_y < asteroide[1] + 50 and nave_y + 50 > asteroide[1]:
                    vidas -= 1
                    if vidas == 0:
                        return "menu"
                    else:
                        invencible = True
                        invencible_tiempo = pygame.time.get_ticks()
                        
        # Modo invencible
        if invencible:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - invencible_tiempo > 5000:  # 5000 milisegundos = 5 segundos
                invencible = False


 
        # Limpiar pantalla
        pantalla.fill(NEGRO)
        
         # Dibujar asteroides
        for asteroide in asteroides:
            dibujar_asteroide(asteroide[0], asteroide[1])
                    
        # Dibujar nave (parpadeo si está en modo invencible)
        if not invencible or pygame.time.get_ticks() % 500 < 250:
            dibujar_nave(nave_x, nave_y)
        # Dibujar contador de vidas
        dibujar_vidas(vidas)
        # Mostrar puntos
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(f'Puntos: {puntos}', True, BLANCO)
        pantalla.blit(texto, (10, 50))

        # Actualizar pantalla
        pygame.display.flip()

        # Controlar la velocidad del juego
        reloj.tick(50+n)
        
         # Verificar si el jugador perdió todas las vidas
        if vidas == 0:
            return "menu"
        n += 0.050
# Main
if __name__ == "__main__":
    while True:
        resultado = mostrar_menu()
        if resultado == "juego":
            resultado = empezar_juego()
            if resultado == "menu":
                resultado = mostrar_menu()