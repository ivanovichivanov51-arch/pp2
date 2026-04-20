import pygame, random, sys, time

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

# ТАМАҚ ФУНКЦИЯСЫ (Жаңа салмақ пен таймермен)
def spawn_food():
    x = random.randrange(0, SIZE//BLOCK) * BLOCK
    y = random.randrange(0, SIZE//BLOCK) * BLOCK
    weight = random.choice([1, 1, 1, 3]) # 75% жай тамақ (1), 25% супер тамақ (3)
    spawn_time = time.time() # Пайда болған уақыты
    return [x, y, weight, spawn_time]

food = spawn_food()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN': direction = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP': direction = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT': direction = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT': direction = 'RIGHT'

    # ТАЙМЕРДІ ТЕКСЕРУ (2-тапсырма: тамақ біраз уақыттан кейін жоғалады)
    # Егер 5 секунд өтіп кетсе, жаңа тамақ шығады
    if time.time() - food[3] > 5:
        food = spawn_food()

    # Жыланның қозғалысы
    head = list(snake[0])
    if direction == 'UP': head[1] -= BLOCK
    if direction == 'DOWN': head[1] += BLOCK
    if direction == 'LEFT': head[0] -= BLOCK
    if direction == 'RIGHT': head[0] += BLOCK
    snake.insert(0, head)

    # Қабырғаға немесе өзіне соғылу
    if head[0] < 0 or head[0] >= SIZE or head[1] < 0 or head[1] >= SIZE or head in snake[1:]:
        pygame.quit(); sys.exit()

    # Тамақ жеу
    if head[0] == food[0] and head[1] == food[1]:
        score += food[2] # 1-тапсырма: тамақтың салмағын қосу
        
        # Деңгей мен жылдамдықты ұпайға байланысты көтеру
        if score // 5 >= level: 
            level += 1
            speed += 1
            
        food = spawn_food()
        # Егер салмағы 1-ден көп болса, жылан соғұрлым ұзарады
        for _ in range(food[2] - 1):
            snake.append(snake[-1]) 
    else:
        snake.pop()

    screen.fill((0, 0, 0))
    
    # Жыланды салу
    for pos in snake: 
        pygame.draw.rect(screen, (0, 255, 0), (pos[0], pos[1], BLOCK, BLOCK))
    
    # ТАМАҚТЫ САЛУ (Салмағына қарай түсі өзгереді)
    food_color = (255, 0, 0) if food[2] == 1 else (255, 215, 0) # Алтын түс - үлкен тамақ
    pygame.draw.rect(screen, food_color, (food[0], food[1], BLOCK, BLOCK))
    
    # Таймерді экранға шығару (ыңғайлы болу үшін)
    time_left = max(0, int(5 - (time.time() - food[3])))
    pygame.display.set_caption(f"Score: {score}  Level: {level}  Food Timer: {time_left}s")
    
    pygame.display.update()
    clock.tick(speed)