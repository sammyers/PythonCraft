import numpy as np
import math
import random
import os

from mayavi import mlab


os.environ['ETS_TOOLKIT'] = 'qt4'



def Terrain(detail):
	"""
	initializes a height map with a size specified by 'detail'
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
	mlab.surf(big_mama)
	mlab.show()
	

	# yv = np.meshgrid(x, y, sparse=True) 
	# np.plot(yv)


def divide(max_length,size, b_m):

	#some roughness constant...
	roughness = .7
	half = int(size/2)



	scale = roughness*size

	if half < 1:
		return


	for y in range(half, max_length, size):
		for x in range(half, max_length, size):
			try:
				square(x, y, b_m, random.randint(0,int(scale)), half)
			except ValueError:
				square(x, y, b_m, 1, half)
				
				print 'ooops sqr'
				print half
				print size

	for y in range(0, max_length, half):
		for x in range((y + half)%size, max_length, size):
			try:
				diamond(x, y, b_m, random.randint(0,int(scale)), half)
			except ValueError:
				diamond(x, y, b_m, 2, half) 

				print 'ooops dia'
				print half
				print size

	divide(max_length,int(size/2), b_m)






def diamond(x, y, b_m, offset, size):
	"""
	takes average of four surrounding points and sets that as the base height for the center point
	then adds a random offset value to the center point
	"""
	try:
		avg = np.average([b_m[x-size,y], b_m[x,y-size], b_m[x+size,y], b_m[x,y+size]])
	except IndexError:
		avg = size   
		print 'checkx, ', x + size
		print 'checky, ', y + size
		print 'height_check, ', avg + offset
	

	b_m[x,y] = avg + offset


def square(x, y, b_m, offset, size):

	avg = np.average([b_m[x-size,y-size], b_m[x+size,y-size], b_m[x-size,y+size], b_m[x+size,y+size]])

	b_m[x,y] = avg + offset


Terrain(10)



 