import pyglet
from graphics import Window, setup, convert_heightmap
from worldgen import generate_heightmap
from worldgen import fractal_height_map
from worldgen import platec_text
import numpy as np

def main(world_size):
    width, height = (world_size,) * 2
    continents = np.round(np.load("worldgen/plates_1000.npy"))
    continents = continents.astype(int)
    world = convert_heightmap(continents, *continents.shape)
    # world = convert_heightmap(generate_heightmap(7487670, width, height), width, height)
    window = Window(world=world, width=800, height=600, caption='PythonCraft', resizable=True)
    setup()
    pyglet.app.run()

if __name__ == '__main__':
    main(1000)
