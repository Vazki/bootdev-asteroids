import pygame
import random
from constants import *
from circleshape import CircleShape
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        # Initialize the circular collision area and position via the base class
        super().__init__(x, y, radius)

    # --- Rendering ---

    def draw(self, screen):
        # Draws the asteroid as a simple circular outline
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    # --- Physics & Movement ---

    def update(self, dt):
        # Linearly update position based on the current velocity vector and frame time
        self.position += self.velocity * dt

    # --- Life-cycle & Splitting Logic ---

    def _tier_value(self, small, medium, large):
        if self.radius >= ASTEROID_MAX_RADIUS:
            return large
        elif self.radius >= ASTEROID_MIN_RADIUS * 2:
            return medium
        return small

    @property
    def damage_value(self):
        return self._tier_value(DAMAGE_SMALL, DAMAGE_MEDIUM, DAMAGE_LARGE)

    @property
    def score_value(self):
        return self._tier_value(SCORE_SMALL, SCORE_MEDIUM, SCORE_LARGE)

    def split(self):
        """
        Handles the destruction of the asteroid. If the asteroid is large enough, 
        it spawns two smaller fragments moving in divergent directions.
        """
        # Remove the current asteroid from all sprite groups
        self.kill()

        # If the asteroid is at minimum size, it does not split further
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        # 1. Calculate the physics for the new fragments
        # Determine a random angle of divergence for the split
        random_angle = random.uniform(20, 50)
        
        # Create two new velocity vectors by rotating the current velocity
        new_vector_1 = self.velocity.rotate(random_angle)
        new_vector_2 = self.velocity.rotate(-random_angle)
        
        # The new fragments will be one tier smaller than the parent
        new_radius   = self.radius - ASTEROID_MIN_RADIUS

        # 2. Instantiate new fragments (1.2x speed of parent)
        for vec in (new_vector_1, new_vector_2):
            Asteroid(self.position.x, self.position.y, new_radius).velocity = vec * 1.2