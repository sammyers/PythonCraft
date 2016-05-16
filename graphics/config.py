TEXTURE_PATH = 'terrain3.png'

# Ticks per second
TICKS = 60

# Field of view in degrees
FOV = 60.0

# Render distance in meters
RENDER_DISTANCE = 250

# Vectors representing directions normal to each face of a cube.
DIRECTIONS = [(1, 0, 0),
              (-1, 0, 0),
              (0, 1, 0),
              (0, -1, 0),
              (0, 0, 1),
              (0, 0, -1)]

# Width of chunks in blocks (used to make block loading easier)
CHUNK_SIZE = 25

# Number of adjacent chunks to render around the player
CHUNK_DISTANCE = 6

# Speeds are in meters per second
WALKING_SPEED = 5.0
FLYING_SPEED = 20.0
