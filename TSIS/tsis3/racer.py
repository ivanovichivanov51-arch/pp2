import pygame
import random

# Экран өлшемдері
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Бастапқы сурет (main.py-да таңдалған машинаға ауыстырылады)
        self.image = pygame.image.load("assets/mycar1.png")
        self.image = pygame.transform.scale(self.image, (50, 90))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        self.speed = 5
        self.shield = False
        self.slowed = False

    def move(self):
        """Ойыншының қозғалысы"""
        pressed_keys = pygame.key.get_pressed()
        # Майға тайғанда жылдамдық азаяды
        current_speed = self.speed // 2 if self.slowed else self.speed
        
        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-current_speed, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(current_speed, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        # 3 түрлі жау машинасының бірін кездейсоқ таңдау
        car_type = random.choice(["assets/car1.png", "assets/car2.png", "assets/car3.png"])
        self.image = pygame.image.load(car_type)
        self.image = pygame.transform.scale(self.image, (50, 90))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
        self.speed = speed

    def update(self):
        """Жаудың төмен қарай қозғалысы"""
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, coin_type):
        super().__init__()
        self.type = coin_type
        # Тиын түріне қарай суреті мен құнын белгілеу
        if self.type == "gold":
            self.image = pygame.image.load("assets/coin1.png") # Алтын тиын
            self.value = 5
        else:
            self.image = pygame.image.load("assets/coin2.png") # Күміс (сұр) тиын
            self.value = 2
            
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_WIDTH-30), 0)

    def update(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Hazard(pygame.sprite.Sprite):
    def __init__(self, hazard_type):
        super().__init__()
        self.type = hazard_type
        
        # Сурет жүктеудің орнына уақытша түсті төртбұрыш жасау
        if self.type == "oil":
            self.image = pygame.Surface((40, 40))
            self.image.fill((0, 0, 0))  # Қара түс (май)
        else:
            self.image = pygame.Surface((60, 30))
            self.image.fill((255, 0, 0)) # Қызыл түс (барьер)
            
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def update(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, p_type):
        super().__init__()
        self.type = p_type
        if self.type == "nitro":
            self.image = pygame.image.load("assets/azot.png")
        else:
            self.image = pygame.image.load("assets/shield.png")
            
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_WIDTH-30), 0)

    def update(self):
        self.rect.move_ip(0, 4)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()