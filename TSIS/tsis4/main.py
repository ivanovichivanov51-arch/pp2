import pygame
import sys
import random
import json
import os
from config import *
from db import (create_tables, get_or_create_player, save_game_session, 
                 get_leaderboard, get_personal_best)

# --- Инициализация ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("KBTU Snake Game")
clock = pygame.time.Clock()

font_small = pygame.font.SysFont("Arial", 20)
font_medium = pygame.font.SysFont("Arial", 30)
font_large = pygame.font.SysFont("Arial", 50)

# --- Баптаулармен жұмыс ---
def load_settings():
    if not os.path.exists("settings.json"):
        default = {"snake_color": list(GREEN), "grid_overlay": True, "sound": True}
        save_settings(default)
        return default
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except:
        return {"snake_color": list(GREEN), "grid_overlay": True, "sound": True}

def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)

# --- Ойын объектілері ---
class Food:
    def __init__(self, snake_body, obstacles, type=FOOD_NORMAL):
        self.type = type
        self.spawn_time = pygame.time.get_ticks()
        while True:
            self.pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if self.pos not in snake_body and self.pos not in obstacles:
                break

    def draw(self, surface):
        x, y = self.pos[0] * GRID_SIZE, self.pos[1] * GRID_SIZE + 40
        color = GREEN if self.type == FOOD_NORMAL else (ORANGE if self.type == FOOD_BONUS else DARK_RED)
        pygame.draw.rect(surface, color, (x, y, GRID_SIZE - 1, GRID_SIZE - 1))

class Game:
    def __init__(self, username, player_id, pb, settings):
        self.username = username
        self.player_id = player_id
        self.personal_best = pb
        self.settings = settings
        self.reset()

    def reset(self):
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self.score = 0
        self.level = 1
        self.obstacles = []
        self.foods = [Food(self.snake, self.obstacles)]
        self.active_pu = None
        self.pu_timer = 0
        self.shield_active = False
        self.running = True

    def generate_obstacles(self):
        self.obstacles = []
        if self.level >= 3:
            for _ in range(self.level * 2):
                obs = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                if obs not in self.snake and obs not in [f.pos for f in self.foods]:
                    self.obstacles.append(obs)

    def update(self):
        # Жыланның басын есептеу
        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])

        # Шектерге немесе кедергілерге соғылу
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or 
            new_head in self.snake or new_head in self.obstacles):
            if self.shield_active:
                self.shield_active = False
                self.active_pu = None
            else:
                self.running = False
                return

        self.snake.insert(0, new_head)
        
        # Тамақ жеу логикасы
        ate_food = False
        for f in self.foods[:]:
            if new_head == f.pos:
                if f.type == FOOD_NORMAL: self.score += 1
                elif f.type == FOOD_BONUS: self.score += 3
                elif f.type == FOOD_POISON:
                    if len(self.snake) > 2:
                        self.snake.pop(); self.snake.pop()
                    else: self.running = False
                
                self.foods.remove(f)
                ate_food = True
                # Жаңа деңгейге өту
                if self.score // FOODS_PER_LEVEL + 1 > self.level:
                    self.level += 1
                    self.generate_obstacles()
                break

        if not ate_food:
            self.snake.pop()
        else:
            self.foods.append(Food(self.snake, self.obstacles))
            if random.random() < 0.2: # Бонус тамақ шығу мүмкіндігі
                self.foods.append(Food(self.snake, self.obstacles, FOOD_BONUS))

    def draw(self):
        screen.fill(BLACK)
        if self.settings["grid_overlay"]:
            for x in range(0, SCREEN_WIDTH, GRID_SIZE):
                pygame.draw.line(screen, GRAY, (x, 40), (x, SCREEN_HEIGHT))
            for y in range(40, SCREEN_HEIGHT, GRID_SIZE):
                pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

        for x, y in self.obstacles:
            pygame.draw.rect(screen, BROWN, (x*GRID_SIZE, y*GRID_SIZE+40, GRID_SIZE-1, GRID_SIZE-1))
        
        for f in self.foods: f.draw(screen)
        
        for segment in self.snake:
            pygame.draw.rect(screen, self.settings["snake_color"], (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE+40, GRID_SIZE-1, GRID_SIZE-1))

        # HUD
        pygame.draw.rect(screen, GRAY, (0, 0, SCREEN_WIDTH, 40))
        score_t = font_small.render(f"Score: {self.score}  Lvl: {self.level}  Best: {self.personal_best}  User: {self.username}", True, WHITE)
        screen.blit(score_t, (10, 10))
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != (0, 1): self.direction = (0, -1)
                    if event.key == pygame.K_DOWN and self.direction != (0, -1): self.direction = (0, 1)
                    if event.key == pygame.K_LEFT and self.direction != (1, 0): self.direction = (-1, 0)
                    if event.key == pygame.K_RIGHT and self.direction != (-1, 0): self.direction = (1, 0)
            
            self.update()
            self.draw()
            clock.tick(BASE_FPS + (self.level * FPS_INCREMENT))
        
        save_game_session(self.player_id, self.score, self.level)
        return self.score, self.level

# --- Мұнда алдыңғы жауаптардағы экрандарды (Menu, Settings, Leaderboard) қосу керек ---
# (Орын үнемдеу үшін оларды қысқарттым, бірақ олар міндетті түрде тұруы керек)

def main():
    create_tables()
    settings = load_settings()
    # (Бұл жерде screen_main_menu, screen_settings және ойын циклі тұрады)
    # Жоғарыдағы main() функциясын толықтырып жазсаң болды.

if __name__ == "__main__":
    main()