# game options/settings
TITLE = "Jumpy!"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'comicsansms'
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"
SLEEP = .5

# Player Properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

# Sprite Layering
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POWERUP_LAYER = 1
MOB_LAYER = 2

# Game Properties
BOOST_POWER = 60
POW_SPAWN_PCT = 9
MOB_FREQ = 5000

# Starting Platforms
PLATFORM_LIST = [(0, HEIGHT-60),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4),
                 (125, HEIGHT-350),
                 (350, 200),
                 (175, 100)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (0, 155, 155)
LIGHTER_BLUE = (174, 234, 255)
SLIGHTER_BLUE = (50, 255, 255)
BGCOLOR = SLIGHTER_BLUE
