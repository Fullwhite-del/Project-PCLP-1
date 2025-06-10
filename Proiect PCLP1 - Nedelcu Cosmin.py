import pygame as py
import sys

py.init()

# Culori
VERDE = (20, 40, 9)
ROSU = (191, 15, 2)
METALIC = (169, 169, 169)
MARONIU = (244,164,96)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#font pentru text
font = py.font.Font('freesansbold.ttf', 32)

#sunete
music = py.mixer.music.load('NEDELCU COSMIN PCLP1 PROIECT/Proiect PCLP1 - Nedelcu Cosmin/random silly chip song.ogg')
music_jump = py.mixer.Sound('NEDELCU COSMIN PCLP1 PROIECT/Proiect PCLP1 - Nedelcu Cosmin/random silly chip song.ogg')
py.mixer.music.play(-1)
py.mixer.music.set_volume(0.3)
music_jump.set_volume(0.2)

# creez o platforma generala din care pot crea mai multe PLATFORME

class Platforma:            
    def __init__(self, x, y, width, height, color):
        self.rect = py.Rect(x, y, width, height)
        self.color = color
        self.y = y

    def desenare(self, surface):
        py.draw.rect(surface, self.color, self.rect)

    def modifica_dimensiunea(self, width, height):
        self.rect.width = width
        self.rect.height = height

# PLATFORME
platforme = [
    Platforma(650, 350, 80, 30, METALIC),   # pun cate platforme doresc
    Platforma(80, 450, 80, 30, VERDE),
    Platforma(300, 650, 80, 30, VERDE),
    Platforma(350, 300, 80, 30, VERDE),    
]  

class PEACH():
    def __init__(self, x, y, image_peach):
        self.x = x  # Poziția pe axa X
        self.y = y  # Poziția pe axa Y
        self.image = py.transform.scale(py.image.load(image_peach), (96, 108)) # Încărcarea imaginii
        self.rect = self.image.get_rect(topleft=(self.x, self.y))  # Obiect pentru manipularea poziției

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Desenează imaginea pe ecran

princess = PEACH(800, 280, "NEDELCU COSMIN PCLP1 PROIECT/Proiect PCLP1 - Nedelcu Cosmin/New Piskel.png")
saved_peach = py.image.load('NEDELCU COSMIN PCLP1 PROIECT/Proiect PCLP1 - Nedelcu Cosmin/SAVED_Peach.png')


class MARIO():
    def __init__(self, p_x, p_y, saritura_M, repaus_M ):
        self.p_x = p_x 
        self.p_y = p_y
        self.saritura_M = saritura_M
        self.repaus_M  = repaus_M 

# MARIO
p_x = 50  # Poziția inițială pe axa X
p_y = 800  # Poziția inițială pe axa Y
saritura_M = py.transform.scale(py.image.load('NEDELCU COSMIN PCLP1 PROIECT/Proiect PCLP1 - Nedelcu Cosmin/mario_jumping.png'), (48, 64))
repaus_M = py.transform.scale(py.image.load('NEDELCU COSMIN PCLP1 PROIECT/Proiect PCLP1 - Nedelcu Cosmin/mario_standing.png'), (48, 64))
alergare_M = py.transform.scale(py.image.load('NEDELCU COSMIN PCLP1 PROIECT/Proiect PCLP1 - Nedelcu Cosmin/Mario_sheets_run-1.png.png'), (48, 64))
alergare2_M = py.transform.scale(py.image.load('NEDELCU COSMIN PCLP1 PROIECT/Proiect PCLP1 - Nedelcu Cosmin/MARIO_run2.png'), (48, 64))

animation_run = [alergare_M, alergare2_M]

# Configurări fereastră
screen_width = 1000
screen_height = 1000
py.display.set_caption("Super Mario")
screen = py.display.set_mode((screen_width, screen_height))

clock = py.time.Clock()
fps = 180
fundal = py.image.load('NEDELCU COSMIN PCLP1 PROIECT/Proiect PCLP1 - Nedelcu Cosmin/BACKGROUND1.png')

# Variabile pentru mișcare
viteza_x = 0  # Viteza de mișcare orizontală
viteza_y = 0  # Viteza de mișcare verticală (pentru săritură)

viteza_saritura = -15  # Viteza inițială de săritură
gravitatia = 0.5       # Gravitația aplicată personajului se adauga la saritura pana devine pozitiva si astfel personajul coboara
pe_sol = True          # Starea personajului (dacă este pe sol)
y_sol = p_y            # Poziția solului (înălțimea unde aterizează) 

# Funcție pentru afișarea mesajului Game Over
def game_over():
    font = py.font.SysFont(None, 100)
    text = font.render('Game Over', True, (255, 0, 0))
    screen.blit(text, (screen_width // 3, screen_height // 3))

def show_dialog():
    dialog_running = True
    while dialog_running:
        # crearea unu text box unde apare mesajul printesei peach
        py.draw.rect(screen, BLACK, (100, 400, 600, 200))
        py.draw.rect(screen, WHITE, (110, 410, 580, 180))

        text = font.render("Thanks Mario! You saved me!", True, BLACK)
        screen.blit(text, (120, 450))

        screen.blit(saved_peach, (600, 400))

        # Evenimente
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.KEYDOWN and event.key == py.K_RETURN:
                dialog_running = False

        py.display.flip()

# Bucla principală a jocului
running = True
while running:
    screen.blit(fundal, (0, 0))  # Desenează fundalul

    princess.draw(screen)
    mario_rect = py.Rect(p_x, p_y, 48, 64)  # 48x64 este dimensiunea sprite-ului lui Mario

    moving = False
    # Evenimente
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        
        # Evenimente KEYDOWN pentru control     
        if event.type == py.KEYDOWN:
            if event.key == py.K_UP and pe_sol:  # Dacă Mario e pe sol și apăsăm sageata sus 
                music_jump.play()
                viteza_y = viteza_saritura       # Inițializează săritura
                pe_sol = False                 # Mario nu mai este pe sol
                
            if event.key == py.K_LEFT:          # Mișcare la stânga
                viteza_x = -3

            if event.key == py.K_RIGHT:         # Mișcare la dreapta
                viteza_x = 3
                    
            # Verifică coliziunea cu princess
            if mario_rect.colliderect(princess.rect):
                show_dialog()
                

        # Evenimente KEYUP pentru oprirea mișcării
        if event.type == py.KEYUP:
            if event.key in [py.K_LEFT, py.K_RIGHT]:
                viteza_x = 0

    # Actualizare poziție orizontala
    p_x += viteza_x

    # Actualizare poziție verticală (gravitație și săritură)
    if not pe_sol:              # daca nu este pe sol
        viteza_y += gravitatia  # Gravitația afectează viteza verticală crescand viteza pana ajunge la 0 si mario coboara
        p_y += viteza_y         # Actualizează poziția verticală

        # Verifică dacă Mario atinge solul
    if p_y == y_sol:        
        pe_sol = True       # Mario este pe sol
        viteza_y = 0        # Oprește mișcarea verticala
    
    # Afișare sprite corespunzător stării
    if not pe_sol:
        screen.blit(saritura_M, (p_x, p_y))  # Sprite-ul pentru săritură         
    else:                                                               # efecte de animatie
        screen.blit(repaus_M, (p_x, p_y))   # Sprite-ul pentru repaus

    # desenarea platformei
    for platforma in platforme:
        platforma.desenare(screen)

    for platforma in platforme:
        if p_y + 64 >= platforma.rect.top and p_y + 64 <= platforma.rect.bottom: 
            if p_x + 48 > platforma.rect.left and p_x < platforma.rect.right:
                pe_sol = True
                p_y = platforma.rect.top - 64
                viteza_y = 0

            elif p_x > platforma.rect.right or p_x < platforma.rect.left:
                pe_sol = False

    if mario_rect.x < 0 or mario_rect.x > screen_width or mario_rect.y < 0 or mario_rect.y > screen_height:
        screen.fill(METALIC)
        game_over()
        py.mixer.music.set_volume(0)


    # apelarea unei platforme
    platforme[0].modifica_dimensiunea(200, 50)
    platforme[0].color = VERDE # schimbare culorii platformei 1
    platforme[1].modifica_dimensiunea(200, 50)
    platforme[0].color = VERDE
    platforme[2].modifica_dimensiunea(200, 50)
    platforme[0].color = VERDE
    platforme[3].modifica_dimensiunea(200, 50)
    # platforme.append(Platforma(40, 230, 100, 100, ROSU)) # adaugarea unei noi platforme in lista in timpul jocului
   
    # Actualizare fereastră
    py.display.update()
    clock.tick(180)  # Controlează viteza jocului (180 FPS)
      
py.quit()