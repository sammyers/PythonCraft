import pyglet
from graphics import Window, setup
from worldgen import generate_heightmap
from factal_height_map import Terrain

def main():
    #world = generate_heightmap(7487670, 350, 350)
    world = Terrain(4)
    window = Window(world=world, width=800, height=600, caption='PythonCraft', resizable=True)
    setup()
    pyglet.app.run()

if __name__ == '__main__':
    main()
