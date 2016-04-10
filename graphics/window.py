import math

import pyglet
from pyglet.window import key, mouse
from pyglet.gl import *

from config import *
from model import Model
from controls import *

class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.model = Model()

        # Don't capture the mouse at first
        self.exclusive = False

        # Initialize the debug text
        self.label = pyglet.text.Label('', font_name='Arial', font_size=18, 
                                       x=10, y=self.height-10, 
                                       anchor_x='left', anchor_y='top',
                                       color=(255, 255, 255, 255),
                                       multiline=True,
                                       width=300)

        # Set the game to update physics
        pyglet.clock.schedule_interval(self.update, 1.0 / TICKS)

    def set_exclusive_mouse(self, exclusive):
        """
        If true, the game will capture the mouse. 
        If false, the game will ignore it.
        """
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def draw_label(self):
        """
        Draw the debug text.
        """
        x, y, z = self.model.position
        debug_string = 'Position: ({}, {}, {}) \n{} fps \nBlocks: {} \nBlocks shown: {} \n{}'
        self.label.text = debug_string.format(x, y, z, 
                                              pyglet.clock.get_fps(),
                                              len(self.model.world),
                                              len(self.model.visible),
                                              self.get_motion_vector())
        self.label.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """ 
        Called when the player moves the mouse.
        
        Parameters:
            x, y (int):
                The coordinates of the mouse click. Always center of the screen if
                the mouse is captured.
            dx, dy (float):
                The movement of the mouse.
        """
        if self.exclusive:
            m = 0.15 #Mouse sensitivity
            x, y = self.model.rotation
            x, y = x + dx * m, y + dy * m
            # Make sure up-down rotation is within a 180 degree range
            y = max(-90, min(90, y))
            self.model.rotation = (x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the player clicks one of the mouse buttons.
        """
        if self.exclusive:
            #Do something
            pass
        else: #Capture the mouse
            self.set_exclusive_mouse(True)

    def on_key_press(self, symbol, modifiers):
        """
        Called when the player presses a key.
        """
        if symbol == key.ESCAPE:
            self.set_exclusive_mouse(False)
        elif symbol in MOVE:
            self.model.motion[MOVE[symbol][0]] += MOVE[symbol][1]

    def on_key_release(self, symbol, modifiers):
        """
        Called when the player releases a key.
        """
        if symbol in MOVE:
            self.model.motion[MOVE[symbol][0]] -= MOVE[symbol][1]

    def set_3d(self):
        """
        Configure OpenGL to draw in 3D.
        This is where most of the OpenGL nonsense goes on.
        """
        # Get dimensions of the viewport
        width, height = self.get_size()
        # Enable depth testing (basically, draw pixels that are closer to the camera)
        glEnable(GL_DEPTH_TEST)
        # Apply a projection matrix (set up the space the viewer can see)
        glMatrixMode(GL_PROJECTION)
        # Transform from normalized device coordinates to 3D window coordinates
        glViewport(0, 0, width, height)
        
        # Reset the current matrix
        glLoadIdentity()
        # Set up a perspective projection matrix
        gluPerspective(FOV, width / float(height), 0.1, 60.0)
        # Switch to a modelview matrix (necessary to make translations and rotations)
        glMatrixMode(GL_MODELVIEW)
        
        # Translate and rotate the world 
        # (this is the reverse of a transformation from the origin to the camera)
        glLoadIdentity()
        xz, yz = self.model.rotation
        # Note: glRotatef takes the number of degrees to rotate, then the axis to rotate around
        # (the axis is specified by an x, y, z vector)
        glRotatef(xz, 0, 1, 0)
        # The up-down rotation is around an axis orthogonal to the current sight vector
        glRotatef(-yz, math.cos(math.radians(xz)), 0, math.sin(math.radians(xz)))
        x, y, z = self.model.position
        glTranslatef(-x, -y, -z)

    def set_2d(self):
        """ 
        Configure OpenGL to draw in 2D.
        Basically, switches to an orthographic view so we can draw over the current scene.
        """
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_draw(self):
        """
        Called by pyglet to draw the canvas.
        """
        self.clear()
        self.set_3d()
        glColor3d(1, 1, 1)
        self.model.batch.draw()
        self.set_2d()
        self.draw_label()

    def get_sight_vector(self):
        """
        Return a unit vector in the direction the player is currently looking.
        """
        pass

    def get_motion_vector(self):
        """
        Return a unit vector in the direction the player is currently moving.
        If the player is not moving, return a zero vector.
        """
        # Check for movement in x and z, y is operated on differently
        if any(self.model.motion[::2]):
            # Angle of motion relative to orientation (radians)
            motion = math.atan2(self.model.motion[2], self.model.motion[0])
        else:
            return (0, self.model.motion[1], 0)
        # Angle of orientation
        direction = math.radians(self.model.rotation[0])
        # Absolute angle of motion (0 radians is in the +x direction)
        angle = motion - direction
        x, z = math.cos(angle), math.sin(angle)
        return (x, self.model.motion[1], z)

    def update(self, dt):
        """
        Update player movement. Called once per tick.
        """
        x, y, z = self.model.position
        dx, dy, dz = self.get_motion_vector()
        x += dx * WALKING_SPEED * dt
        y += dy * FLYING_SPEED * dt
        z -= dz * WALKING_SPEED * dt
        self.model.position = (x, y, z)
