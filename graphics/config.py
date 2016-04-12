TEXTURE_PATH = 'terrain.png'

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
CHUNK_SIZE = 16

# Speeds are in meters per second
WALKING_SPEED = 5.0
FLYING_SPEED = 4.0
