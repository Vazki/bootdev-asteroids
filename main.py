import sys
import os
import pygame
from constants import *
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def _ship_icon_points(cx, cy, radius=8, rotation=180):
    forward = pygame.Vector2(0, 1).rotate(rotation)
    right   = pygame.Vector2(0, 1).rotate(rotation + 90) * radius / 1.5
    pos     = pygame.Vector2(cx, cy)
    return [pos + forward * radius, pos - forward * radius - right, pos - forward * radius + right]

def main():
    # --- Initialization ---
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock      = pygame.time.Clock()
    _font_path = os.path.join(os.path.dirname(__file__), "assets", "fonts", "PressStart2P-Regular.ttf")
    score_font = pygame.font.Font(_font_path, 28)

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
                    score += a.score_value
                    
                    a.split()
                    s.kill()

        # 4. Collision Detection: Player vs Asteroids
        for a in asteroids:
            # Check collisions only if the player is not currently invincible
            if invincible_timer <= 0 and player.collides_with(a):
                log_event("player_hit")
                a.split()
                player.apply_knockback(a.position)
                
                player_hits += a.damage_value
                
                # Determine if hit results in a death or temporary invincibility
                if player_hits >= PLAYER_MAX_HITS:
                    lives -= 1
                    player_hits = 0
                    
                    if lives <= 0:
                        print("Game over!")
                        sys.exit()
                    
                    player.respawn(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
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

        ui_top = 14

        # Score — top-left
        score_surf = score_font.render(str(score), True, "white")
        screen.blit(score_surf, (16, ui_top))

        # Health pips — 10 segments, top-center
        pip_count   = 10
        pip_gap     = 4
        pip_h       = 12
        pip_w       = 36
        pips_total  = pip_count * pip_w + (pip_count - 1) * pip_gap
        pip_x0      = (SCREEN_WIDTH - pips_total) // 2
        pip_y       = ui_top
        health_frac = max(0.0, 1.0 - player_hits / PLAYER_MAX_HITS)
        lit         = round(pip_count * health_frac)
        for i in range(pip_count):
            px   = pip_x0 + i * (pip_w + pip_gap)
            rect = (px, pip_y, pip_w, pip_h)
            if i < lit:
                pygame.draw.rect(screen, "white", rect)
            else:
                pygame.draw.rect(screen, "white", rect, LINE_WIDTH)

        # Lives — ship icons, top-right
        for i in range(PLAYER_LIVES):
            cx    = SCREEN_WIDTH - PLAYER_RADIUS - 12 - i * (PLAYER_RADIUS * 2 + 15)
            color = (80, 80, 80) if i >= lives else "white"
            pygame.draw.polygon(screen, color,
                                _ship_icon_points(cx, PLAYER_RADIUS + 12, PLAYER_RADIUS),
                                LINE_WIDTH)

        pygame.display.flip()

        # 6. Frame Timing
        # Set delta time for the next frame (60 FPS target)
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()