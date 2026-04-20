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
YELLOW = (255, 255, 0) # Тиынның түсі

# Ойын параметрлері
FPS = 60
SCORE = 0
font = pygame.font.SysFont("Verdana", 20)

# Ойыншының көлігі (қарапайым тіктөртбұрыш ретінде)
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

# ТИЫН КЛАСЫ (Сенің 1-ші тапсырмаң)
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(YELLOW) # Сары тиын
        self.rect = self.image.get_rect()
        # Тиын жолдың кез келген жерінен шығады
        self.rect.center = (random.randint(40, WIDTH-40), 0)

    def move(self):
        self.rect.move_ip(0, 5) # Тиын төмен қарай жылжиды
        if self.rect.top > HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH-40), 0)

# Спрайттарды топтастыру
P1 = Player()
C1 = Coin()

coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(C1)

# Ойын циклі
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)
    
    # Ұпайды көрсету (2-ші тапсырма)
    scores = font.render(f"Coins: {SCORE}", True, (0,0,0))
    screen.blit(scores, (WIDTH - 100, 10))

    # Қозғалыстар
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    # Тиынды жинауды тексеру
    if pygame.sprite.spritecollideany(P1, coins):
        SCORE += 1 # Ұпай қосу
        # Тиынды қайтадан жоғары жіберу
        C1.rect.top = 0
        C1.rect.center = (random.randint(40, WIDTH-40), 0)

    pygame.display.update()
    clock.tick(FPS)
    