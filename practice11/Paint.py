import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))
clock = pygame.time.Clock()

color = (0, 0, 0)
mode = 'line' 
start_pos = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: color = (255, 0, 0) # Қызыл түс
            if event.key == pygame.K_g: color = (0, 255, 0) # Жасыл түс
            if event.key == pygame.K_e: color = (255, 255, 255) # Өшіргіш
            if event.key == pygame.K_l: mode = 'line' # Еркін салу
            
            # ЖАҢА ФИГУРАЛАР (3-тапсырма)
            if event.key == pygame.K_s: mode = 'square' # Квадрат
            if event.key == pygame.K_t: mode = 'right_triangle' # Тікбұрышты үшбұрыш
            if event.key == pygame.K_a: mode = 'equilateral_triangle' # Тең қабырғалы
            if event.key == pygame.K_d: mode = 'rhombus' # Ромб

        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            end_pos = event.pos
            x1, y1 = start_pos
            x2, y2 = end_pos
            width = x2 - x1
            height = y2 - y1

            # 1. Квадрат салу
            if mode == 'square':
                side = min(abs(width), abs(height)) # Тең қабырғалы болуы үшін
                s_x = x1 if width > 0 else x1 - side
                s_y = y1 if height > 0 else y1 - side
                pygame.draw.rect(screen, color, (s_x, s_y, side, side), 2)

            # 2. Тікбұрышты үшбұрыш (Right triangle)
            elif mode == 'right_triangle':
                points = [(x1, y1), (x1, y2), (x2, y2)]
                pygame.draw.polygon(screen, color, points, 2)

            # 3. Тең қабырғалы үшбұрыш (Equilateral triangle)
            elif mode == 'equilateral_triangle':
                side = abs(width)
                h = side * math.sqrt(3) / 2 # Биіктігін есептеу
                points = [(x1, y1), (x1 + side, y1), (x1 + side / 2, y1 - h)]
                pygame.draw.polygon(screen, color, points, 2)

            # 4. Ромб (Rhombus)
            elif mode == 'rhombus':
                points = [
                    (x1 + width / 2, y1),        # Жоғарғы нүкте
                    (x1 + width, y1 + height / 2), # Оң жақ нүкте
                    (x1 + width / 2, y1 + height), # Төменгі нүкте
                    (x1, y1 + height / 2)        # Сол жақ нүкте
                ]
                pygame.draw.polygon(screen, color, points, 2)

            # Бұрынғы фигуралар
            elif mode == 'rect':
                pygame.draw.rect(screen, color, (x1, y1, width, height), 2)
            elif mode == 'circle':
                rad = int((width**2 + height**2)**0.5)
                pygame.draw.circle(screen, color, start_pos, rad, 2)
    
    # Еркін салу (Егер режим 'line' болса)
    if pygame.mouse.get_pressed()[0] and mode == 'line':
        pygame.draw.circle(screen, color, pygame.mouse.get_pos(), 5)

    pygame.display.update()
    clock.tick(60)