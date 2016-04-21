"""first run at diamond square method, with help of javascript tutorial
"""

import numpy as np
import math
import random


def Terrain(detail):
	"""
	initializes a height map with a size specified by 'detail'
	returns a dictionary containing x, y and z values 
	"""
	
	#size defines the length and width of a height map
	size = math.pow(2,detail)+1
	max_length = int(size)
	
	#defines height map
	big_mama = np.zeros((size,size), np.int32)

	
	#defines all the corners to be halfway up the height map
	big_mama[0,0] = size/2
	big_mama[0,size-1] = size/2
	big_mama[size-1,0] = size/2
	big_mama[size-1,size-1] = size/2


	divide(max_length,int(size),big_mama)
	#np.set_printoptions(threshold='nan')

	print big_mama

	#places height map into a dictionary
	height_dict = {}
	for z, row in enumerate(big_mama):
		for x, h in enumerate(row):
			for y in range(h + 1):
				height_dict[(x, y, z)] = 6 if h == 0 else (1 if y == h else 2)

	return height_dict


def divide(max_length, size, b_m):

	"""
	divides the grid into squares and diamonds recursively in that order  
	"""

	roughness = .5 #dictates roughness of 

	half = int(size/2)

	scale = (roughness*size)/2

	#ends recursion once size = 1
	if half < 1:
		return

	#finds all the points that need a square part of algorithm applied to it
	for y in range(half, max_length, size):
		for x in range(half, max_length, size):
			square(x, y, b_m, random.random()*scale*2-scale, half)
		
	#finds all the points that need diamond part of algorithm applied to it
	for y in range(0, max_length, half):
		for x in range((y + half)%(size), max_length, size):
			diamond(x, y, b_m, random.random()*scale*2-scale, half, max_length)
		
	#calls divide again to increase detail 	
	divide(max_length,int(size/2), b_m)


def diamond(x, y, b_m, offset, size, ml):
	"""
	takes average of four surrounding points and sets that as the base height for the center point
	then adds a random offset value to the center point
	"""

	avg = []

	# print 'x ', x
	# print 'y ',y

	if x - size >= 0:
		avg.append(b_m[x-size,y])
	if y - size >= 0:
		avg.append(b_m[x,y-size])
	if x + size < ml:
		avg.append(b_m[x+size,y])
	if y + size < ml:
		avg.append(b_m[x,y+size])
	#print avg

	avgg = np.average(avg)
	

	b_m[x,y] = avgg + offset
	if x == 2 and y == 1:
		b_m[x,y] = 10


def square(x, y, b_m, offset, size):

	"""
	computes the average height of the four surrounding points and adds and additional random height to 
	average
	"""

	avg = np.average([b_m[x-size,y-size], b_m[x+size,y-size], b_m[x-size,y+size], b_m[x+size,y+size]])

	b_m[x,y] = avg + offset


if __name__ == "__main__":
 	Terrain(3)