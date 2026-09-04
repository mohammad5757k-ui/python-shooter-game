import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter Game")
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed_x = 5
        
        self.rect.x += self.speed_x
        
        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 3)
        self.speed_x = random.randint(-2, 2)

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        
        # Wrap around screen edges
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        
        # Remove if off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -7

    def update(self):
        self.rect.y += self.speed_y
        # Remove if off screen
        if self.rect.bottom < 0:
            self.kill()


# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Game variables
score = 0
wave = 1
enemies_spawned = 0
max_enemies = 5 + (wave - 1) * 2

# Font for score
font = pygame.font.Font(None, 36)

# Main game loop
running = True
spawn_timer = 0

while running:
    clock.tick(60)  # 60 FPS
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update sprites
    all_sprites.update()

    # Spawn enemies
    spawn_timer += 1
    if spawn_timer > 30 and len(enemies) < max_enemies:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        enemies_spawned += 1
        spawn_timer = 0

    # Check for collisions
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Check if enemies reached bottom
    for enemy in enemies:
        if enemy.rect.top > SCREEN_HEIGHT:
            running = False

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    wave_text = font.render(f"Wave: {wave}", True, WHITE)
    screen.blit(wave_text, (SCREEN_WIDTH - 200, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
