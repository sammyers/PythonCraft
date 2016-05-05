"""first run at diamond square method, with help of javascript tutorial
"""
from tempfile import TemporaryFile
import numpy as np
import math
import random


def terrain(detail):
	"""
	initializes a height map with a size specified by 'detail'
	returns a dictionary containing x, y and z values 
	"""
	
	#size defines the length and width of a height map
	size = math.pow(2,detail)+1
	max_length = int(size)
	
	
	#defines height map
	big_mama = np.zeros((size,size), np.int32)
	test_mama = np.zeros((size,size), np.int32)	
	
	#defines all the corners to be halfway up the height map
	big_mama[0,0] = size/2
	big_mama[0,size-1] = size/2
	big_mama[size-1,0] = size/2
	big_mama[size-1,size-1] = size/2

	print len(big_mama)


	# big_mama[0,0] = size/2
	# big_mama[0,size-1] = size/2
	# big_mama[size-1,0] = size/2
	# big_mama[size-1,size-1] = size/2


	# print big_mama

	# test_mama[0,0] = 10
	# test_mama[0,size-1] = 9
	# test_mama[size-1,0] = 2
	# test_mama[size-1,size-1] = size/2

	#print test_mama

	divide(max_length,int(size-1),big_mama)
	#np.set_printoptions(threshold='nan')

	#print big_mama
	#return big_mama
	# print big_mama

	#places height map into a dictionary
	height_dict = {}
	for z, row in enumerate(big_mama):
		for x, h in enumerate(row):
			for y in range(h + 1):
				height_dict[(x, y, z)] = 6 if h == 0 else (1 if y == h else 2)

	#return height_dict

	return big_mama

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

	scale = (roughness*(size))

	#ends recursion once size = 1
	if half < 1:
		return

	#finds all the points that need a square part of algorithm applied to it
	for column in range(half, max_length, size):
		for row in range(half, max_length, size):
			# print row
			# print column
			# print 'scale', scale

			square(row, column, b_m, random.random()*scale*2-scale, half)
		
	#finds all the points that need diamond part of algorithm applied to it
	for column in range(0, max_length, half):
		for row in range((column + half)%(size), max_length, size):
			# print column
			# print row
			# print 'scale', scale

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
	#print avg

	avgg = np.average(avg)
	# print 'avg', avgg
	# print 'offset', offset
	

	b_m[row,column] = avgg + offset 
	# if x == 2 and y == 1:
	# 	b_m[x,y] = 0


def square(row, column, b_m, offset, size):

	"""
	computes the average height of the four surrounding points and adds and additional random height to 
	average
	"""
	


	avg = np.average([b_m[row-size,column-size], b_m[row+size,column-size], b_m[row-size,column+size], b_m[row+size,column+size]])

	b_m[row,column] = avg + offset 




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
	#outfile = TemporaryFile()
 	b = terrain(2)
 	np.save('mountain.npy', b)
 	print np.load('mountain.npy')
 	#np.savetxt('dump2.csv', b, delimiter=',') 
