"""
generates 3D caves using fractal noise and returns a binary 3D matrix 
"""


import math
import numpy as np
from noise_map import terrain
import scipy.io as sio

def generate_cave_2D(size):
	"""
	generates a 2D cave using diamond square, fractal noise
	"""

	temp_noise_map = terrain(size)

	size = int(math.pow(2,size))+1


	noise_map = np.zeros((size,size), np.int16)

	mean = np.mean(temp_noise_map)

	for x in range(0,size):
		for y in range(0,size):
			if temp_noise_map[y][x] > mean/.922:

				noise_map[y,x] = 1
			else:
				noise_map[y,x] = 0

	return noise_map


def generate_cave_2D_XL(size, iterations):

	"""
	Generates a cave by stitching together a bunch of smaller caves
	"""

	test_cave = generate_cave_2D(size)
	test_cave_2 = generate_cave_2D(size)
	test_cave_3 = generate_cave_2D(size)
	test_cave_4 = generate_cave_2D(size)
	test_cave_5 = generate_cave_2D(size)
	test_cave_6 = generate_cave_2D(size)
	test_cave_7 = generate_cave_2D(size)
	test_cave_8 = generate_cave_2D(size)

	print len(test_cave), len(test_cave[0])

	a = combine_vert(test_cave,test_cave_2)

	b = combine_vert(test_cave_3,test_cave_4)

	c = combine_horiz(a,b)

	print len(c), len(c[0])

	d = combine_vert(test_cave_5,test_cave_6)

	e = combine_vert(test_cave_7,test_cave_8)

	f = combine_horiz(d,e)

	print len(f),len(f[0])

	g = combine_horiz(c,f)

	print len(g),len(g[0])

	h = combine_vert(g,g)

	return h


def combine_horiz(baby_1,baby_2):
	"""
	merges two arrays horizontally with an overlap
	"""
	
	overlap = 10

	baby_1_r = baby_1[len(baby_1)-overlap:len(baby_1)]

	baby_2_l = baby_2[0:overlap]

	baby_baby_rl = baby_1_r + baby_2_l

	combination = np.concatenate((baby_1[0:len(baby_1)-overlap].T,baby_baby_rl.T), axis = 1)

	combination = np.concatenate((combination,baby_2[overlap:len(baby_2)].T), axis = 1)

	return combination


def combine_vert(baby_1, baby_2):
	"""
	merges two arrays vertically with an overlap
	"""
	
	overlap = 10

	baby_1_b = baby_1[len(baby_1)-overlap:len(baby_1),0:len(baby_1)]

	baby_2_t = baby_2[0:overlap,0:len(baby_2)]

	baby_baby_tb = baby_1_b + baby_2_t 

	combination = np.concatenate((baby_1_b, baby_1[0:len(baby_1)-overlap,0:len(baby_1)]), axis= 0)
	combination = np.concatenate((combination, baby_2[overlap:len(baby_2),0:len(baby_2)]), axis = 0)

	return combination 


def depopulate_cave(cave):
	"""
	returns a cave with decreased volume
	"""
	size = len(cave)

	new_cave = np.zeros((size,size), np.int16)

	#if the inside of the cave is touching a wall
	#move the wall inward by a single point
	for x in range(0,size):
		for y in range(0,size):
			if cave[y,x] == 1:
				sides = 0
				if x-1 >= 0:
					if (cave[y,x-1]) == 0:
						sides +=1
				if y-1 >= 0:
					if (cave[y-1,x]) == 0:
						sides +=1

				if x +1 < size:
					if (cave[y,x-1]) == 0:
						sides += 1

				if y +1 < size:
					if (cave[y+1,x]) == 0:
						sides +=1

				if sides > 0:
					new_cave[y,x] = 0
				else:
					new_cave[y,x] = cave[y,x]
			else:
				new_cave[y,x] = cave[y,x]

	return new_cave


def generate_cave_3D(cave):
	"""
	generates a 3D heightmap of a cave by creating multiple
	layers of decreasing cave size 
	"""

	temp_cave = cave
	stack = np.zeros((len(cave),len(cave)),np.int16)

	#creates a 'stack' of 30 caves
	for i in range(30):
		temp2_cave = depopulate_cave(temp_cave)
		stack = np.dstack((stack,temp2_cave)) 
		temp_cave = temp2_cave

	return stack


if __name__ == "__main__":

	cave_one = generate_cave_2D_XL(7,4)

	cave_3D = generate_cave_3D(cave_one)

	sio.savemat('test.mat', {'cave_3D': cave_3D})
