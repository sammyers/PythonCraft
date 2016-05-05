from pyglet.graphics import Batch, TextureGroup
from pyglet import image
from pyglet.gl import *
import math, time
from collections import deque
from .blocks import BLOCKS
from .config import *
from .helpers import cube_vertices, texture_map, get_chunk

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

        # The chunk in which the player is currently located.
        self.chunk = None

        # The player's position in the world, initially at the origin.
        self.position = (0, 2, 0)

        # The rotation of the player's view. 
        # First element is in the xz plane, second in some rotation of the yz plane.
        # Up-down rotation is constrained to between -90 and 90 (straight up and down)
        self.rotation = (0, 0)

        # Initialize player motion in the xz plane.
        # For the first element, -1 and 1 are left and right.
        # For the second, -1 and 1 are down and up.
        # For the third, backwards and forwards.
        self.motion = [0, 0, 0]

        # A queue for function calls; this allows blocks to be added and removed
        # in a way that doesn't slow down the game loop
        self.queue = deque()

        # Place blocks in the world
        self._initialize()

    def _initialize(self):
        """
        Generate terrain to initialize the world.
        """
        for location in self.world:
            self.add_block(location, self.world[location])

    def initial_render(self):
        """
        Make all blocks visually current by emptying the queue without breaks.
        This method is called once, when the world is first loaded.
        """
        while self.queue:
            self.dequeue()

    def get_nearby_chunks(self, location):
        """
        Return a set containing the chunk locations within range of a given chunk.
        """
        x, z = location
        x_range = range(-CHUNK_DISTANCE, CHUNK_DISTANCE + 1)
        z_range = range(-CHUNK_DISTANCE, CHUNK_DISTANCE + 1)
        chunks = set()
        for dx in x_range:
            for dz in z_range:
                # Only include chunks within a certain Euclidean distance
                if math.sqrt(dx ** 2 + dz ** 2) > CHUNK_DISTANCE:
                    continue
                chunks.add((x + dx, z + dz))
        return chunks

    def update_chunk_location(self, before, after):
        """
        Ensure that the proper adjacent chunks are visible.
        """
        # Show all chunks in range when none are currently loaded.
        # This happens once when the program starts.
        if before is None:
            chunks = self.get_nearby_chunks(after)
            for chunk in chunks:
                self.show_chunk(chunk)
            return

        current = self.get_nearby_chunks(before)
        updated = self.get_nearby_chunks(after)

        shown = updated - current
        hidden = current - updated

        for chunk in shown:
            self.show_chunk(chunk)
        for chunk in hidden:
            self.hide_chunk(chunk)

    def show_chunk(self, chunk_location):
        """
        Show all blocks contained within a given chunk.
        """
        for position in self.chunks.get(chunk_location, []):
            if position not in self.visible and self.check_exposed(position):
                self.enqueue(self.show_block, position)

    def hide_chunk(self, chunk_location):
        """
        Hide all blocks contained within a given chunk.
        """
        for position in self.chunks.get(chunk_location, []):
            if position in self.visible:
                self.visible.pop(position)
                self.enqueue(self.hide_block, position)

    def add_block(self, position, block_id):
        """
        Place a block at a given set of coordinates.
        """
        # Place the block in the world
        self.world[position] = block_id
        # Register the block in the proper chunk
        self.chunks.setdefault(get_chunk(position, CHUNK_SIZE), []).append(position)

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

    def enqueue(self, func, *args):
        """
        Add a function to the queue to be called in the program's update loop.
        """
        self.queue.append((func, args))

    def dequeue(self):
        """
        Call the function at the top of the queue.
        """
        func, args = self.queue.popleft()
        func(*args)

    def process_queue(self):
        """
        Call as many functions in the queue as possible within one tick of the game loop.
        This allows chunks to be loaded and unloaded without slowing down the program.
        """
        start_time = time.clock()
        while self.queue and time.clock() - start_time < 1.0 / TICKS:
            self.dequeue()
