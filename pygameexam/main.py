import pygame

pygame.init()
screen = pygame.display.set_mode((600, 300))#flags=pygame.NOFRAME
pygame.display.set_caption("serikzhan product")
icon = pygame.image.load('images/icon9.png')
pygame.display.set_icon(icon)
running = True
while running:
    
    #screen.fill((124, 157, 224))
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                screen.fill((77, 44, 133))
    
    