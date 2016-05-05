import pyglet
from graphics import Window, setup, convert_heightmap
from worldgen import generate_heightmap
from worldgen import fractal_height_map
from worldgen import platec_text

def main(world_size):
    #width, height = (1025,) * 2 #(world_size,) * 2

    #world = convert_heightmap(generate_heightmap(7487670, width, height), width, height)

    #world = convert_heightmap(platec_text.Terrain(10), width, height)

    world = fractal_height_map.Terrain(7)
    #world = platec_text.Terrain(8)
    window = Window(world=world, width=800, height=600, caption='PythonCraft', resizable=True)
    setup()
    pyglet.app.run()

if __name__ == '__main__':
    main(1000)
  