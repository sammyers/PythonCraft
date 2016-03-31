import math

import pyglet
from pyglet.window import key, mouse
from pyglet.gl import *

FPS = 60

DIRECTIONS = [(1, 0, 0),
              (-1, 0, 0),
              (0, 1, 0),
              (0, -1, 0),
              (0, 0, 1),
              (0, 0, -1)]

def cube_vertices(x, y, z, n):
    """ Return the vertices of the cube at position x, y, z with size 2*n.
    """
    return [
        x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # top
        x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
        x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # left
        x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # right
        x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # front
        x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # back
    ]

class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.batch = pyglet.graphics.Batch()

        self.model = Model()

        self.exclusive = True

        x, y, z = (0, 0, -4)

        vertex_data = cube_vertices(x, y, z, 0.5)

        self.batch.add(24, GL_QUADS, None,
            ('v3f/static', vertex_data),
            ('c3B/static', (255, 0, 0,
                     0, 255, 0,
                     0, 0, 255,
                     0, 255, 0,
                     255, 0, 0,
                     0, 255, 0,
                     0, 0, 255,
                     0, 255, 0,
                     255, 0, 0,
                     0, 255, 0,
                     0, 0, 255,
                     0, 255, 0,
                     255, 0, 0,
                     0, 255, 0,
                     0, 0, 255,
                     0, 255, 0,
                     255, 0, 0,
                     0, 255, 0,
                     0, 0, 255,
                     0, 255, 0,
                     255, 0, 0,
                     0, 255, 0,
                     0, 0, 255,
                     0, 255, 0)))

    def on_draw(self):
        self.clear()
        self.set_3d()
        glColor3d(1, 1, 1)
        self.batch.draw()
        self.set_2d()

    def set_3d(self):
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(61.0, width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        xz, xy = self.model.rotation
        glRotatef(xz, 0, 1, 0)
        glRotatef(-xy, math.cos(math.radians(xz)), 0, math.sin(math.radians(xz)))
        x, y, z = self.model.position
        glTranslatef(-x, -y, -z)

    def set_2d(self):
        """ Configure OpenGL to draw in 2d.
        """
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called when the player moves the mouse.
        Parameters
        ----------
        x, y : int
            The coordinates of the mouse click. Always center of the screen if
            the mouse is captured.
        dx, dy : float
            The movement of the mouse.
        """
        
        if self.exclusive:
            m = 0.15
            x, y = self.model.rotation
            x, y = x + dx * m, y + dy * m
            y = max(-90, min(90, y))
            self.model.rotation = (x, y)


class Model(object):

    def __init__(self):

        # All of the blocks in the world; key is a tuple of (x, y, z) position
        self.world = {}

        # Just the blocks that are visible, i.e. exposed on at least one side
        self.visible = {}

        # The player's position in the world, initially at the origin.
        self.position = (0, 0, 0)

        # The rotation of the player's view.
        self.rotation = (0, 0)

    def _initialize(self):
        """Generate terrain to initialize the world."""
        pass

    def add_block(position, block):
        """Place a block at a given set of coordinates."""
        pass

    def delete_block(position):
        """Remove a block from a given set of coordinates."""
        pass


class Block(object):

    def __init__(self):
        pass

class Grass(Block):
    pass

class Stone(Block):
    pass

def setup():
    """Basic OpenGL setup function."""
    glClearColor(0.5, 0.69, 1.0, 1)
    glEnable(GL_CULL_FACE)

def main():
    window = Window(width=800, height=600, caption='PythonCraft', resizable=True)
    setup()
    pyglet.app.run()

if __name__ == '__main__':
    main()