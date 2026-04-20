import pygame, random, sys

pygame.init()

# Экран
SIZE = 400
screen = pygame.display.set_mode((SIZE, SIZE))
clock = pygame.time.Clock()

# Параметрлер
BLOCK = 20
score = 0
level = 1
speed = 10

snake = [[100, 100], [80, 100], [60, 100]]
direction = 'RIGHT'
food = [random.randrange(1, SIZE//BLOCK)*BLOCK, random.randrange(1, SIZE//BLOCK)*BLOCK]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN': direction = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP': direction = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT': direction = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT': direction = 'RIGHT'

    # Жыланның қозғалысы
    head = list(snake[0])
    if direction == 'UP': head[1] -= BLOCK
    if direction == 'DOWN': head[1] += BLOCK
    if direction == 'LEFT': head[0] -= BLOCK
    if direction == 'RIGHT': head[0] += BLOCK
    snake.insert(0, head)

    # Қабырғаға немесе өзіне соғылу (Game Over)
    if head[0] < 0 or head[0] >= SIZE or head[1] < 0 or head[1] >= SIZE or head in snake[1:]:
        pygame.quit(); sys.exit()

    # Тамақ жеу
    if head == food:
        score += 1
        if score % 3 == 0: # Әр 3 тамақ сайын деңгей өседі
            level += 1
            speed += 2
        food = [random.randrange(1, SIZE//BLOCK)*BLOCK, random.randrange(1, SIZE//BLOCK)*BLOCK]
    else:
        snake.pop()

    screen.fill((0, 0, 0))
    for pos in snake: pygame.draw.rect(screen, (0, 255, 0), (pos[0], pos[1], BLOCK, BLOCK))
    pygame.draw.rect(screen, (255, 0, 0), (food[0], food[1], BLOCK, BLOCK))
    
    pygame.display.set_caption(f"Score: {score}  Level: {level}")
    pygame.display.update()
    clock.tick(speed)
    