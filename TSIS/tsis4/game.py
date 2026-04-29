import pygame
import sys
import random
import json
from config import *
from db import create_tables, get_or_create_player, save_game_session, get_leaderboard, get_personal_best

# -------- Settings жүктеу / сақтау --------
def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except:
        return {"snake_color": [0, 200, 0], "grid_overlay": True, "sound": False}

def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)

# -------- Pygame инициализация --------
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

font_large  = pygame.font.SysFont("Arial", 40, bold=True)
font_medium = pygame.font.SysFont("Arial", 28)
font_small  = pygame.font.SysFont("Arial", 20)

# -------- Food класы --------
class Food:
    def __init__(self, food_type, occupied):
        self.type = food_type
        self.pos  = self.random_pos(occupied)
        self.spawn_time = pygame.time.get_ticks()

        if self.type == FOOD_NORMAL:
            self.color  = RED
            self.points = 1
            self.lifetime = None       # жоғалмайды
        elif self.type == FOOD_BONUS:
            self.color  = ORANGE
            self.points = 3
            self.lifetime = 5000       # 5 секунд (мс)
        elif self.type == FOOD_POISON:
            self.color  = DARK_RED
            self.points = 0
            self.lifetime = None

    def random_pos(self, occupied):
        while True:
            pos = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            if pos not in occupied:
                return pos

    def is_expired(self):
        if self.lifetime is None:
            return False
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime

    def draw(self, surface):
        x = self.pos[0] * GRID_SIZE
        y = self.pos[1] * GRID_SIZE + 40   # 40px HUD үшін
        pygame.draw.rect(surface, self.color, (x, y, GRID_SIZE, GRID_SIZE))


# -------- PowerUp класы --------
class PowerUp:
    def __init__(self, pu_type, occupied):
        self.type       = pu_type
        self.pos        = self.random_pos(occupied)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime   = 8000    # 8 секунд

        if self.type == PU_SPEED:
            self.color = YELLOW
        elif self.type == PU_SLOW:
            self.color = CYAN
        elif self.type == PU_SHIELD:
            self.color = PURPLE

    def random_pos(self, occupied):
        while True:
            pos = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            if pos not in occupied:
                return pos

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime

    def draw(self, surface):
        x = self.pos[0] * GRID_SIZE
        y = self.pos[1] * GRID_SIZE + 40
        pygame.draw.diamond = pygame.draw.polygon
        cx = x + GRID_SIZE // 2
        cy = y + GRID_SIZE // 2
        r  = GRID_SIZE // 2
        pygame.draw.polygon(surface, self.color, [
            (cx, cy - r), (cx + r, cy),
            (cx, cy + r), (cx - r, cy)
        ])
        
# -------- Snake класы --------
class Snake:
    def __init__(self, color):
        self.color     = color
        self.body      = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)   # оңға қарай
        self.grow      = False
        self.shield    = False

    def set_direction(self, new_dir):
        # Кері бағытқа жол берілмейді
        if (new_dir[0] * -1, new_dir[1] * -1) == self.direction:
            return
        self.direction = new_dir

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def shorten(self, amount=2):
        """Poison жегенде қысқарту"""
        for _ in range(amount):
            if len(self.body) > 1:
                self.body.pop()

    def get_head(self):
        return self.body[0]

    def check_wall_collision(self):
        hx, hy = self.get_head()
        return hx < 0 or hx >= GRID_WIDTH or hy < 0 or hy >= GRID_HEIGHT

    def check_self_collision(self):
        return self.get_head() in self.body[1:]

    def get_occupied(self):
        return set(self.body)

    def draw(self, surface):
        for i, segment in enumerate(self.body):
            x = segment[0] * GRID_SIZE
            y = segment[1] * GRID_SIZE + 40
            color = self.color if i != 0 else WHITE
            pygame.draw.rect(surface, color, (x, y, GRID_SIZE - 1, GRID_SIZE - 1))
            # Shield белгісі
            if i == 0 and self.shield:
                pygame.draw.rect(surface, PURPLE,
                    (x, y, GRID_SIZE - 1, GRID_SIZE - 1), 2)
                
# -------- Game класы --------
class Game:
    def __init__(self, username, player_id, personal_best, settings):
        self.username      = username
        self.player_id     = player_id
        self.personal_best = personal_best
        self.settings      = settings

        self.snake    = Snake(tuple(settings["snake_color"]))
        self.score    = 0
        self.level    = 1
        self.foods_eaten = 0
        self.fps      = BASE_FPS
        self.running  = True
        self.obstacles = []

        # Power-up жағдайы
        self.powerup         = None
        self.active_pu       = None
        self.active_pu_start = 0
        self.active_pu_dur   = 5000   # 5 секунд

        # Тамақтар
        self.foods = []
        self._spawn_food(FOOD_NORMAL)
        self._spawn_food(FOOD_BONUS)
        self._spawn_poison()

    def _get_occupied(self):
        occupied = self.snake.get_occupied()
        occupied.update(self.obstacles)
        for f in self.foods:
            occupied.add(f.pos)
        if self.powerup:
            occupied.add(self.powerup.pos)
        return occupied

    def _spawn_food(self, food_type):
        occupied = self._get_occupied()
        self.foods.append(Food(food_type, occupied))

    def _spawn_poison(self):
        occupied = self._get_occupied()
        self.foods.append(Food(FOOD_POISON, occupied))

    def _spawn_powerup(self):
        if self.powerup is None:
            pu_type = random.choice([PU_SPEED, PU_SLOW, PU_SHIELD])
            occupied = self._get_occupied()
            self.powerup = PowerUp(pu_type, occupied)

    def _spawn_obstacles(self):
        """Деңгей 3-тен бастап кедергілер"""
        self.obstacles = []
        if self.level < 3:
            return
        count = (self.level - 2) * 3   # Деңгей өскен сайын көбейеді
        head  = self.snake.get_head()
        attempts = 0
        while len(self.obstacles) < count and attempts < 1000:
            pos = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            # Жыланның басына жақын орналаспасын
            if pos not in self.snake.get_occupied() and \
               abs(pos[0] - head[0]) + abs(pos[1] - head[1]) > 4:
                self.obstacles.append(pos)
            attempts += 1

    def _next_level(self):
        self.level      += 1
        self.foods_eaten = 0
        self.fps         = BASE_FPS + (self.level - 1) * FPS_INCREMENT
        self._spawn_obstacles()
        # Тамақтарды жаңарту
        self.foods = []
        self._spawn_food(FOOD_NORMAL)
        self._spawn_food(FOOD_BONUS)
        self._spawn_poison()
        
    def update(self):
        # Power-up уақыты бітті ме?
        if self.active_pu and self.active_pu != PU_SHIELD:
            if pygame.time.get_ticks() - self.active_pu_start > self.active_pu_dur:
                self.active_pu = None
                self.fps = BASE_FPS + (self.level - 1) * FPS_INCREMENT

        # Жылан қозғалысы
        self.snake.move()
        head = self.snake.get_head()

        # Қабырға соқтығысуы
        if self.snake.check_wall_collision():
            if self.snake.shield:
                self.snake.shield = False
                self.active_pu    = None
                # Жыланды қайтару
                self.snake.body[0] = (
                    max(0, min(GRID_WIDTH - 1, head[0])),
                    max(0, min(GRID_HEIGHT - 1, head[1]))
                )
            else:
                self.running = False
                return

        # Өз-өзіне соқтығысу
        if self.snake.check_self_collision():
            if self.snake.shield:
                self.snake.shield = False
                self.active_pu    = None
            else:
                self.running = False
                return

        # Кедергіге соқтығысу
        if head in self.obstacles:
            if self.snake.shield:
                self.snake.shield = False
                self.active_pu    = None
            else:
                self.running = False
                return

        # Тамақ жеу
        for food in self.foods[:]:
            if head == food.pos:
                if food.type == FOOD_POISON:
                    self.snake.shorten(2)
                    if len(self.snake.body) <= 1:
                        self.running = False
                        return
                    self.foods.remove(food)
                    self._spawn_poison()
                else:
                    self.score       += food.points
                    self.foods_eaten += 1
                    self.snake.grow   = True
                    self.foods.remove(food)
                    self._spawn_food(food.type)

                    if self.foods_eaten >= FOODS_PER_LEVEL:
                        self._next_level()
                break

        # Power-up жеу
        if self.powerup and head == self.powerup.pos:
            self.active_pu       = self.powerup.type
            self.active_pu_start = pygame.time.get_ticks()

            if self.active_pu == PU_SPEED:
                self.fps = BASE_FPS + (self.level - 1) * FPS_INCREMENT + 6
            elif self.active_pu == PU_SLOW:
                self.fps = max(2, BASE_FPS - 4)
            elif self.active_pu == PU_SHIELD:
                self.snake.shield = True

            self.powerup = None

        # Ескірген тамақтарды жою
        for food in self.foods[:]:
            if food.is_expired():
                self.foods.remove(food)
                self._spawn_food(food.type)

        # Ескірген power-up жою
        if self.powerup and self.powerup.is_expired():
            self.powerup = None

        # Кездейсоқ power-up шығару (3% мүмкіндік)
        if self.powerup is None and random.random() < 0.03:
            self._spawn_powerup()
            
    def draw(self):
        screen.fill(BLACK)

        # ---- Тор (grid overlay) ----
        if self.settings["grid_overlay"]:
            for x in range(0, SCREEN_WIDTH, GRID_SIZE):
                pygame.draw.line(screen, GRAY, (x, 40), (x, SCREEN_HEIGHT))
            for y in range(40, SCREEN_HEIGHT, GRID_SIZE):
                pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

        # ---- Кедергілер ----
        for obs in self.obstacles:
            x = obs[0] * GRID_SIZE
            y = obs[1] * GRID_SIZE + 40
            pygame.draw.rect(screen, BROWN, (x, y, GRID_SIZE - 1, GRID_SIZE - 1))

        # ---- Тамақтар ----
        for food in self.foods:
            food.draw(screen)

        # ---- Power-up ----
        if self.powerup:
            self.powerup.draw(screen)

        # ---- Жылан ----
        self.snake.draw(screen)

        # ---- HUD (жоғарғы панель) ----
        pygame.draw.rect(screen, GRAY, (0, 0, SCREEN_WIDTH, 40))

        score_text = font_small.render(f"Score: {self.score}", True, WHITE)
        level_text = font_small.render(f"Level: {self.level}", True, WHITE)
        best_text  = font_small.render(f"Best: {self.personal_best}", True, YELLOW)
        user_text  = font_small.render(f"{self.username}", True, CYAN)

        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (150, 10))
        screen.blit(best_text,  (280, 10))
        screen.blit(user_text,  (440, 10))

        # ---- Активті power-up белгісі ----
        if self.active_pu:
            if self.active_pu == PU_SPEED:
                pu_text = font_small.render("SPEED BOOST!", True, YELLOW)
            elif self.active_pu == PU_SLOW:
                pu_text = font_small.render("SLOW MOTION!", True, CYAN)
            elif self.active_pu == PU_SHIELD:
                pu_text = font_small.render("SHIELD ON!", True, PURPLE)
            screen.blit(pu_text, (SCREEN_WIDTH // 2 - 60, 10))

        pygame.display.flip()

    def handle_keys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.set_direction((0, -1))
            elif event.key == pygame.K_DOWN:
                self.snake.set_direction((0, 1))
            elif event.key == pygame.K_LEFT:
                self.snake.set_direction((-1, 0))
            elif event.key == pygame.K_RIGHT:
                self.snake.set_direction((1, 0))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_keys(event)

            self.update()
            self.draw()
            clock.tick(self.fps)

        # Ойын бітті — нәтижені сақтау
        save_game_session(self.player_id, self.score, self.level)
        return self.score, self.level
    
    # -------- Main Menu --------
def screen_main_menu(settings):
    username = ""
    active   = True

    while active:
        screen.fill(BLACK)

        title = font_large.render("SNAKE GAME", True, GREEN)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

        # Username енгізу
        prompt = font_small.render("Enter username:", True, WHITE)
        screen.blit(prompt, (SCREEN_WIDTH // 2 - 100, 180))

        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, 210, 200, 35)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        name_surf = font_small.render(username, True, WHITE)
        screen.blit(name_surf, (input_box.x + 5, input_box.y + 7))

        # Батырмалар
        play_btn  = pygame.Rect(SCREEN_WIDTH // 2 - 80, 280, 160, 45)
        lb_btn    = pygame.Rect(SCREEN_WIDTH // 2 - 80, 340, 160, 45)
        set_btn   = pygame.Rect(SCREEN_WIDTH // 2 - 80, 400, 160, 45)
        quit_btn  = pygame.Rect(SCREEN_WIDTH // 2 - 80, 460, 160, 45)

        for btn, txt in [
            (play_btn, "PLAY"),
            (lb_btn,   "LEADERBOARD"),
            (set_btn,  "SETTINGS"),
            (quit_btn, "QUIT")
        ]:
            pygame.draw.rect(screen, GRAY, btn, border_radius=8)
            t = font_medium.render(txt, True, WHITE)
            screen.blit(t, (btn.centerx - t.get_width() // 2,
                            btn.centery - t.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    pass
                else:
                    if len(username) < 15:
                        username += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if play_btn.collidepoint(mx, my):
                    if username.strip() == "":
                        username = "Player"
                    return "play", username.strip()

                elif lb_btn.collidepoint(mx, my):
                    return "leaderboard", username.strip()

                elif set_btn.collidepoint(mx, my):
                    return "settings", username.strip()

                elif quit_btn.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()
# -------- Game Over --------
def screen_game_over(score, level, personal_best):
    while True:
        screen.fill(BLACK)

        title = font_large.render("GAME OVER", True, RED)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

        score_t = font_medium.render(f"Score: {score}", True, WHITE)
        level_t = font_medium.render(f"Level: {level}", True, WHITE)
        best_t  = font_medium.render(f"Personal Best: {personal_best}", True, YELLOW)

        screen.blit(score_t, (SCREEN_WIDTH // 2 - score_t.get_width() // 2, 180))
        screen.blit(level_t, (SCREEN_WIDTH // 2 - level_t.get_width() // 2, 220))
        screen.blit(best_t,  (SCREEN_WIDTH // 2 - best_t.get_width() // 2,  260))

        retry_btn = pygame.Rect(SCREEN_WIDTH // 2 - 80, 340, 160, 45)
        menu_btn  = pygame.Rect(SCREEN_WIDTH // 2 - 80, 400, 160, 45)

        for btn, txt in [
            (retry_btn, "RETRY"),
            (menu_btn,  "MAIN MENU")
        ]:
            pygame.draw.rect(screen, GRAY, btn, border_radius=8)
            t = font_medium.render(txt, True, WHITE)
            screen.blit(t, (btn.centerx - t.get_width() // 2,
                            btn.centery - t.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if retry_btn.collidepoint(mx, my):
                    return "retry"
                elif menu_btn.collidepoint(mx, my):
                    return "menu"


# -------- Leaderboard --------
def screen_leaderboard():
    rows = get_leaderboard()

    while True:
        screen.fill(BLACK)

        title = font_large.render("LEADERBOARD", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))

        # Баған атаулары
        headers = ["#", "Username", "Score", "Level", "Date"]
        x_pos   = [20, 60, 220, 320, 400]
        for i, h in enumerate(headers):
            t = font_small.render(h, True, CYAN)
            screen.blit(t, (x_pos[i], 90))

        pygame.draw.line(screen, GRAY, (10, 112), (SCREEN_WIDTH - 10, 112), 1)

        # Нәтижелер
        for rank, row in enumerate(rows, 1):
            username, score, level, date = row
            values = [str(rank), username, str(score), str(level), str(date)]
            color  = YELLOW if rank == 1 else WHITE
            for i, val in enumerate(values):
                t = font_small.render(val, True, color)
                screen.blit(t, (x_pos[i], 115 + rank * 28))

        back_btn = pygame.Rect(SCREEN_WIDTH // 2 - 60, 560, 120, 40)
        pygame.draw.rect(screen, GRAY, back_btn, border_radius=8)
        t = font_medium.render("BACK", True, WHITE)
        screen.blit(t, (back_btn.centerx - t.get_width() // 2,
                        back_btn.centery - t.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(pygame.mouse.get_pos()):
                    return
def screen_settings(settings):
    # Қолжетімді түстер тізімі
    colors = [
        ("Green", [0, 200, 0]), 
        ("Blue", [0, 0, 200]), 
        ("Purple", [128, 0, 128]),
        ("Yellow", [255, 255, 0])
    ]
    
    # Қазіргі таңдаулы түстің индексін табу
    color_idx = 0
    current_col = settings.get("snake_color", [0, 200, 0])
    for i, (name, col) in enumerate(colors):
        if col == current_col:
            color_idx = i
            break

    active = True
    while active:
        screen.fill(BLACK)
        
        # Тақырып
        title = font_large.render("SETTINGS", True, CYAN)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 60))

        # --- Батырмалардың аймақтарын анықтау ---
        color_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, 180, 200, 45)
        grid_btn  = pygame.Rect(SCREEN_WIDTH // 2 - 100, 250, 200, 45)
        save_btn  = pygame.Rect(SCREEN_WIDTH // 2 - 100, 400, 200, 50)

        # 1. Түс таңдау батырмасы
        pygame.draw.rect(screen, GRAY, color_btn, border_radius=8)
        color_name = colors[color_idx][0]
        color_txt = font_medium.render(f"Color: {color_name}", True, WHITE)
        screen.blit(color_txt, (color_btn.centerx - color_txt.get_width() // 2, 
                               color_btn.centery - color_txt.get_height() // 2))
        # Түстің кішкентай шаршысы (превью)
        pygame.draw.rect(screen, colors[color_idx][1], (color_btn.right + 15, color_btn.y + 10, 25, 25))

        # 2. Торды қосу/өшіру батырмасы
        pygame.draw.rect(screen, GRAY, grid_btn, border_radius=8)
        grid_status = "ON" if settings["grid_overlay"] else "OFF"
        grid_txt = font_medium.render(f"Grid: {grid_status}", True, WHITE)
        screen.blit(grid_txt, (grid_btn.centerx - grid_txt.get_width() // 2, 
                              grid_btn.centery - grid_txt.get_height() // 2))

        # 3. Сақтау және шығу
        pygame.draw.rect(screen, GREEN, save_btn, border_radius=8)
        save_txt = font_medium.render("SAVE & BACK", True, BLACK)
        screen.blit(save_txt, (save_btn.centerx - save_txt.get_width() // 2, 
                              save_btn.centery - save_txt.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                
                # Түсті ауыстыру
                if color_btn.collidepoint(mx, my):
                    color_idx = (color_idx + 1) % len(colors)
                    settings["snake_color"] = colors[color_idx][1]
                
                # Торды ауыстыру
                if grid_btn.collidepoint(mx, my):
                    settings["grid_overlay"] = not settings["grid_overlay"]
                
                # Сақтау және артқа қайту
                if save_btn.collidepoint(mx, my):
                    save_settings(settings)
                    return settings
def main():
    create_tables()
    settings = load_settings()
    
    while True:
        # 1. Бас мәзір
        action, username = screen_main_menu(settings)
        
        if action == "leaderboard":
            screen_leaderboard()
            continue
        elif action == "settings":
            settings = screen_settings(settings)
            continue
            
        # 2. Ойынды бастау
        player_id = get_or_create_player(username)
        
        running_game = True
        while running_game:
            pb = get_personal_best(player_id)
            game_instance = Game(username, player_id, pb, settings)
            score, level = game_instance.run()
            
            # 3. Game Over экраны
            choice = screen_game_over(score, level, max(score, pb))
            if choice == "menu":
                running_game = False
            # "retry" таңдалса, ішкі цикл қайталанып, ойын басынан басталады

if __name__ == "__main__":
    main()                   