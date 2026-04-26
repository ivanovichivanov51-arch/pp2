import pygame
import sys
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))

clock = pygame.time.Clock()

color = (0, 0, 0)
mode = 'line'   # line, rect, circle, eraser
start_pos = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 🎨 Түс таңдау
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                color = (255, 0, 0)
            if event.key == pygame.K_g:
                color = (0, 255, 0)
            if event.key == pygame.K_b:
                color = (0, 0, 255)

            # 🔧 Режимдер
            if event.key == pygame.K_1:
                mode = 'line'
            if event.key == pygame.K_2:
                mode = 'rect'
            if event.key == pygame.K_3:
                mode = 'circle'
            if event.key == pygame.K_4:
                mode = 'eraser'

        # 🖱️ Тышқан басу
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = event.pos

        # 🖱️ Жіберу (фигуралар үшін)
        if event.type == pygame.MOUSEBUTTONUP:
            end_pos = event.pos

            if mode == 'rect':
                rect = pygame.Rect(
                    start_pos[0],
                    start_pos[1],
                    end_pos[0] - start_pos[0],
                    end_pos[1] - start_pos[1]
                )
                pygame.draw.rect(screen, color, rect, 2)

            elif mode == 'circle':
                radius = int(math.hypot(
                    end_pos[0] - start_pos[0],
                    end_pos[1] - start_pos[1]
                ))
                pygame.draw.circle(screen, color, start_pos, radius, 2)

    # ✏️ Еркін сызық (line)
    if pygame.mouse.get_pressed()[0] and mode == 'line':
        pygame.draw.circle(screen, color, pygame.mouse.get_pos(), 4)

    # 🧽 Өшіргіш
    if pygame.mouse.get_pressed()[0] and mode == 'eraser':
        pygame.draw.circle(screen, (255, 255, 255), pygame.mouse.get_pos(), 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()