import pygame
from constants import *
from circleshape import CircleShape
from logger import log_event
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        # Initialize the base CircleShape with the player's specific collision radius
        super().__init__(x, y, PLAYER_RADIUS)
        # The direction the player is currently facing in degrees
        self.rotation            = 0
        # Tracks time remaining until the next projectile can be fired
        self.shot_cooldown_timer = 0.0

    # --- Shape Calculation & Rendering ---

    def triangle(self):
        """
        Computes the three vertices of the player's ship based on position and rotation.
        """
        # Directional vector pointing directly 'up' relative to the ship's rotation
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        # Perpendicular vector used to calculate the width of the ship's base
        right   = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        
        # Tip of the ship
        a = self.position + forward * self.radius
        # Bottom-left corner
        b = self.position - forward * self.radius - right
        # Bottom-right corner
        c = self.position - forward * self.radius + right
        
        return [a, b, c]
    
    

    def draw(self, screen):
        # Renders the triangular ship as a white outline
        pygame.draw.polygon(screen, "white", self.triangle(), width=LINE_WIDTH)

    # --- Transformation & Physics ---

    def rotate(self, dt):
        # Updates rotation angle based on turn speed constant and frame delta time
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        # Applies acceleration in the current forward direction
        forward        = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_ACCELERATION * dt

    def update(self, dt):
        # Apply simulated drag to the current velocity
        self.velocity *= max(0, 1 - PLAYER_DRAG * dt)
        # Update the position vector based on the resulting velocity
        self.position += self.velocity * dt

        # Process all player-specific keyboard inputs
        self._handle_input(dt)
        
        # Decrement the firing cooldown timer
        if self.shot_cooldown_timer > 0:
            self.shot_cooldown_timer -= dt

    # --- Input Handling & Logic ---

    def _handle_input(self, dt):
        """
        Encapsulates keyboard logic for movement and system actions.
        """
        keys = pygame.key.get_pressed()

        # Emergency escape and logging
        if keys[pygame.K_ESCAPE]:
             log_event("game_quit")
             print("Game quit!")
             pygame.quit()
             exit()

        # Rotation controls (Left/Right)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        # Thrust and Braking controls (Forward/Backward)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        
        # Combat controls
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        """
        Creates a new Shot entity if the cooldown timer has expired.
        """
        if self.shot_cooldown_timer > 0:
            return
            
        # Calculate velocity vector for the projectile
        forward  = pygame.Vector2(0, 1).rotate(self.rotation)
        velocity = forward * PLAYER_SHOOT_SPEED
        
        # Instantiate projectile at the ship's current position
        Shot(self.position.x, self.position.y, velocity)
        
        # Reset the cooldown timer
        self.shot_cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS