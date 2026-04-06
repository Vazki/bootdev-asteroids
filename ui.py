import os
import pygame
from constants import *

_font = None


def init_ui():
    global _font
    path  = os.path.join(os.path.dirname(__file__), "assets", "fonts", "PressStart2P-Regular.ttf")
    _font = pygame.font.Font(path, 28)


def _ship_icon_points(cx, cy, radius, rotation=180):
    forward = pygame.Vector2(0, 1).rotate(rotation)
    right   = pygame.Vector2(0, 1).rotate(rotation + 90) * radius / 1.5
    pos     = pygame.Vector2(cx, cy)
    return [pos + forward * radius, pos - forward * radius - right, pos - forward * radius + right]


def draw_sprites(screen, drawable, player, invincible_timer):
    screen.fill("black")
    for d in drawable:
        if d is player and invincible_timer > 0:
            if int(invincible_timer * INVINCIBILITY_FLICKER_RATE) % 2 == 0:
                continue
        d.draw(screen)


def draw_score(screen, score):
    surf = _font.render(str(score), True, "white")
    screen.blit(surf, (16, 14))


def draw_health(screen, player_hits):
    pip_count   = 10
    pip_gap     = 4
    pip_h       = 12
    pip_w       = 36
    pips_total  = pip_count * pip_w + (pip_count - 1) * pip_gap
    pip_x0      = (SCREEN_WIDTH - pips_total) // 2
    pip_y       = 14
    health_frac = max(0.0, 1.0 - player_hits / PLAYER_MAX_HITS)
    lit         = round(pip_count * health_frac)
    for i in range(pip_count):
        px   = pip_x0 + i * (pip_w + pip_gap)
        rect = (px, pip_y, pip_w, pip_h)
        if i < lit:
            pygame.draw.rect(screen, "white", rect)
        else:
            pygame.draw.rect(screen, "white", rect, LINE_WIDTH)


def draw_lives(screen, lives):
    for i in range(PLAYER_LIVES):
        cx    = SCREEN_WIDTH - PLAYER_RADIUS - 12 - i * (PLAYER_RADIUS * 2 + 15)
        color = (80, 80, 80) if i >= lives else "white"
        pygame.draw.polygon(screen, color,
                            _ship_icon_points(cx, PLAYER_RADIUS + 12, PLAYER_RADIUS),
                            LINE_WIDTH)


def draw_hud(screen, score, lives, player_hits):
    draw_score(screen, score)
    draw_health(screen, player_hits)
    draw_lives(screen, lives)
