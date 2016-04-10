import pyglet
from graphics import Window, setup

def main():
    window = Window(width=800, height=600, caption='PythonCraft', resizable=True)
    setup()
    pyglet.app.run()

if __name__ == '__main__':
    main()
