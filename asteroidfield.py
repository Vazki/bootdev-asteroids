import pygame
import random
from asteroid import Asteroid
from constants import *

class AsteroidField(pygame.sprite.Sprite):
    # --- Spawn Configuration ---
    # A lookup table defining the spawn physics for the four screen boundaries.
    # Entry format: [Direction Vector, Position Calculation Lambda]
    edges = [
        [
            pygame.Vector2(1, 0),                                             # Move Right
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),   # Start Left
        ],
        [
            pygame.Vector2(-1, 0),                                            # Move Left
            lambda y: pygame.Vector2(SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT), # Start Right
        ],
        [
            pygame.Vector2(0, 1),                                             # Move Down
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),  # Start Top
        ],
        [
            pygame.Vector2(0, -1),                                            # Move Up
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS), # Start Bottom
        ],
    ]

    def __init__(self, asteroids_group):
        # Initialize as a sprite within the global 'updatable' group
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer     = 0.0
        self.asteroids_group = asteroids_group

    def spawn(self, radius, position, velocity):
        """
        Helper method to instantiate an asteroid with specific movement parameters.
        """
        asteroid          = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        """
        Main logic loop for the asteroid field: increments the spawn timer and
        generates new asteroids if the cap has not been reached.
        """
        self.spawn_timer += dt

        # Check if it is time to spawn a new asteroid
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            # Exit if the current asteroid count exceeds the defined limit
            if len(self.asteroids_group) >= ASTEROID_MAX_COUNT:
                return

            # 1. Randomly select an edge (Left, Right, Top, or Bottom)
            edge = random.choice(self.edges)
            
            # 2. Calculate base velocity and add directional variance (±30 degrees)
            speed    = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            
            # 3. Calculate the spawn coordinate along the selected boundary
            position = edge[1](random.uniform(0, 1))
            
            # 4. Select a random size tier (1 to ASTEROID_KINDS)
            kind = random.randint(1, ASTEROID_KINDS)
            
            # 5. Create the asteroid
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)