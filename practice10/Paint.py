import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))
clock = pygame.time.Clock()

color = (0, 0, 0)
mode = 'line' # 'rect', 'circle', 'eraser'
start_pos = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: color = (255, 0, 0) # Қызыл
            if event.key == pygame.K_g: color = (0, 255, 0) # Жасыл
            if event.key == pygame.K_rect: mode = 'rect'
            if event.key == pygame.K_c: mode = 'circle'
            if event.key == pygame.K_e: color = (255, 255, 255) # Өшіргіш

        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            end_pos = event.pos
            if mode == 'rect':
                pygame.draw.rect(screen, color, (start_pos[0], start_pos[1], end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]), 2)
            elif mode == 'circle':
                rad = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                pygame.draw.circle(screen, color, start_pos, rad, 2)
    
    # Еркін салу (тышқан басылып тұрғанда)
    if pygame.mouse.get_pressed()[0] and not mode in ['rect', 'circle']:
        pygame.draw.circle(screen, color, pygame.mouse.get_pos(), 5)

    pygame.display.update()
    clock.tick(60)