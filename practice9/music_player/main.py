import pygame
import os

# 1. Инициализация
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

# ПАПКА ЖОЛЫН ДҰРЫСТАУ (Ең маңызды жері)
# Бұл файлдың (main.py) тұрған жерін табады
current_dir = os.path.dirname(os.path.abspath(__file__))
# Соның ішіндегі 'music' папкасына жол сілтейді
music_dir = os.path.join(current_dir, "music")

# Әндерді жинау
songs = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]

current_index = 0

def play_song(index):
    path = os.path.join(music_dir, songs[index])
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

# Түстер
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
font = pygame.font.SysFont("Arial", 22)

running = True
is_playing = False

while running:
    screen.fill((20, 20, 20))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: # Play
                if not is_playing:
                    play_song(current_index)
                    is_playing = True
                else:
                    pygame.mixer.music.unpause()
            if event.key == pygame.K_s: # Stop/Pause
                pygame.mixer.music.pause()
            if event.key == pygame.K_n: # Next
                current_index = (current_index + 1) % len(songs)
                play_song(current_index)
                is_playing = True
            if event.key == pygame.K_b: # Back
                current_index = (current_index - 1) % len(songs)
                play_song(current_index)
                is_playing = True

    # Экранға ақпарат шығару
    if songs:
        text = font.render(f"Ойнап тұр: {songs[current_index]}", True, GREEN)
        screen.blit(text, (50, 150))
    
    help_text = font.render("P: Play | S: Pause | N: Next | B: Back", True, WHITE)
    screen.blit(help_text, (50, 300))
    
    pygame.display.flip()

pygame.quit()