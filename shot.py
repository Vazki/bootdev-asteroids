import pygame
from circleshape import CircleShape
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y, velocity):
        super().__init__(x, y, SHOT_RADIUS)
        self.velocity = velocity

    def update(self, dt):
        self.position += self.velocity * dt
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius)

    def wrap_position(self, screen_width, screen_height):
        if (self.position.x < -self.radius or self.position.x > screen_width + self.radius or
                self.position.y < -self.radius or self.position.y > screen_height + self.radius):
            self.kill()