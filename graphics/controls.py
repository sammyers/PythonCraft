from pyglet.window import key

MOVE = {
	key.W: (0, 1),
	key.A: (1, -1),
	key.S: (0, -1),
	key.D: (1, 1),
	key.SPACE: (2, 1),
	key.LSHIFT: (2, -1)
}