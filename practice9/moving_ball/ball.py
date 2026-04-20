import pygame

# 1. Инициализация
pygame.init()

# Экран өлшемдері
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

# Түстер
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Доптың бастапқы күйі
ball_radius = 25
x = WIDTH // 2  # Экранның ортасы
y = HEIGHT // 2
speed = 20      # Бір басқандағы қозғалыс қадамы

# Ойын циклі
running = True
clock = pygame.time.Clock()

while running:
    # Экранды әр кадр сайын ақ түспен бояп тұрамыз
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Батырмалар басылғандағы логика
        if event.type == pygame.KEYDOWN:
            # Жоғары (Экран шекарасынан шықпауын тексеру)
            if event.key == pygame.K_UP and y - speed >= ball_radius:
                y -= speed
            # Төмен
            if event.key == pygame.K_DOWN and y + speed <= HEIGHT - ball_radius:
                y += speed
            # Солға
            if event.key == pygame.K_LEFT and x - speed >= ball_radius:
                x -= speed
            # Оңға
            if event.key == pygame.K_RIGHT and x + speed <= WIDTH - ball_radius:
                x += speed

    # Допты (шеңберді) салу
    pygame.draw.circle(screen, RED, (x, y), ball_radius)
    
    # Экранды жаңарту
    pygame.display.flip()
    
    # Кадр жиілігін 60 FPS-ке шектеу
    clock.tick(60)

pygame.quit()