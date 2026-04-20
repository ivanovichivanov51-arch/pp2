import pygame
import datetime

# 1. Инициализация
pygame.init()

# Экран өлшемін суреттің өлшеміне сәйкес жасайық (мысалы, 800x800)
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Mouse Clock")

# 2. Суреттерді жүктеу (СІЗДЕГІ АТТАРМЕН)
try:
    mickey_face = pygame.image.load('mickeys_clock/images/clock.png')
    hand_left = pygame.image.load('mickeys_clock/images/left_hand.png')
    hand_right = pygame.image.load('mickeys_clock/images/hand_right_centered.png')
    
    # Суреттерді экранға сыйғызу (800x800)
    mickey_face = pygame.transform.scale(mickey_face, (WIDTH, HEIGHT))
except pygame.error as e:
    print(f"Суретті жүктеу мүмкін емес: {e}")
    pygame.quit()
    exit()

def rotate_center(image, angle):
    """Суретті ортасынан айналдыру функциясы"""
    rotated_image = pygame.transform.rotate(image, -angle)
    # Ортасын (400, 400) нүктесінде сақтап қалу
    new_rect = rotated_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    return rotated_image, new_rect

# 3. Ойын циклі
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Уақытты алу
    now = datetime.datetime.now()
    seconds = now.second
    minutes = now.minute

    # Бұрыштарды есептеу және түзету
    # Егер қол сағат 10-ды көрсетіп тұрса, демек оны шамамен 60-90 градусқа бұру керек
    sec_angle = (seconds * 6)    # 65-тің орнына басқа сан қойып көр (мысалы 90)
    min_angle = (minutes * 6) -10 # Екі қол бір бағытта болуы үшін

    # Экранды тазалау
    screen.fill((255, 255, 255))
    
    # 1. Сағат бетін салу
    screen.blit(mickey_face, (0, 0))

    # 2. Минуттық қолды салу (right_hand)
    surf_m, rect_m = rotate_center(hand_right, min_angle)
    screen.blit(surf_m, rect_m)

    # 3. Секундтық қолды салу (left_hand)
    surf_s, rect_s = rotate_center(hand_left, sec_angle)
    screen.blit(surf_s, rect_s)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()