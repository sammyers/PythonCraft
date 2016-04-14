class Block(object):

    def __init__(self, id):
        self.id = id

# Mapping of block IDs to attributes of those blocks.
BLOCKS = {
	1: {
		'name': 'Grass',
		'texture': ((0, 15), (2, 15), (3, 15)),
		'durability': 1
		},
	2: {
		'name': 'Dirt',
		'texture': ((2, 15), (2, 15), (2, 15)),
		'durability': 1
		},
	3: {
		'name': 'Stone',
		'texture': ((1, 15), (1, 15), (1, 15)),
		'durability': 5
		},
	4: {
		'name': 'Brick',
		'texture': ((7, 15), (7, 15), (7, 15)),
		'durability': 5
		},
	5: {
		'name': 'Bookshelf',
		'texture': ((4, 15), (4, 15), (3, 13)),
		'durability': 2
		},
	6: {
		'name': 'Water',
		'texture': ((14, 15), (14, 15), (14, 15)),
		'durability': 1000
		},
	7: {
		'name': 'Diamond Block',
		'texture': ((8, 10), (8, 8), (8, 9)),
		'durability': 1000
		}
}
