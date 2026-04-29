import pygame
import datetime
from tools import flood_fill

pygame.init()

# Баптаулар
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
canvas = pygame.Surface((WIDTH, HEIGHT)) # Нақты сурет осында салынады
canvas.fill((255, 255, 255))

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Күйлер (Variables)
drawing = False
current_tool = 'pencil'
color = (0, 0, 0)
brush_size = 2
start_pos = None

# Текст құралы үшін
text_active = False
user_text = ""
text_pos = (0, 0)

running = True
while running:
    screen.fill((200, 200, 200)) # Артқы фон (сұр)
    screen.blit(canvas, (0, 0))   # Канвасты экранға шығару
    
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Құралдарды перне тақта арқылы ауыстыру
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: brush_size = 2
            if event.key == pygame.K_2: brush_size = 5
            if event.key == pygame.K_3: brush_size = 10
            
            # Сақтау (Ctrl + S)
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                pygame.image.save(canvas, f"paint_{timestamp}.png")
                print("Сурет сақталды!")

            # Текст енгізу логикасы
            if text_active:
                if event.key == pygame.K_RETURN:
                    txt_surf = font.render(user_text, True, color)
                    canvas.blit(txt_surf, text_pos)
                    text_active = False
                    user_text = ""
                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
            if current_tool == 'fill':
                flood_fill(canvas, event.pos[0], event.pos[1], color)
            if current_tool == 'text':
                text_active = True
                text_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and current_tool == 'line':
                pygame.draw.line(canvas, color, start_pos, event.pos, brush_size)
            drawing = False

        if event.type == pygame.MOUSEMOTION and drawing:
            if current_tool == 'pencil':
                # consecutive mouse positions
                pygame.draw.line(canvas, color, start_pos, event.pos, brush_size)
                start_pos = event.pos

    # Live Preview (Түзу сызықтың алдын-ала көрінісі)
    if drawing and current_tool == 'line':
        pygame.draw.line(screen, color, start_pos, mouse_pos, brush_size)

    # Экранда текст жазылып жатса көрсету
    if text_active:
        temp_text = font.render(user_text + "|", True, color)
        screen.blit(temp_text, text_pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()