# Better Than Earth

A program to procedurally generate 3-dimensional worlds made of cubes based on realistic terrain generation algorithms. To run the program, first ensure there's a world file; if one hasn't already been generated, run generate_world.py with the desired SEED and FILENAME variables. Once saved, launch the simulation by running main.py (make sure the WORLD_FILE variable is the same as the name of the world file) with Python.

The current version uses a third-party texture pack for Mojang's Minecraft, and certain elements of the program structure were inspired by Michael Fogleman's "Minecraft" repository.

#### Dependencies:
* Pyglet
* Numpy
* PyPlatec

To install dependencies, execute this from the command line:

`pip install pyglet numpy pyplatec`

#### Controls:

__WASD:__ Normal movement

__Space:__ Fly up

__Shift:__ Fly down

__Esc:__ Pause