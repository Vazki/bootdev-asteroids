import pygame
from constants import *
from circleshape import CircleShape
from logger import log_event
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown_timer = 0.0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), width=LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.velocity *= max(0, 1 - PLAYER_DRAG * dt)
        self.position += self.velocity * dt

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
             log_event("game_quit")
             print("Game quit!")
             pygame.quit()
             exit()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if self.shot_cooldown_timer > 0:
            self.shot_cooldown_timer -= dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_ACCELERATION * dt

    def shoot(self):
        if self.shot_cooldown_timer > 0:
            return
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        velocity = forward * PLAYER_SHOOT_SPEED
        Shot(self.position.x, self.position.y, velocity)
        self.shot_cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS