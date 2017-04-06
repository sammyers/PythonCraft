import pyglet
from graphics import Window, setup, convert_heightmap
from worldgen import generate_heightmap
import numpy as np

WORLD_FILE = "plates_1000.npy"

def load_world(filename):
    continents = np.round(np.load(filename))
    continents = continents.astype(int)
    world = convert_heightmap(continents, *continents.shape)
    return world

def main():
    world = load_world(WORLD_FILE)

    window = Window(world=world, width=800, height=600, caption='PythonCraft', resizable=True)
    setup()
    pyglet.app.run()

if __name__ == '__main__':
    main()
