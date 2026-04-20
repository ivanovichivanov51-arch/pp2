import pygame

# Инициализация
pygame.init()

# Экран өлшемдері
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

# Түстер
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Доптың қасиеттері
ball_radius = 25
x = WIDTH // 2
y = HEIGHT // 2
speed = 20

# Ойын циклі
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE) # Экранды ақ түспен тазалау
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Батырма басылғанда тексеру
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and y - speed >= ball_radius:
                y -= speed
            if event.key == pygame.K_DOWN and y + speed <= HEIGHT - ball_radius:
                y += speed
            if event.key == pygame.K_LEFT and x - speed >= ball_radius:
                x -= speed
            if event.key == pygame.K_RIGHT and x + speed <= WIDTH - ball_radius:
                x += speed

    # Допты салу
    pygame.draw.circle(screen, RED, (x, y), ball_radius)
    
    pygame.display.flip() # Экранды жаңарту
    clock.tick(60) # Кадр жиілігі (FPS)

pygame.quit()