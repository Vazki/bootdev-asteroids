import pygame
from circleshape import CircleShape
from constants import *

class Shot(CircleShape):
    """
    Represents a projectile fired by the player. 
    Inherits base circular properties and physics from CircleShape.
    """
    def __init__(self, x, y, velocity):
        # 1. Initialization
        # Sets the initial position and the fixed SHOT_RADIUS constant
        super().__init__(x, y, SHOT_RADIUS)
        # Inherits and assigns the velocity vector provided at instantiation
        self.velocity = velocity

    # --- Physics & Movement ---

    def update(self, dt):
        """
        Updates the bullet's position linearly based on its constant velocity.
        """
        self.position += self.velocity * dt

    # --- Rendering ---

    def draw(self, screen):
        """
        Renders the projectile as a solid white circle.
        """
        pygame.draw.circle(screen, "white", self.position, self.radius)

    # --- Life-Cycle Management ---

    def wrap_position(self, screen_width, screen_height):
        """
        Overrides the default wrapping behavior. 
        Projectiles are destroyed (killed) immediately upon leaving the screen 
        boundaries to conserve memory and processing power.
        """
        # Check all four boundaries (Left, Right, Top, Bottom)
        if (self.position.x < -self.radius or 
            self.position.x > screen_width + self.radius or
            self.position.y < -self.radius or 
            self.position.y > screen_height + self.radius):
            
            # Removes the sprite from all assigned groups
            self.kill()