import pygame
import random
import color_detection as cd
import shape_detection as sd
import cv2
import time

# -----------------------------------------------------------#
# ------------------------INIT PYGAME------------------------#
pygame.init()

screen = pygame.display.set_mode([640, 480])
pygame.display.set_caption("Geometric Shapes Exergame")

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

# -----------------------------------------------------------#
# --------------------LOAD FILES-----------------------------#

# FONTS
font_path = "resources/fonts/OpenDyslexic-Regular.otf"
font = pygame.font.Font(font_path, 24)

# IMAGES
background_init = pygame.image.load("resources/images/background_init.jpg")
background_init = pygame.transform.scale(background_init, (640, 480))

background_playing = pygame.image.load("resources/images/background.jpg")
background_playing = pygame.transform.scale(background_playing, (640, 480))

# helps images
helper = []
help_red_circle = pygame.image.load("resources/images/ayudas/circulo rojo ayuda.png")
helper.append(help_red_circle)
help_blue_circle = pygame.image.load("resources/images/ayudas/circulo azul ayuda.png")
helper.append(help_blue_circle)
help_green_circle = pygame.image.load("resources/images/ayudas/circulo verde ayuda.png")
helper.append(help_green_circle)
help_red_square = pygame.image.load("resources/images/ayudas/cuadrado rojo ayuda.png")
helper.append(help_red_square)
help_blue_square = pygame.image.load("resources/images/ayudas/cuadrado azul ayuda.png")
helper.append(help_blue_square)
help_green_squar = pygame.image.load("resources/images/ayudas/cuadrado verde ayuda.png")
helper.append(help_green_squar)
help_red_tri = pygame.image.load("resources/images/ayudas/triangulo rojo ayuda.png")
helper.append(help_red_tri)
help_blue_tri = pygame.image.load("resources/images/ayudas/triangulo azul ayuda.png")
helper.append(help_blue_tri)
help_green_tri = pygame.image.load("resources/images/ayudas/triangulo verde ayuda.png")
helper.append(help_green_tri)
# scale help images
original_width, original_height = helper[0].get_size()
aspect_ratio = original_height / original_width
target_width = 270
target_height = int(target_width * aspect_ratio)
for i in range(len(helper)):
    helper[i] = pygame.transform.scale(helper[i], (target_width, target_height))
print(helper[0].get_size())
# SOUNDS
sounds = []
circle_red = pygame.mixer.Sound("resources/sounds/circulo rojo.mp3")
sounds.append(circle_red)
circle_blue = pygame.mixer.Sound("resources/sounds/circulo azul.mp3")
sounds.append(circle_blue)
circle_green = pygame.mixer.Sound("resources/sounds/circulo verde.mp3")
sounds.append(circle_green)
square_red = pygame.mixer.Sound("resources/sounds/cuadrado rojo.mp3")
sounds.append(square_red)
square_blue = pygame.mixer.Sound("resources/sounds/cuadrado azul.mp3")
sounds.append(square_blue)
square_green = pygame.mixer.Sound("resources/sounds/cuadrado verde.mp3")
sounds.append(square_green)
triangle_red = pygame.mixer.Sound("resources/sounds/triangulo rojo.mp3")
sounds.append(triangle_red)
triangle_blue = pygame.mixer.Sound("resources/sounds/triangulo azul.mp3")
sounds.append(triangle_blue)
triangle_green = pygame.mixer.Sound("resources/sounds/triangulo verde.mp3")
sounds.append(triangle_green)
# others sounds
notify_sounds = []
nice_job_sound = pygame.mixer.Sound("resources/sounds/bien_hecho.mp3")
notify_sounds.append(nice_job_sound)

for s in sounds:
    s.set_volume(0.6)

for s in notify_sounds:
    s.set_volume(0.6)
# ------------------------------------------------------------#
# --------------------GAME PARAMETERS-------------------------#

# BUTTONS
button_width = 200
button_height = 100
button_x = (640 - button_width) // 2
button_y = (480 - button_height) // 2

button_start = pygame.Rect(button_x, button_y, button_width, button_height)
button_continue = pygame.Rect(button_x, button_y, button_width, button_height)

# SHAPE AND COLORS
shapes = ["circulo", "cuadrado", "triangulo"]
colors = ["rojo", "azul", "verde"]

param_colors = []
red_params = [155, 15, 110, 255, 150, 255]
param_colors.append(red_params)
blue_params = [90, 120, 90, 255, 0, 255]
param_colors.append(blue_params)
green_params = [35, 65, 70, 255, 0, 255]
param_colors.append(green_params)

param_colors2 = [[7, 182, 212], [105, 157, 128], [50, 162, 128]]

# GENERAL
WHITE = (255, 255, 255)
BLUE = (44, 145, 157)
BLACK = (0, 0, 0)

level = 0
help = False
state = "init"  # GAME STATES: init - playing - paused - exit

# ------------------------------------------------------------#
# ------------------------FUNCTIONS---------------------------#


# Función para dibujar un botón
def draw_button(button, text, color):
    pygame.draw.rect(screen, color, button)
    text = font.render(text, True, WHITE)
    text_rect = text.get_rect(center=button.center)
    screen.blit(text, text_rect)


# Función para dibujar texto en la pantalla
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Función para mostrar una imagen en pantalla
def draw_image(image, surface, x, y):
    # print("image:", image)
    image_rect = image.get_rect()
    image_rect.center = (x, y)
    surface.blit(image, image_rect)


# Funcion que devuelve un color, forma y sonido aleatorio
def random_shape_color():
    idx_shape = random.randint(0, 2)
    # idx_shape = 1
    idx_color = random.randint(0, 2)
    # idx_color = 0
    idx_sound = idx_shape * 3 + idx_color
    idx_help = idx_sound
    color = colors[idx_color]
    param_color = param_colors[idx_color]
    # param_color = param_colors2[idx_color]
    shape = shapes[idx_shape]
    sound = sounds[idx_sound]
    help_image = helper[idx_help]

    return shape, color, sound, param_color, help_image


# Funcion de dibujado y actualizacion de pantalla
def draw_screen(state, level, help, shape="", color="", help_image=[]):
    screen.fill(WHITE)
    if state == "init":
        screen.blit(background_init, (0, 0))
        draw_button(button_start, "Empezar", BLUE)
    elif state == "playing":
        screen.blit(background_playing, (0, 0))
        if help:
            draw_text("Levante el " + shape + " " + color, font, BLACK, screen, 160, 85)
            draw_image(help_image, screen, frameWidth // 2, frameHeight // 2 + 20)
        else:
            draw_text(
                "Levante el " + shape + " " + color, font, BLACK, screen, 160, 220
            )
    elif state == "paused":
        screen.blit(background_playing, (0, 0))
        draw_text("Bien hecho! ", font, BLACK, screen, 260, 220)
    elif state == "finished":
        screen.blit(background_init, (0, 0))
        draw_text(
            "¡Felicitaciones!",
            font,
            WHITE,
            screen,
            225,
            90,
        )
        draw_text("Has completado el juego.", font, WHITE, screen, 160, 130)
        draw_button(button_continue, "Volver a jugar", BLUE)
        # print("llego aca")

    pygame.display.flip()


# Variables globales
global shape
global color
shape = ""
param_color = []
help_image = []
color = ""
camera_mode = 3
count = 0
time_wait = 10  # segundos
time_init = time.time()
# ------------------------------------------------------------#
# -----------------------MAIN LOOP----------------------------#
running = True
help = False

while running:
    # print(state)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
                print("Saliendo del juego...")
            if event.key == pygame.K_0:
                camera_mode = 0  # imagen original
            if event.key == pygame.K_1:
                camera_mode = 1  # segmentación de color
            if event.key == pygame.K_2:
                camera_mode = 2  # bordes
            if event.key == pygame.K_3:
                camera_mode = 3  # detector de formas

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_start.collidepoint(event.pos):
                state = "playing"
                level = 1
                help = False
                draw_screen(state, level, help)
                time_init = time.time()
                shape, color, sound, param_color, help_image = random_shape_color()
                pygame.time.delay(1000)
                sound.play()
            elif button_continue.collidepoint(event.pos):
                state = "playing"
                level += 1
                help = False
                time_init = time.time()
                draw_screen(state, level, help)
                shape, color, sound, param_color, help_image = random_shape_color()
                pygame.time.delay(1000)
                sound.play()

    draw_screen(state, level, help, shape, color, help_image)

    if state == "playing":
        ok, img = cap.read()

        # color segmentation
        imgSegmentation = cd.color_segmentation(img, param_color)
        # threshold = 5
        # imgSegmentation = cd.color_segmentation2(img, param_color, threshold)

        # edges
        imgCanny = sd.getEdges(imgSegmentation)

        # contours
        imgContour = img.copy()
        success, imgContour = sd.getContours(imgCanny, imgContour, shape)

        # check time to help
        time_elapsed = time.time() - time_init
        if help == False and time_elapsed >= time_wait:
            help = True
            pygame.time.delay(1000)
            sound.play()


        # check match
        if success:
            print("Paleta detectada")
            state = "paused"
            count += 1
            print("contador:", count)
        # Testing modes
        if camera_mode == 1:
            cv2.imshow("Result", imgSegmentation)
        elif camera_mode == 2:
            cv2.imshow("Result", imgCanny)
        elif camera_mode == 3:
            cv2.imshow("Result", imgContour)
        else:
            cv2.imshow("Result", img)

    elif state == "paused":
        print("pausa")
        help = False
        draw_screen(state, level, help)
        sound = notify_sounds[0]
        pygame.time.wait(1000)
        sound.play()
        pygame.time.wait(2000)
        if count == 5:
            count = 0
            state = "finished"
        else:
            shape, color, sound, param_color, help_image = random_shape_color()
            pygame.time.wait(1000)
            sound.play()
            state = "playing"
            time_init = time.time()

    elif state == "finished":
        draw_screen(state, level, help)


# Done! Time to quit.
pygame.quit()
