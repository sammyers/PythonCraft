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

Guess what more text


### Graphical Engine



#### OpenGL Vertices

#### Chunk Loading

Some more text here

#### This is a subheading 