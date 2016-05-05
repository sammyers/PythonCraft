"""
this program incrementally built up fractal_height_map.py
this program interpolates a height map produced by pyplatec and 'textures'
it with fractal noise (diamond square)

refer to fractal_height_map.py for proper documentation
"""

import numpy as np
import math
import random
from plate_simulation_array import generate_heightmap
import fractal_height_map


def Terrain(detail):
	"""
	initializes a height map with a size specified by 'detail'
	returns a dictionary containing x, y and z values 
	"""
	
	size = int(math.pow(2,detail)+1)

	#retrieves a world from the
	world = generate_heightmap(7487670, size, size)


	world2 = world.tolist()

	world2 = add_zeros(world2)



	divide(len(world),2,world)


	#places height map into a dictionary
	height_dict = {}
	for z, row in enumerate(world):
		for x, h in enumerate(row):
			for y in range(h + 1):
				height_dict[(x, y, z)] = 6 if h == 0 else (1 if y == h else 2)

	return height_dict


def add_zeros(array):
	for row in range(0,len(array)):

		#check if row is even
		if row % 2 == 0:
			for column in range(len(array[row]),0,-1):
				array[row].insert(column,0)	
				#np.insert(array[row],column,0)
		else:
			for column in range(len(array[row])-1,-1,-1):
				array[row].insert(column,0)	
				#np.insert(array[row],column,0)

	return array 


def divide(max_length, size, b_m):

	"""
	divides the grid into squares and diamonds recursively in that order  
	"""

	roughness = .7 #dictates roughness of 

	half = int(size/2)
	# print half

	scale = 4 #(roughness*(size))

	#ends recursion once size = 1
	if half < 1:
		return

	#finds all the points that need a square part of algorithm applied to it
	for column in range(half, max_length, size):
		for row in range(half, max_length, size):

			square(row, column, b_m, random.random()*scale*2-scale, half)
		
	#finds all the points that need diamond part of algorithm applied to it
	for column in range(0, max_length, half):
		for row in range((column + half)%(size), max_length, size):
		
			diamond(row, column, b_m, random.random()*scale*2-scale, half, max_length)
		
	#calls divide again to increase detail 	
	divide(max_length,int(size/2), b_m)


def diamond(row, column, b_m, offset, size, ml):
	"""
	takes average of four surrounding points and sets that as the base height for the center point
	then adds a random offset value to the center point
	"""

	avg = []

	if row - size >= 0:
		avg.append(b_m[row-size,column])
	if column - size >= 0:
		avg.append(b_m[row,column-size])
	if row + size < ml:
		avg.append(b_m[row+size,column])
	if column + size < ml:
		avg.append(b_m[row,column+size])

	avgg = np.average(avg)

	b_m[row,column] = avgg + offset 

def square(row, column, b_m, offset, size):

	"""
	computes the average height of the four surrounding points and adds and additional random height to 
	average
	"""


	avg = np.average([b_m[row-size,column-size], b_m[row+size,column-size], b_m[row-size,column+size], b_m[row+size,column+size]])

	b_m[row,column] = avg + offset 



if __name__ == "__main__":
 	b = Terrain(4)

