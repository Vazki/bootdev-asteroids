import sys
import pygame
from constants import *
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    dt = 0
    score = 0
    lives = PLAYER_LIVES
    invincible_timer = 0.0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()
    Shot.containers = (shots, updatable, drawable)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        if invincible_timer > 0:
            invincible_timer -= dt
        for u in updatable:
            u.update(dt)
        for a in asteroids:
            for s in shots:
                if s.collides_with(a):
                    log_event("asteroid_shot")
                    if a.radius >= ASTEROID_MAX_RADIUS:
                        score += SCORE_LARGE
                    elif a.radius >= ASTEROID_MIN_RADIUS * 2:
                        score += SCORE_MEDIUM
                    else:
                        score += SCORE_SMALL
                    a.split()
                    s.kill()
        for a in asteroids:
            for a in asteroids:
                if invincible_timer <= 0 and player.collides_with(a):
                    log_event("player_hit")
                    lives -= 1
                    if lives <= 0:
                        print("Game over!")
                        sys.exit()
                    # respawn
                    player.position = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    player.velocity = pygame.Vector2(0, 0)
                    player.rotation = 0
                    invincible_timer = RESPAWN_INVINCIBLE_SECS
        screen.fill("black")
        for d in drawable:
            if d is player and invincible_timer > 0 and int(invincible_timer * INVINCIBILITY_FLICKER_RATE) % 2 == 0:
                continue
            d.draw(screen)
        score_surface = font.render(f"Score: {score}", True, "white")
        screen.blit(score_surface, (10, 10))
        lives_surface = font.render(f"Lives: {lives}", True, "white")
        screen.blit(lives_surface, (10, 40))
        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()