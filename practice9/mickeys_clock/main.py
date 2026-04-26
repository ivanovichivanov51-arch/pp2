import pygame
import datetime
import sys

# 1. Инициализация
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Mouse Clock")

CENTER = (WIDTH // 2, HEIGHT // 2)

# 2. Суреттерді жүктеу
try:
    mickey_face = pygame.image.load('mickeys_clock/images/clock.png')
    mickey_face = pygame.transform.scale(mickey_face, (WIDTH, HEIGHT))
    
    hand_left_raw = pygame.image.load('mickeys_clock/images/left_hand.png')
    hand_right_raw = pygame.image.load('mickeys_clock/images/hand_right_centered.png')
    
    
    
    # ОҢ ҚОЛ (Right hand) - Ұзынырақ және жіңішке
    RIGHT_HAND_WIDTH = 550  # Ұзындығын тағы арттырдық
    RIGHT_HAND_HEIGHT = 100  # Жіңішкелігі
    
    # СОЛ ҚОЛ (Left hand) - Бастапқы қалыпқа жақын
    LEFT_HAND_WIDTH = 800   
    LEFT_HAND_HEIGHT = 500
       

    hand_right = pygame.transform.scale(hand_right_raw, (RIGHT_HAND_WIDTH, RIGHT_HAND_HEIGHT))
    hand_left = pygame.transform.scale(hand_left_raw, (LEFT_HAND_WIDTH, LEFT_HAND_HEIGHT))
    # ---------------------------------------------------------

    mickey_static = pygame.image.load('mickeys_clock/images/mickey_body.png')
    mickey_static = pygame.transform.scale(mickey_static, (300, 300))
    
except pygame.error as e:
    print(f"Қате: {e}")
    pygame.quit()
    sys.exit()

def rotate_hand(image, angle, center_pos):
    """Суретті центрін сақтап айналдыру"""
    rotated_image = pygame.transform.rotate(image, -angle)
    new_rect = rotated_image.get_rect(center=center_pos)
    return rotated_image, new_rect

# 3. Цикл
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()
    
    # Градустарды баптау
    # Егер қолдардың бағыты бұрыс болса, +90 санын өзгертіңіз
    sec_angle = (now.second * 6) + 90
    min_angle = (now.minute * 6) -30

    screen.fill((255, 255, 255))
    
    # 1. Циферблат
    screen.blit(mickey_face, (0, 0))

    # 2. Айналмайтын дене
    static_rect = mickey_static.get_rect(center=CENTER)
    screen.blit(mickey_static, static_rect)

    # 3. Оң қол (Минуттық - Ұзын)
    surf_m, rect_m = rotate_hand(hand_right, min_angle, CENTER)
    screen.blit(surf_m, rect_m)

    # 4. Сол қол (Секундтық - Қысқалау)
    surf_s, rect_s = rotate_hand(hand_left, sec_angle, CENTER)
    screen.blit(surf_s, rect_s)

    pygame.display.flip()
    clock.tick()