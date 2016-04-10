from pyglet.graphics import Batch, TextureGroup
from pyglet import image
from pyglet.gl import *
from blocks import BLOCKS
from config import TEXTURE_PATH
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
        self.position = (0, 0, 0)

        # The rotation of the player's view. 
        # First element is in the xz plane, second in some rotation of the yz plane.
        self.rotation = (0, 0)

        self._initialize()

    def _initialize(self):
        """Generate terrain to initialize the world."""
        self.add_block((1, 1, -4), 0)

        for x in range(-8, 9):
            for z in range(-8, 9):
                self.add_block((x, -2, z), 0)

    def add_block(self, position, block_id):
        """Place a block at a given set of coordinates."""
        # Place the block in the world
        self.world[position] = block_id
        # Make the block renderable
        self.show_block(position)

    def delete_block(self, position):
        """Remove a block from a given set of coordinates."""
        pass

    def show_block(self, position):
        # Find the texture coordinates for the block
        texture = BLOCKS[self.world[position]]['texture']

        vertex_data = cube_vertices(position, 1)
        texture_data = texture_map(*texture)

        self.vertices[position] = self.batch.add(24, GL_QUADS, self.group,
            ('v3f/static', vertex_data),
            ('t2f/static', texture_data))
