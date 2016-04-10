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
