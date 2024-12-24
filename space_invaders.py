import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game variables
player_width = 50
player_height = 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

bullet_width = 5
bullet_height = 10
bullet_speed = 7
bullets = []

enemy_width = 50
enemy_height = 50
enemy_speed = 2
enemies = []

score = 0
font = pygame.font.SysFont("Arial", 36)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Function to display the score
def display_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Function to create a new enemy
def create_enemy():
    x = random.randint(0, WIDTH - enemy_width)
    y = random.randint(-100, -40)  # Start off-screen
    return pygame.Rect(x, y, enemy_width, enemy_height)

# Function to move enemies
def move_enemies():
    global score
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemies.remove(enemy)
            score -= 1  # Missed enemy decreases score
        if enemy.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
            return True  # Game over if enemy hits the player
    return False

# Function to handle bullet movement
def move_bullets():
    global score
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)
        else:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1  # Increase score for hitting enemy
                    break

# Main game loop
def game_loop():
    global player_x, bullets, enemies, score
    running = True

    # Spawn initial enemies
    for _ in range(5):
        enemies.append(create_enemy())

    while running:
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Create a bullet
                    bullet = pygame.Rect(player_x + player_width // 2 - bullet_width // 2, player_y, bullet_width, bullet_height)
                    bullets.append(bullet)

        # Get the pressed keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Move bullets and enemies
        move_bullets()
        if move_enemies():
            running = False  # Game over if enemy hits player

        # Draw player spaceship
        pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, BLUE, bullet)

        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)

        # Display score
        display_score(score)

        # Update the screen
        pygame.display.update()

        # Set the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

# Start the game loop
if __name__ == "__main__":
    game_loop()
