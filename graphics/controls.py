from pyglet.window import key

# Mapping of movement keys to motions.
# First element is the axis to move in, second is the direction.
# e.g. (2, 1) corresponds to forward in the z direction.
MOVE = {
	key.W: (2, 1),
	key.A: (0, -1),
	key.S: (2, -1),
	key.D: (0, 1),
	key.SPACE: (1, 1),
	key.LSHIFT: (1, -1)
}