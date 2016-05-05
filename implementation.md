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

Once loaded, blocks are stored as 3-dimensional coordinates in the form of dictionary keys (the corresponding values are integers corresponding to block type). There are separate dictionaries to keep track of blocks that should be visible and cube vertices of visual blocks, and to map chunk positions (see Chunk Loading below) to coordinates of blocks within those chunks. 

#### OpenGL Vertices

When a block is supposed to be visually active, a helper function converts this position to a list of 24 vertex coordinates bounding the 6 faces (this is the format OpenGL takes). OpenGL can work with any relative coordinate system; for our purposes, each block has a width of 1 unit. These are "sized" relatively based on the player's field of view, which is 60 degrees. Each block ID is mapped to a set of 2-dimensional vertex coordinates that determine the textures of the top, bottom, and sides of that block, which can be returned as a list by a helper function and passed to OpenGL. Once cube and texture vertices have been generated, these lists are stored in a Pyglet batch and are rendered each frame until removed from the batch. Note: only blocks that can be seen (not surrounded on all sides) are rendered to reduce overhead. When drawing polygons to the screen, OpenGL uses a series of transformation matrices to move the camera (note: actually moving the world in reverse) according to the rotation and position of the player, establish perspective, and draw a 2-D overlay afterward.

#### Chunk Loading

In order to prevent all of the thousands of blocks from being rendered at once, the world is sectioned into 25x25-block sections (no y-coordinate limit) and rendered in a certain radius around the player as necessary. When a chunk is hidden or shown, the chunk mapping dictionary is used to hide or show each visual block in each position within the chunk. The current chunk the player is in is checked during each tick, allowing the active radius to be updated accordingly.
