SCREEN_WIDTH                  = 1280                                  # Horizontal resolution of the game window
SCREEN_HEIGHT                 = 720                                   # Vertical resolution of the game window
PLAYER_RADIUS                 = 20                                    # Collision radius of the player ship in pixels
LINE_WIDTH                    = 2                                     # Thickness of lines used for drawing shapes
PLAYER_TURN_SPEED             = 300                                   # Rotation speed of the player in degrees per second
PLAYER_SPEED                  = 200                                   # Forward movement speed of the player
ASTEROID_MIN_RADIUS           = 20                                    # Radius of the smallest possible asteroid
ASTEROID_KINDS                = 3                                     # Number of different asteroid size tiers
ASTEROID_SPAWN_RATE_SECONDS   = 0.8                                   # Interval between new asteroid spawns
ASTEROID_MAX_RADIUS           = ASTEROID_MIN_RADIUS * ASTEROID_KINDS  # Radius of the largest possible asteroid
SHOT_RADIUS                   = 5                                     # Collision radius of player projectiles
PLAYER_SHOOT_SPEED            = 500                                   # Velocity of player projectiles
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3                                   # Minimum time delay between consecutive shots
SCORE_LARGE                   = 20                                    # Points awarded for destroying a large asteroid
SCORE_MEDIUM                  = 50                                    # Points awarded for destroying a medium asteroid
SCORE_SMALL                   = 100                                   # Points awarded for destroying a small asteroid
PLAYER_LIVES                  = 3                                     # Starting number of lives for the player
PLAYER_MAX_HITS               = 10                                    # Health points before losing a life
DAMAGE_SMALL                  = 2                                     # Damage dealt by a small asteroid
DAMAGE_MEDIUM                 = 4                                     # Damage dealt by a medium asteroid
DAMAGE_LARGE                  = 6                                     # Damage dealt by a large asteroid
PLAYER_ACCELERATION           = 500                                   # Thrust acceleration in pixels/sec²
PLAYER_DRAG                   = 1.5                                   # Drag coefficient; higher = stops faster
PLAYER_KNOCKBACK_SPEED        = 300                                   # Speed applied to player on asteroid hit
RESPAWN_INVINCIBLE_SECS       = 2.0                                   # Duration of invulnerability after losing a life
HIT_INVINCIBLE_SECS           = 1.0                                   # Duration of invulnerability after a regular hit
INVINCIBILITY_FLICKER_RATE    = 10                                    # Toggles per second (10 = 0.1s on, 0.1s off)
ASTEROID_MAX_COUNT            = 15                                    # Max asteroids AsteroidField will spawn; splits are unaffected