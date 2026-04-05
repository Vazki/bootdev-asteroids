import sys
import pygame
from constants import *
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    # --- Initialization ---
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock  = pygame.time.Clock()
    font   = pygame.font.Font(None, 36)

    # --- Game State Variables ---
    dt               = 0
    score            = 0
    lives            = PLAYER_LIVES
    player_hits      = 0
    invincible_timer = 0.0

    # --- Sprite Groups ---
    updatable = pygame.sprite.Group()
    drawable  = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots     = pygame.sprite.Group()

    # --- Object Containers Setup ---
    # Assigning containers to classes allows automatic group management upon instantiation
    Player.containers        = (updatable, drawable)
    Asteroid.containers      = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers          = (shots, updatable, drawable)

    # --- Entity Instantiation ---
    player         = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    asteroid_field = AsteroidField(asteroids)

    # --- Main Game Loop ---
    while True:
        log_state()
        
        # 1. Input Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # 2. Movement and Logic Updates
        if invincible_timer > 0:
            invincible_timer -= dt

        for u in updatable:
            u.update(dt)
            # Ensure entities wrap around the screen edges
            if hasattr(u, 'wrap_position'):
                u.wrap_position(SCREEN_WIDTH, SCREEN_HEIGHT)

        # 3. Collision Detection: Projectiles vs Asteroids
        for a in asteroids:
            for s in shots:
                if s.collides_with(a):
                    log_event("asteroid_shot")
                    
                    # Points awarded based on the radius of the hit asteroid
                    if a.radius >= ASTEROID_MAX_RADIUS:
                        score += SCORE_LARGE
                    elif a.radius >= ASTEROID_MIN_RADIUS * 2:
                        score += SCORE_MEDIUM
                    else:
                        score += SCORE_SMALL
                    
                    a.split()
                    s.kill()

        # 4. Collision Detection: Player vs Asteroids
        for a in asteroids:
            # Check collisions only if the player is not currently invincible
            if invincible_timer <= 0 and player.collides_with(a):
                log_event("player_hit")
                a.split()
                
                # Calculate knockback vector based on relative positions
                away = player.position - a.position
                if away.length() > 0:
                    player.velocity = away.normalize() * PLAYER_KNOCKBACK_SPEED
                
                player_hits += 1
                
                # Determine if hit results in a death or temporary invincibility
                if player_hits >= PLAYER_MAX_HITS:
                    lives -= 1
                    player_hits = 0
                    
                    if lives <= 0:
                        print("Game over!")
                        sys.exit()
                    
                    # Reset player position and movement on respawn
                    player.position  = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    player.velocity  = pygame.Vector2(0, 0)
                    player.rotation  = 0
                    invincible_timer = RESPAWN_INVINCIBLE_SECS
                else:
                    invincible_timer = HIT_INVINCIBLE_SECS

        # 5. Drawing and Rendering
        screen.fill("black")

        # Render all drawable sprites
        for d in drawable:
            # Implement flicker effect by skipping draw calls based on timer frequency
            if d is player and invincible_timer > 0:
                if int(invincible_timer * INVINCIBILITY_FLICKER_RATE) % 2 == 0:
                    continue
            d.draw(screen)

        # Render UI text (Score and Lives)
        score_surface = font.render(f"Score: {score}", True, "white")
        screen.blit(score_surface, (10, 10))
        
        lives_surface = font.render(f"Lives: {lives}", True, "white")
        screen.blit(lives_surface, (10, 40))

        # Render health pips/circles representing current player_hits
        for i in range(PLAYER_MAX_HITS):
            cx    = 14 + i * 18
            cy    = 82
            color = (80, 80, 80) if i < player_hits else "white"
            pygame.draw.circle(screen, color, (cx, cy), 6, LINE_WIDTH)

        pygame.display.flip()

        # 6. Frame Timing
        # Set delta time for the next frame (60 FPS target)
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()