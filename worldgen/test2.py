
test_array = [[1, 2, 3, 4, 5,6],
				[2, 3, 4, 5, 6,7],
				[3, 4, 5, 6, 7,8],
				[4, 5, 6, 7, 8,9],
				[5, 6, 7, 8, 9,10]]

print test_array[0][1]

for row in range(0,len(test_array)):

	#check if row is even
	if row % 2 == 0:
		for column in range(len(test_array[row]),0,-1):
			test_array[row].insert(column,0)	
	else:
		for column in range(len(test_array[row])-1,-1,-1):
			test_array[row].insert(column,0)	

print test_array
	
size = 2
half = 1



for column in range(0, len(test_array), half):
	scale = 

		for row in range((column + half)%(size), max_length, size):
			# print column
			# print row
			print 'scale', scale

			diamond(row, column, b_m, random.random()*scale*2-scale, half, max_length)

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
	print 'avg', avgg
	print 'offset', offset
	

	b_m[row,column] = avgg + offset 
	# if x == 2 and y == 1:
	# 	b_m[x,y] = 0
