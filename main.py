import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tap Game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 100, 0)

# Загрузка картинок
try:
    bg_image = pygame.image.load('playfon.png')
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    
    shop_height = int(HEIGHT * 0.25)
    shop_bg_image = pygame.image.load('shopfon.png')
    shop_bg_image = pygame.transform.scale(shop_bg_image, (WIDTH, shop_height))
    
    main_btn_orig = pygame.image.load('btn.png')
    main_button_img = pygame.transform.scale(main_btn_orig, (350, 120))
    
    original_coin = pygame.image.load('coin.png')
    particle_coin = pygame.transform.scale(original_coin, (40, 40))
    
    icon_gray_orig = pygame.image.load('unup.png')
    buy_icon_gray = pygame.transform.scale(icon_gray_orig, (60, 60))
    
    icon_red_orig = pygame.image.load('up.png')
    buy_icon_red = pygame.transform.scale(icon_red_orig, (60, 60))
    
    fire_orig = pygame.image.load('effect.png')
    fire_particle = pygame.transform.scale(fire_orig, (50, 50))
    
except Exception as e:
    print(f"Ошибка загрузки картинок: {e}")
    bg_image = pygame.Surface((WIDTH, HEIGHT)); bg_image.fill((50, 100, 50))
    shop_bg_image = pygame.Surface((WIDTH, int(HEIGHT * 0.25))); shop_bg_image.fill((30, 30, 30))
    main_button_img = pygame.Surface((350, 120)); main_button_img.fill((255, 215, 0))
    particle_coin = pygame.Surface((40, 40)); particle_coin.fill((255, 215, 0))
    buy_icon_gray = pygame.Surface((60, 60)); buy_icon_gray.fill((100, 100, 100))
    buy_icon_red = pygame.Surface((60, 60)); buy_icon_red.fill((255, 0, 0))
    fire_particle = pygame.Surface((50, 50)); fire_particle.fill((255, 100, 0))

# Загрузка звуков
try:
    sound_click = pygame.mixer.Sound('click.wav')
    sound_buy = pygame.mixer.Sound('up.mp3')
    sound_error = pygame.mixer.Sound('error.wav')
except Exception as e:
    print(f"Ошибка загрузки звуков: {e}")
    sound_click = sound_buy = sound_error = None

# Запуск фоновой музыки (MP3)
try:
    pygame.mixer.music.load('fonmuisk.mp3')
    pygame.mixer.music.set_volume(0.4) # Громкость на 40%, чтобы не перебивала клики
    pygame.mixer.music.play(-1)        # -1 означает "играть по кругу"
except Exception as e:
    print(f"Ошибка загрузки музыки: {e}")

font_big = pygame.font.SysFont("Arial", 80, bold=True)
font_mid = pygame.font.SysFont("Arial", 50, bold=True)
font_small = pygame.font.SysFont("Arial", 40)

score = 0
score_per_click = 1
upgrade_cost = 10
level = 1

flash_timer = 0 
flash_surface = pygame.Surface((WIDTH, HEIGHT))
flash_surface.fill(ORANGE)

GAME_HEIGHT = int(HEIGHT * 0.75)
SHOP_HEIGHT = HEIGHT - GAME_HEIGHT

main_button_rect = main_button_img.get_rect(center=(WIDTH // 2, GAME_HEIGHT // 2))
buy_button_rect = pygame.Rect(WIDTH // 2 - 200, GAME_HEIGHT + 20, 400, 100)

particles = []

def spawn_particles(start_x, start_y, count=1, is_fire=False):
    for _ in range(count):
        vx = random.uniform(-8, 8) if is_fire else random.uniform(-5, 5)
        vy = random.uniform(-15, -5) if is_fire else random.uniform(-12, -6)
        life = random.randint(30, 60) if is_fire else random.randint(30, 50)
        particles.append({
            "x": start_x + random.uniform(-50, 50) if is_fire else start_x + random.uniform(-20, 20),
            "y": start_y,
            "vx": vx, "vy": vy, "life": life, "max_life": life, "is_fire": is_fire
        })

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if pos[1] < GAME_HEIGHT:
                if main_button_rect.collidepoint(pos):
                    score += score_per_click
                    spawn_particles(main_button_rect.centerx, main_button_rect.centery, count=2)
                    if sound_click: sound_click.play()
            elif buy_button_rect.collidepoint(pos):
                if score >= upgrade_cost:
                    score -= upgrade_cost
                    level += 1
                    score_per_click += 1
                    upgrade_cost = int(upgrade_cost * 1.5)
                    spawn_particles(buy_button_rect.centerx, buy_button_rect.top, count=15, is_fire=True)
                    spawn_particles(buy_button_rect.centerx, buy_button_rect.top, count=10, is_fire=False)
                    flash_timer = 5
                    if sound_buy: sound_buy.play()
                else:
                    if sound_error: sound_error.play()

    for p in particles[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vy"] += 0.5 if not p["is_fire"] else 0.2
        p["life"] -= 1
        if p["life"] <= 0:
            particles.remove(p)

    screen.blit(bg_image, (0, 0))
    screen.blit(main_button_img, main_button_rect)

    for p in particles:
        alpha = int((p["life"] / p["max_life"]) * 255)
        particle_copy = fire_particle.copy() if p["is_fire"] else particle_coin.copy()
        particle_copy.set_alpha(alpha)
        screen.blit(particle_copy, (p["x"], p["y"]))

    score_text = font_big.render(f"{score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, 60))
    outline_text = font_big.render(f"{score}", True, BLACK)
    screen.blit(outline_text, (score_rect.x - 3, score_rect.y))
    screen.blit(outline_text, (score_rect.x + 3, score_rect.y))
    screen.blit(outline_text, (score_rect.x, score_rect.y - 3))
    screen.blit(outline_text, (score_rect.x, score_rect.y + 3))
    screen.blit(score_text, score_rect)
    
    click_text = font_small.render(f"+{score_per_click} за клик", True, WHITE)
    click_rect = click_text.get_rect(center=(WIDTH // 2, 130))
    click_outline = font_small.render(f"+{score_per_click} за клик", True, BLACK)
    screen.blit(click_outline, (click_rect.x - 2, click_rect.y))
    screen.blit(click_outline, (click_rect.x + 2, click_rect.y))
    screen.blit(click_outline, (click_rect.x, click_rect.y - 2))
    screen.blit(click_outline, (click_rect.x, click_rect.y + 2))
    screen.blit(click_text, click_rect)

    screen.blit(shop_bg_image, (0, GAME_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, GAME_HEIGHT), (WIDTH, GAME_HEIGHT), 5)

    shop_title = font_mid.render("ПРОКАЧКА", True, WHITE)
    shop_title_rect = shop_title.get_rect(center=(WIDTH // 2, GAME_HEIGHT + 40))
    shop_title_outline = font_mid.render("ПРОКАЧКА", True, BLACK)
    screen.blit(shop_title_outline, (shop_title_rect.x - 2, shop_title_rect.y))
    screen.blit(shop_title_outline, (shop_title_rect.x + 2, shop_title_rect.y))
    screen.blit(shop_title_outline, (shop_title_rect.x, shop_title_rect.y - 2))
    screen.blit(shop_title_outline, (shop_title_rect.x, shop_title_rect.y + 2))
    screen.blit(shop_title, shop_title_rect)

    pygame.draw.rect(screen, BLACK, buy_button_rect)
    pygame.draw.rect(screen, WHITE, buy_button_rect, 3)

    if score >= upgrade_cost:
        current_icon = buy_icon_red
        text_color = WHITE
    else:
        current_icon = buy_icon_gray
        text_color = (150, 150, 150)

    icon_x = buy_button_rect.x + 20
    icon_y = buy_button_rect.centery - current_icon.get_height() // 2
    screen.blit(current_icon, (icon_x, icon_y))

    btn_text = font_small.render(f"Улучшить ({upgrade_cost})", True, text_color)
    text_x = buy_button_rect.x + 100
    text_y = buy_button_rect.centery - btn_text.get_height() // 2
    screen.blit(btn_text, (text_x, text_y))

    if flash_timer > 0:
        flash_surface.set_alpha(100)
        screen.blit(flash_surface, (0, 0))
        flash_timer -= 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
