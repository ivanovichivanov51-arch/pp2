import pygame
import random
import sys

# Ойынды іске қосу
pygame.init()

# Экран өлшемдері
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game - Serikzhan")

# Түстер
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)      # Бағалы тиын түсі
SILVER = (192, 192, 192)  # Жай тиын түсі

# Ойын параметрлері
FPS = 60
SCORE = 0
ENEMY_SPEED = 5           # Қарсыластың бастапқы жылдамдығы
N = 10                    # Әр N тиын сайын жылдамдық артады
font = pygame.font.SysFont("Verdana", 20)

# Ойыншының көлігі
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < WIDTH:        
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)

# ҚАРСЫЛАС КЛАСЫ (Жылдамдықты тексеру үшін қосылды)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH-40), 0)

    def move(self):
        self.rect.move_ip(0, ENEMY_SPEED) # ENEMY_SPEED айнымалысын қолданамыз
        if self.rect.top > HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH-40), 0)

# ТИЫН КЛАСЫ (1-ші тапсырма: әртүрлі салмақ)
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Кездейсоқ салмақ: 1 немесе 3 ұпай
        self.weight = random.choice([1, 1, 1, 3]) 
        self.image = pygame.Surface((30, 30))
        
        # Салмағына қарай түсін өзгертеміз
        if self.weight == 3:
            self.image.fill(GOLD)   # Бағалы тиын
        else:
            self.image.fill(SILVER) # Жай тиын
            
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH-40), 0)

    def move(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > HEIGHT:
            self.reset()

    def reset(self):
        # Тиынды жаңа салмақпен және орынмен қайта шығару
        self.weight = random.choice([1, 1, 1, 3])
        if self.weight == 3:
            self.image.fill(GOLD)
        else:
            self.image.fill(SILVER)
        self.rect.top = 0
        self.rect.center = (random.randint(40, WIDTH-40), 0)

# Спрайттарды баптау
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Ойын циклі
clock = pygame.time.Clock()
last_speed_upgrade = 0 # Соңғы рет жылдамдық қашан өскенін бақылау

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)
    
    # Статистиканы көрсету
    scores = font.render(f"Coins: {SCORE}", True, BLACK)
    speed_text = font.render(f"Speed: {ENEMY_SPEED}", True, BLACK)
    screen.blit(scores, (WIDTH - 120, 10))
    screen.blit(speed_text, (10, 10))

    # Спрайттарды қозғалту және суретін салу
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    # ТИЫН ЖИНАУ ЛОГИКАСЫ
    if pygame.sprite.spritecollideany(P1, coins):
        SCORE += C1.weight  # Тиынның өз салмағын қосамыз
        C1.reset()          # Тиынды қайта баптаймыз

        # 2-ші тапсырма: Әр N тиын сайын Enemy жылдамдығын арттыру
        if SCORE // N > last_speed_upgrade:
            ENEMY_SPEED += 1
            last_speed_upgrade = SCORE // N

    # Қарсыласпен соқтығысу (Ойын аяқталуы)
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.quit()
        sys.exit()

    pygame.display.update()
    clock.tick(FPS)