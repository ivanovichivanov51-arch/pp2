import pygame

class Button:
    def __init__(self, x, y, w, h, text, color=(100, 100, 100)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        # Mouse hover effect
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (150, 150, 150), self.rect, 3)
        
        txt_surf = font.render(self.text, True, (255, 255, 255))
        screen.blit(txt_surf, (self.rect.centerx - txt_surf.get_width()//2, 
                             self.rect.centery - txt_surf.get_height()//2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_text(screen, text, size, x, y, color=(255, 255, 255), center=False):
    font = pygame.font.SysFont("Verdana", size)
    surf = font.render(text, True, color)
    if center:
        x = screen.get_width() // 2 - surf.get_width() // 2
    screen.blit(surf, (x, y))