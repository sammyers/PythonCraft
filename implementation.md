---
title: Implementation
layout: template
filename: implementation
--- 

### Libraries

Better Than Earth uses Pyglet to structure its rendering functionality, since Pyglet serves as a thin wrapper for OpenGL. While some elements of the program use classes and functions from Pyglet, the majority of rendering code is written directly in OpenGL. The terrain generation modules use Numpy for helper functions and data arrays, and PyPlatec for plate tectonics simulations.


### Program Structure

First, a series of algorithms iteratively generate a heightmap of the world, which is written to disk. Upon running the program itself, the world is loaded into memory and the camera is initialized at the origin of the coordinate system. 

#### Model-View/Controller

The main program uses a variant of the standard model-view-controller structure, with two main classes:

* Model - this stores the current state of the program, like player position and information about all of the blocks in the world. It contains helper functions for adding, removing, showing, and hiding blocks, as well as methods for processing delayed function calls (see Game Loop below).

* Window - this is subclassed from the Pyglet Window object and contains both "view" and "controller" elements. The window contains event handlers for mouse and keyboard actions, which update player rotation and position in the model. It's also responsible for drawing polygon vertices to the screen (see Graphical Engine below) based on game state in every cycle of the game clock.

#### Game Loop

60 times per second (by default) the window checks the current player position and motion vector and updates player motion accordingly. In addition, if the player has moved to a different region of the world (see Chunk Loading below), function calls to hide and show appropriate blocks to re-center the rendered areas around the player are queued. During each tick, the queue processes as many function calls as possible within a constant amount of time, then proceeds to the next tick. 


### Terrain Algorithms

The terrain the player explores is generated through a series of algorithms that produce and manipulate various heightmaps and three-dimensional arrays. The original heightmap is a fractal coastline initialized and subsequently heavily manipulated by the plate tectonics simulation. The map may then be scaled up through a combination of cubic interpolation and the diamond-square fractal surface procedure, then eroded through a simplified sediment-pipe model for surface flow. Caves may then be generated below the surface of the heightmap. As the final step, weather, latitude, and Holdridge life zone calculations would determine the material types and local environments.


#### Fractal Algorithms

Fractal algorithms largely compose the basis of modern algorithmic terrain generation. It's no surprise why; fractal techniques are relatively easy to implement, computationally inexpensive, and can generate some impressively realistic results. Under this category is diamond-square surface generation, Perlin noise in two and three dimensions, and fractal coastline generation. Unfortunately, fractal algorithms tend to generate consistently similar results, never achieving the extremes of variation found in many physical systems.


#### Evolutionary Algorithms

Evolutionary algorithms tend to be difficult and expensive to implement, as well as requiring high degrees of accuracy to physical systems to produce convincing results. Most work on iterative algorithmic processes has occured in isolation; much work has been done on producing accurate plate tectonics simulations alone. The iterative evolutionary algorithms we used include plate tectonics and hydraulic erosion.


### Graphical Engine



#### OpenGL Vertices

#### Chunk Loading

Some more text here

#### This is a subheading 
