import pygame
import random

# Inițializare Pygame
pygame.init()

# Dimensiuni ecran
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter cu upgrade-uri")

# Culori
WHITE = (255, 255, 255)

# Încărcare imagini
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")
ally_img = pygame.image.load("ally.png")  # Imaginea aliatului

# Poziții inițiale
player_x, player_y = WIDTH // 2, HEIGHT - 100
player_speed = 10

enemies = [{"x": random.randint(0, WIDTH - 50), "y": -50, "speed_x": random.choice([-2, 2]), "speed_y": 2.5}]
bullets = []
ally = None

# Scoruri
score = 0
mistakes = 0

# Font
font = pygame.font.Font(None, 36)

# Loop principal
running = True
while running:
    screen.fill(WHITE)

    # Evenimente
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mișcare jucător
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_SPACE]:
        bullets.append({"x": player_x + 20, "y": player_y})

    # Mișcare gloanțe
    for bullet in bullets:
        bullet["y"] -= 7

    # Mișcare inamici
    for enemy in enemies:
        enemy["y"] += enemy["speed_y"]
        enemy["x"] += enemy["speed_x"]

        # Schimbă direcția dacă atinge marginea
        if enemy["x"] <= 0 or enemy["x"] >= WIDTH - 50:
            enemy["speed_x"] *= -1

        # Dacă iese din ecran
        if enemy["y"] > HEIGHT:
            mistakes += 1
            enemy["y"] = -50
            enemy["x"] = random.randint(0, WIDTH - 50)

    # Verificare coliziuni gloanțe-inamici
    for bullet in bullets:
        for enemy in enemies:
            if enemy["x"] < bullet["x"] < enemy["x"] + 50 and enemy["y"] < bullet["y"] < enemy["y"] + 50:
                bullets.remove(bullet)
                enemy["y"] = -50
                enemy["x"] = random.randint(0, WIDTH - 50)
                score += 1

                # Upgrade la fiecare 5 puncte
                if score % 5 == 0:
                    if len(enemies) < score // 5:
                        enemies.append({"x": random.randint(0, WIDTH - 50), "y": -50, "speed_x": random.choice([-2, 2]), "speed_y": 2.5})
                    else:
                        for e in enemies:
                            e["speed_y"] += 2.5

    # Adăugare aliat la 50 puncte
    if score >= 50 and ally is None:
        ally = {"x": random.randint(0, WIDTH - 50), "y": -50, "speed_x": random.choice([-2, 2]), "speed_y": 2.5}

    # Mișcare aliat
    if ally:
        ally["y"] += ally["speed_y"]
        ally["x"] += ally["speed_x"]
        if ally["x"] <= 0 or ally["x"] >= WIDTH - 50:
            ally["speed_x"] *= -1

    # Afisare elemente
    screen.blit(player_img, (player_x, player_y))
    for enemy in enemies:
        screen.blit(enemy_img, (enemy["x"], enemy["y"]))
    if ally:
        screen.blit(ally_img, (ally["x"], ally["y"]))
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 0, 0), (bullet["x"], bullet["y"], 5, 10))

    # Afisare scor
    score_text = font.render(f"Score: {score}  Mistakes: {mistakes}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Final joc la 100 puncte
    if score >= 100:
        win_text = font.render("WINNER!", True, (0, 255, 0))
        screen.blit(win_text, (WIDTH // 2 - 50, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
