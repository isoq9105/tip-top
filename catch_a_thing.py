import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Catch the Falling Objects")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Clock
clock = pygame.time.Clock()
basket_width = 60
basket_height = 20
falling_object_size = 20

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Basket class
class Basket:
    def __init__(self):
        self.x = width // 2 - basket_width // 2
        self.y = height - basket_height - 10
        self.speed = 15

    def move(self, dx):
        if self.x + dx >= 0 and self.x + dx <= width - basket_width:
            self.x += dx

    def draw(self):
        pygame.draw.rect(screen, green, [self.x, self.y, basket_width, basket_height])

# Falling object class
class FallingObject:
    def __init__(self):
        self.x = random.randrange(0, width - falling_object_size)
        self.y = -falling_object_size
        self.speed = random.randint(5, 10)

    def fall(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.circle(screen, red, (self.x + falling_object_size // 2, self.y + falling_object_size // 2), falling_object_size // 2)

# Display score
def show_score(score):
    value = score_font.render("Score: " + str(score), True, black)
    screen.blit(value, [10, 10])

# Main game loop
def gameLoop():
    game_over = False
    score = 0

    # Create the basket
    basket = Basket()

    # List of falling objects
    falling_objects = []

    while not game_over:
        screen.fill(blue)
        show_score(score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Handle basket movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            basket.move(-basket.speed)
        if keys[pygame.K_RIGHT]:
            basket.move(basket.speed)

        # Create new falling objects at random intervals
        if random.random() < 0.05:
            falling_objects.append(FallingObject())

        # Move and draw falling objects
        for obj in falling_objects[:]:
            obj.fall()
            obj.draw()

            # Check for collision with basket
            if obj.y + falling_object_size >= basket.y and basket.x < obj.x < basket.x + basket_width:
                score += 1
                falling_objects.remove(obj)  # Remove object after catching it
            # If the object falls below the screen, reduce score and remove
            elif obj.y > height:
                score -= 1
                falling_objects.remove(obj)

        # Draw basket
        basket.draw()

        pygame.display.update()
        clock.tick(30)  # Set the frame rate to 30 FPS

    # End of game, display message
    game_over_message("Game Over! Press Q to Quit or R to Restart", red)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:
                    gameLoop()

def game_over_message(msg, color):
    message = font_style.render(msg, True, color)
    screen.blit(message, [width / 6, height / 3])

# Run the game
gameLoop()
