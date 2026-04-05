import pygame

class CircleShape(pygame.sprite.Sprite):
    """
    Base class for circular game entities. Inherits from pygame.sprite.Sprite 
    to facilitate automatic group management and rendering.
    """
    def __init__(self, x, y, radius):
        # 1. Sprite Group Registration
        # Uses the 'containers' class attribute pattern common in Pygame for 
        # automatic addition to updatable/drawable groups upon instantiation.
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        # 2. Base Physics State
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius   = radius

    # --- Abstract Methods ---

    def draw(self, screen):
        """
        Placeholder for rendering logic. Subclasses (Player, Asteroid, etc.) 
        must provide their own drawing implementation.
        """
        pass

    def update(self, dt):
        """
        Placeholder for physics/logic updates. Subclasses must override 
        to define unique behavior per frame.
        """
        pass

    # --- Boundary & Collision Logic ---

    def wrap_position(self, screen_width, screen_height):
        """
        Implements toroidal screen wrapping. If an object moves entirely 
        off-screen, it is teleported to the opposite side.
        """
        # Horizontal Wrapping
        if self.position.x < -self.radius:
            self.position.x = screen_width + self.radius
        elif self.position.x > screen_width + self.radius:
            self.position.x = -self.radius

        # Vertical Wrapping
        if self.position.y < -self.radius:
            self.position.y = screen_height + self.radius
        elif self.position.y > screen_height + self.radius:
            self.position.y = -self.radius

    def collides_with(self, other):
        """
        Detects collisions using radial distance. Collision occurs if the 
        distance between the centers is less than the sum of the radii.
        """
        distance = self.position.distance_to(other.position)
        return distance < self.radius + other.radius