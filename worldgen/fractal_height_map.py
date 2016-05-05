"""
first run at diamond square method, with help of javascript tutorial: http://www.playfuljs.com/realistic-terrain-in-130-lines/
"""

import numpy as np
import math
import random


def terrain(detail):
	"""
	initializes a height map with a size specified by 'detail'
	and returns a dictionary of blocks containing x, y and z values
	"""

	#size defines the length and width of a height map
	size = math.pow(2,detail)+1
	max_length = int(size)


	#defines height map as numpy array
	big_mama = np.zeros((size,size), np.int32)

	#defines all the corners to be halfway up the height map
	big_mama[0,0] = size/2
	big_mama[0,size-1] = size/2
	big_mama[size-1,0] = size/2
	big_mama[size-1,size-1] = size/2

	#populates the height map with pseudo-random values
	divide(max_length,int(size-1),big_mama)

	#places height map into a dictionary
	height_dict = {}
	for z, row in enumerate(big_mama):
		for x, h in enumerate(row):
			for y in range(h + 1):
				height_dict[(x, y, z)] = 6 if h == 0 else (1 if y == h else 2)

	return height_dict


def divide(max_length, size, b_m):

	"""
	divides the grid into squares and diamonds recursively 
	in that order and then define's each points height
	by calling either the diamond and square function
	"""

	#higher value results in more rought terrain (0-1)
	roughness = .7

	#dicates how many squares the height map is divided into
	half = int(size/2)

	#earlier height definitions are larger in scale (height) than later height definitions
	scale = (roughness*(size))

	#ends recursive calls once size = 1
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

	#recursively calls divide again to increase detail
	divide(max_length,int(size/2), b_m)


def diamond(row, column, b_m, offset, size, ml):
	"""
	takes average of four surrounding points and sets that as the base height for the center point
	then adds a random offset value to the center point
	"""

	avg = []

	#checks if surrounding dimaond points exist
	#takes value if point exists
	if row - size >= 0:
		avg.append(b_m[row-size,column])
	if column - size >= 0:
		avg.append(b_m[row,column-size])
	if row + size < ml:
		avg.append(b_m[row+size,column])
	if column + size < ml:
		avg.append(b_m[row,column+size])

	#averages all existing surounding diamond points
	avgg = np.average(avg)

	b_m[row,column] = avgg + offset

def square(row, column, b_m, offset, size):
	"""
	computes the average height of the four surrounding points and adds and additional random height to
	average
	"""

	#calculates the average of the four surrounding points
	avg = np.average([b_m[row-size,column-size], b_m[row+size,column-size], b_m[row-size,column+size], b_m[row+size,column+size]])

	b_m[row,column] = avg + offset


if __name__ == "__main__":
 	b = terrain(4)


