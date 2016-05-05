"""first run at diamond square method, with help of javascript tutorial
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

	world = generate_heightmap(7487670, size, size)
	#world = fractal_height_map.Terrain(4)

	world2 = world.tolist()

	#print 'world2', world2

	#print world

	world2 = add_zeros(world2)

	#print 'added zeros', world2

	divide(len(world2),64,world2)

	world2 = world2*5
	#return world2
	#np.asarray(world2)
	#print world2
	#places height map into a dictionary
	height_dict = {}
	for z, row in enumerate(world2):
		for x, h in enumerate(row):
			#print h
			for y in range(h + 1):

				height_dict[(x, y, z)] = 6 if h == 0 else (1 if y == h else 2)

	return height_dict

	#return big_mama
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

def chop_chimneys(b_m):

	
			if row - size >= 0:
				avg.append(b_m[row-size,column])
			if column - size >= 0:
				avg.append(b_m[row,column-size])
			if row + size < ml:
				avg.append(b_m[row+size,column])
			if column + size < ml:
				avg.append(b_m[row,column+size])


def divide(max_length, size, b_m):

	"""
	divides the grid into squares and diamonds recursively in that order  
	"""

	roughness = .7 #dictates roughness of 

	half = int(size/2)
	# print half

	scale = (roughness*(size))/3

	#ends recursion once size = 1
	if half < 1:
		return

	#finds all the points that need a square part of algorithm applied to it
	for column in range(half, max_length, size):
		for row in range(half, max_length, size):
			# print row
			# print column
			#print 'scale', scale

			square(row, column, b_m, random.random()*scale*2-scale, half)
		
	#finds all the points that need diamond part of algorithm applied to it
	for column in range(0, max_length, half):
		for row in range((column + half)%(size), max_length, size):
			# print column
			# print row
			#print 'scale', scale

			diamond(row, column, b_m, random.random()*scale*2-scale, half, max_length)
		
	#calls divide again to increase detail 	
	divide(max_length,int(size/2), b_m)


def diamond(row, column, b_m, offset, size, ml):
	"""
	takes average of four surrounding points and sets that as the base height for the center point
	then adds a random offset value to the center point
	"""

	avg = []

	row = int(row)
	column = int(column)

	if row - size >= 0:
		avg.append(b_m[row-size][column])
	if column - size >= 0:
		avg.append(b_m[row][column-size])
	if row + size < ml:
		avg.append(b_m[row+size][column])
	if column + size < ml:
		avg.append(b_m[row][column+size])
	#print avg

	avgg = sum(avg)/len(avg) #np.average(avg)
	#print 'avg', avgg
	#print 'offset', offset
	offset = random.randint(0,2)
	if avgg == 0:
		return
	# elif avgg <= 1 and avgg != 0:
	# 	b_m[row][column] = 1
	
	elif avgg <= 2:
		offset = random.randint(0,1)
		b_m[row][column] = int(avgg + offset)
	else:
		offset = random.randint(0,2)
		b_m[row][column] = int(avgg + offset)
	# if x == 2 and y == 1:
	# 	b_m[x,y] = 0


def square(row, column, b_m, offset, size):

	"""
	computes the average height of the four surrounding points and adds and additional random height to 
	average
	"""

	offset = random.randint(0,2)
	avg = np.average([b_m[row-size][column-size], b_m[row+size][column-size], b_m[row-size][column+size], b_m[row+size][column+size]])
	if avg == 0:
		return



	#elif avg <= 1 and avg != 0:
		#b_m[row][column] = 1
	elif avg <= 2:
		offset = offset = random.randint(0,1)

		b_m[row][column] = int(avg + offset)
		
	else:
		offset = offset = random.randint(0,2)
		b_m[row][column] = int(avg + offset)




def test(numba):
	a = Terrain(numba)
 	b = Terrain(numba)
 	c = a*b/2
 	print c/2

 	height_dict = {}

	for z, row in enumerate(b):
		for x, h in enumerate(row):
			for y in range(h + 1):
				height_dict[(x, y, z)] = 0 if h == 2 else (1 if y == h else 2)

	return height_dict


if __name__ == "__main__":
 	b = Terrain(10)

 	#np.savetxt('dump2.csv', b, delimiter=',') 