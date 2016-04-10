from pyglet.graphics import Batch, TextureGroup
from pyglet import image
from pyglet.gl import *
from blocks import BLOCKS
from config import *
from helpers import cube_vertices, texture_map

class Model(object):

    def __init__(self):

        # Batch of pyglet VertexLists; everything loaded into the batch is drawn
        self.batch = Batch()

        # TextureGroup for managing OpenGL textures.
        self.group = TextureGroup(image.load(TEXTURE_PATH).get_texture())

        # All of the blocks in the world; key is a tuple of (x, y, z) position
        self.world = {}

        # Just the blocks that are visible, i.e. exposed on at least one side
        self.visible = {}

        # Mapping from position to a pyglet VertexList (only for visible blocks)
        self.vertices = {}

        # The player's position in the world, initially at the origin.
        self.position = (0, 2, 0)

        # The rotation of the player's view. 
        # First element is in the xz plane, second in some rotation of the yz plane.
        # Up-down rotation is constrained to between -90 and 90 (straight up and down)
        self.rotation = (0, 0)

        # Initialize player motion in the xz plane.
        # For the first element, -1 and 1 are backward and forward.
        # For the second, -1 and 1 are left and right.
        # For the third, down and up.
        self.motion = [0, 0, 0]

        # Place blocks in the world
        self._initialize()

    def _initialize(self):
        """Generate terrain to initialize the world."""
        self.add_block((1, 1, -4), 0)

        for x in range(-8, 9):
            for z in range(-8, 9):
                self.add_block((x, 0, z), 0)

    def add_block(self, position, block_id):
        """Place a block at a given set of coordinates."""
        # Place the block in the world
        self.world[position] = block_id
        # Make the block renderable
        if self.check_exposed(position):
            self.show_block(position)

    def delete_block(self, position):
        """Remove a block from a given set of coordinates."""
        pass

    def show_block(self, position):
        self.visible[position] = self.world[position]
        # Find the texture coordinates for the block
        texture = BLOCKS[self.world[position]]['texture']

        vertex_data = cube_vertices(position, 1)
        texture_data = texture_map(*texture)

        self.vertices[position] = self.batch.add(24, GL_QUADS, self.group,
            ('v3f/static', vertex_data),
            ('t2f/static', texture_data))

    def hide_block(self, position):
        pass

    def check_exposed(self, position):
        """
        Return true if any of the faces of a block are exposed, otherwise false.
        """
        x, y, z = position
        for dx, dy, dz in DIRECTIONS:
            if (x + dx, y + dy, z + dz) not in self.world:
                return True
        return False
