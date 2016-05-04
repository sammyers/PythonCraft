import pyglet
from graphics import Window, setup, convert_heightmap
from worldgen import generate_heightmap
from worldgen import fractal_height_map

def load_world(filename):
    """Load a collection of region files to be used as a simulation world."""
    pass

def main(world_size):
    width, height = (world_size,) * 2
    world = convert_heightmap(generate_heightmap(7487670, width, height), width, height)
    window = Window(world=world, width=800, height=600, caption='PythonCraft', resizable=True)
    setup()
    pyglet.app.run()

if __name__ == '__main__':
    main(1000)
