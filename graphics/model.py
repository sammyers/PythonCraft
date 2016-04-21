from pyglet.graphics import Batch, TextureGroup
from pyglet import image
from pyglet.gl import *
from blocks import BLOCKS
from config import *
from helpers import cube_vertices, texture_map, get_chunk
import math

class Model(object):
    """
    Stores world and player data, with methods to modify blocks.
    """
    def __init__(self, world=None):
        # Batch of pyglet VertexLists; everything loaded into the batch is drawn
        self.batch = Batch()

        # TextureGroup for managing OpenGL textures.
        self.group = TextureGroup(image.load(TEXTURE_PATH).get_texture())

        # All of the blocks in the world; key is a tuple of (x, y, z) position
        if world is None:
            self.world = {}
        else:
            self.world = world

        # Just the blocks that are visible, i.e. exposed on at least one side
        self.visible = {}

        # Mapping from position to a pyglet VertexList (only for visible blocks)
        self.vertices = {}

        # Mapping from chunks to block locations within those chunks.
        self.chunks = {}

        # The player's position in the world, initially at the origin.
        self.position = (0, 2, 0)

        # The chunk in which the player is currently located.
        self.chunk = get_chunk(self.position, CHUNK_SIZE)

        #
        self.nearby = self.get_nearby_chunks(self.chunk)

        # The rotation of the player's view. 
        # First element is in the xz plane, second in some rotation of the yz plane.
        # Up-down rotation is constrained to between -90 and 90 (straight up and down)
        self.rotation = (0, 0)

        # Initialize player motion in the xz plane.
        # For the first element, -1 and 1 are left and right.
        # For the second, -1 and 1 are down and up.
        # For the third, backwards and forwards.
        self.motion = [0, 0, 0]

        # Place blocks in the world
        self._initialize()

    def _initialize(self):
        """
        Generate terrain to initialize the world.
        """
        for location in self.world:
            self.add_block(location, self.world[location])

    def get_nearby_chunks(self, location):
        x, z = location
        x_range = range(-CHUNK_DISTANCE, CHUNK_DISTANCE + 1)
        z_range = range(-CHUNK_DISTANCE, CHUNK_DISTANCE + 1)
        chunks = set()
        for dx in x_range:
            for dz in z_range:
                if math.sqrt(dx ** 2 + dz ** 2) > CHUNK_DISTANCE:
                    continue
                chunks.add((x + dx, z + dz))
        return chunks

    def update_chunk_location(self, before, after):
        """
        Ensure that the proper adjacent chunks are visible.
        """
        current = self.get_nearby_chunks(before)
        updated = self.get_nearby_chunks(after)

        shown = updated - current
        hidden = current - updated
        for chunk in shown:
            self.show_chunk(chunk)
        for chunk in hidden:
            self.hide_chunk(chunk)
        self.chunk = after

    def show_chunk(self, chunk_location):
        """
        Show all blocks contained within a given chunk.
        """
        for position in self.chunks.get(chunk_location, []):
            if position not in self.visible and self.check_exposed(position):
                self.show_block(position)

    def hide_chunk(self, chunk_location):
        """
        Hide all blocks contained within a given chunk.
        """
        for position in self.chunks.get(chunk_location, []):
            if position in self.visible:
                self.hide_block(position)

    def add_block(self, position, block_id):
        """
        Place a block at a given set of coordinates.
        """
        # Place the block in the world
        self.world[position] = block_id
        # Register the block in the proper chunk
        self.chunks.setdefault(get_chunk(position, CHUNK_SIZE), []).append(position)
        # Make the block renderable
        if get_chunk(position, CHUNK_SIZE) in self.nearby and self.check_exposed(position):
            self.show_block(position)

    def delete_block(self, position):
        """
        Remove a block from a given set of coordinates.
        """
        pass

    def show_block(self, position):
        """
        Add a block to the batch to be rendered by OpenGL.
        The block will continue being rendered until it's hidden or deleted.
        """
        # Add to record of visible blocks
        self.visible[position] = self.world[position]
        # Find the texture coordinates for the block
        texture_location = BLOCKS[self.world[position]]['texture']

        # Convert cube coordinates and texture position to OpenGl vertices
        vertex_data = cube_vertices(position, 1)
        texture_data = texture_map(*texture_location)

        # Add the cube to the batch, mapping texture vertices to cube vertices.
        self.vertices[position] = self.batch.add(24, GL_QUADS, self.group,
            ('v3f/static', vertex_data),
            ('t2f/static', texture_data))

    def hide_block(self, position):
        """
        Stop a block from being rendered.
        """
        del self.visible[position]
        # Remove from the batch by deleting the vertex list
        self.vertices.pop(position).delete()

    def check_exposed(self, position):
        """
        Return true if any of the faces of a block are exposed, otherwise false.
        """
        x, y, z = position
        for dx, dy, dz in DIRECTIONS:
            if (x + dx, y + dy, z + dz) not in self.world:
                return True
        return False
