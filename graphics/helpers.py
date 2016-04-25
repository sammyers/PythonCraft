from pyglet.gl import *

def cube_vertices(position, width):
    """ 
    Return the vertices of the cube at position (x, y, z) with a given size.
    """
    x, y, z = position
    n = width / 2.0 #distance of faces from the cube's center

    return [
        #lower left  #lower right #upper right #upper left
        x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  #top
        x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  #bottom
        x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  #left
        x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  #right
        x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  #front
        x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n   #back
    ]

def block_position(position):
    """
    Take an x, y, z location of arbitrary position 
    and return the block containing that position.
    """
    x, y, z = position
    return (int(x + 0.5), int(y + 0.5), int(z + 0.5))

def get_chunk(position, chunk_size):
    """
    Return the location of the chunk containing a given block.
    """
    position = block_position(position)
    x, z = position[::2]
    x = (x + (chunk_size - 1) / 2) // chunk_size
    z = (z + (chunk_size - 1) / 2) // chunk_size
    return (int(x), int(z))


def texture_coords(position, width=16):
    """
    Return the OpenGL texture coordinates for a given texture square.
    
    Parameters:
        position (tuple):
            The x, y position in the texture grid of the desired texture (indexed from 0).
        width (int):
            The number of texture squares per row/column in the texture file.

        Returns:
            A list of UV texture vertices, mapped to the domain [0, 1].
    """
    u, v = position
    width = float(width)
    map_width = 1 / width
    left_u, lower_v = u / width, v / width
    right_u, upper_v = left_u + map_width, lower_v + map_width
    return [left_u, lower_v,   #lower left
            right_u, lower_v,  #lower right
            right_u, upper_v,  #upper right
            left_u, upper_v]   #upper left

def texture_map(top, bottom, sides):
    """
    Return a list of texture vertices for a cube.
    
    Parameters:
        top, bottom, sides (tuples): 
            Coordinates within the texture file of each face of the cube.
            Values are in the discrete domain [0, n], 
            where n is the number of textures in each row/column of the texture file.

    """
    top_vertices = texture_coords(top)
    bottom_vertices = texture_coords(bottom)
    side_vertices = texture_coords(sides) * 4
    return top_vertices + bottom_vertices + side_vertices

def setup():
    """
    Basic OpenGL setup function.
    """
    # Set the color of the sky (the window is cleared to this color every frame)
    glClearColor(0.5, 0.69, 1.0, 1)
    # Render only front-facing sides of cubes to reduce performance overhead
    glEnable(GL_CULL_FACE)
    # Make pixelated textures not look awful
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

def convert_heightmap(heightmap, width, height):
    """
    Take a 2D array of height values and return a world dictionary that the program can use.
    """
    height_dict = {}

    for z, row in enumerate(heightmap):
        for x, h in enumerate(row):
            for y in range(h + 1):
                height_dict[(x - width / 2, y, z - width / 2)] = 6 if h == 0 else (1 if y == h else (3 if y <= h - 3 else 2))

    return height_dict
