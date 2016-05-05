from worldgen import generate_heightmap, fractal_height_map

SEED = 7487670

FILENAME = "plates_1000.npy"

def generate_world(seed, width, height):
	"""
	Generate a world file using the algorithms in the worldgen package and store it as region files.
	"""
	world = generate_heightmap(seed, width, height)
	np.save(FILENAME, world)

if __name__ == "__main__":
	generate_world(SEED, 1000, 1000)
