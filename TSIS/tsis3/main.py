import pygame, sys, random
from racer import Player, Enemy, Coin, PowerUp, Hazard, SCREEN_WIDTH, SCREEN_HEIGHT
from ui import Button, draw_text
from persistence import save_score, get_leaderboard

# Инициализация
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Arcade: Pro Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

# Жолдың суреті (фон)
background = pygame.image.load("assets/AnimatedStreet.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

def show_leaderboard():
    """Лидерборд беті"""
    while True:
        screen.fill((20, 20, 20))
        draw_text(screen, "TOP 10 SCORES", 35, 0, 50, (255, 215, 0), center=True)
        
        scores = get_leaderboard()
        for i, entry in enumerate(scores):
            txt = f"{i+1}. {entry['name']} - {entry['score']}"
            draw_text(screen, txt, 20, 100, 120 + (i * 30), (255, 255, 255))

        btn_back = Button(100, 500, 200, 45, "BACK", (100, 100, 100))
        btn_back.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.is_clicked(event.pos): return

        pygame.display.update()

def main_game(user_name, selected_car):
    """Негізгі ойын циклі"""
    player = Player()
    # Таңдалған машина суретін қою
    player.image = pygame.image.load(selected_car)
    player.image = pygame.transform.scale(player.image, (50, 90))
    
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    hazards = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)

    score = 0
    distance = 0
    bg_y = 0
    nitro_timer = 0
    oil_timer = 0
    running = True

    while running:
        # Фонның қозғалысы
        bg_speed = 5 if nitro_timer == 0 else 15
        bg_y += bg_speed
        if bg_y >= SCREEN_HEIGHT: bg_y = 0

        distance += 0.2
        enemy_speed = 5 + int(distance // 250)

        # Спавн логикасы
        if len(enemies) < 3 and random.randint(1, 60) == 1:
            e = Enemy(enemy_speed)
            enemies.add(e); all_sprites.add(e)
        if random.randint(1, 120) == 1:
            c = Coin(random.choice(["gold", "silver"]))
            coins.add(c); all_sprites.add(c)
        if random.randint(1, 250) == 1:
            h = Hazard(random.choice(["oil", "barrier"]))
            hazards.add(h); all_sprites.add(h)
        if random.randint(1, 450) == 1:
            p = PowerUp(random.choice(["nitro", "shield"]))
            powerups.add(p); all_sprites.add(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        # Жаңарту
        player.move()
        enemies.update()
        coins.update()
        hazards.update()
        powerups.update()

        # Соқтығысулар
        for c in pygame.sprite.spritecollide(player, coins, True):
            score += c.value

        for h in pygame.sprite.spritecollide(player, hazards, True):
            if h.type == "oil":
                player.slowed = True
                oil_timer = 100
            elif h.type == "barrier" and not player.shield:
                running = False

        if oil_timer > 0: oil_timer -= 1
        else: player.slowed = False

        for p in pygame.sprite.spritecollide(player, powerups, True):
            if p.type == "nitro": nitro_timer = 150
            elif p.type == "shield": player.shield = True

        if nitro_timer > 0:
            nitro_timer -= 1
            player.speed = 12
        else:
            player.speed = 5

        if pygame.sprite.spritecollide(player, enemies, False):
            if player.shield:
                player.shield = False
                for e in pygame.sprite.spritecollide(player, enemies, True): e.kill()
            else:
                running = False

        # Экранға шығару
        screen.blit(background, (0, bg_y))
        screen.blit(background, (0, bg_y - SCREEN_HEIGHT))
        
        all_sprites.draw(screen)
        draw_text(screen, f"Score: {score}", 20, 10, 10, (255, 255, 255))
        
        if player.shield: draw_text(screen, "🛡️ SHIELD", 18, 280, 10, (0, 255, 255))
        if nitro_timer > 0: draw_text(screen, "🔥 NITRO", 18, 280, 35, (255, 215, 0))

        pygame.display.update()
        clock.tick(60)

    save_score(user_name, score, int(distance)) # 3 аргумент: аты, тиындар, қашықтық
    return game_over_screen(user_name, score + int(distance), selected_car)

def game_over_screen(name, final_score, car):
    while True:
        screen.fill((0, 0, 0))
        draw_text(screen, "GAME OVER", 50, 0, 150, (255, 0, 0), center=True)
        draw_text(screen, f"FINAL SCORE: {final_score}", 25, 0, 220, (255, 255, 255), center=True)
        
        btn_retry = Button(100, 320, 200, 50, "RETRY", (0, 150, 0))
        btn_menu = Button(100, 390, 200, 50, "MENU", (150, 0, 0))
        
        btn_retry.draw(screen, font); btn_menu.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retry.is_clicked(event.pos): return "RETRY"
                if btn_menu.is_clicked(event.pos): return "MENU"
        pygame.display.update()

def main_menu():
    selected_car = "assets/mycar1.png" # Бастапқы машина
    while True:
        screen.fill((30, 30, 30))
        draw_text(screen, "RACER PRO", 50, 0, 80, (0, 255, 127), center=True)
        
        # Машинаны таңдау визуализациясы
        draw_text(screen, "Selected Car:", 20, 130, 160)
        car_img = pygame.image.load(selected_car)
        car_img = pygame.transform.scale(car_img, (40, 70))
        screen.blit(car_img, (180, 190))

        btn_start = Button(100, 280, 200, 50, "START GAME", (0, 200, 0))
        btn_change_car = Button(100, 350, 200, 50, "CHANGE CAR", (0, 100, 200))
        btn_scores = Button(100, 420, 200, 50, "LEADERBOARD", (150, 150, 0))
        btn_quit = Button(100, 490, 200, 50, "QUIT", (100, 0, 0))

        for b in [btn_start, btn_change_car, btn_scores, btn_quit]: b.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_start.is_clicked(event.pos):
                    res = main_game("Player1", selected_car)
                    while res == "RETRY": res = main_game("Player1", selected_car)
                if btn_change_car.is_clicked(event.pos):
                    # Машинаны ауыстыру (mycar1 мен mycar2 арасында)
                    selected_car = "assets/mycar2.png" if selected_car == "assets/mycar1.png" else "assets/mycar1.png"
                if btn_scores.is_clicked(event.pos):
                    show_leaderboard()
                if btn_quit.is_clicked(event.pos):
                    pygame.quit(); sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()