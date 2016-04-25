import random 
class DiamondSquare:

    def __init__(self, size, roughness):

        self.size = (2 ** size) + 1
        self.max = self.size - 1
        self.roughness = roughness
        self.make_grid(self.size)
        self.divide(self.max)

    # Sets x,y position in self.grid
    def set(self, x, y, val):
        self.grid[x + self.size * y] = val;


    # Get's value of x, y in self.grid
    def get(self, x, y):
        if (x < 0 or x > self.max or y < 0 or y > self.max):
            return -1
        return self.grid[x + self.size * y]

    def divide(self, size):

        x = size / 2
        y = size / 2
        half = size / 2
        scale = self.roughness * size

        if (half < 1):
            return

        # Square
        for y in range(half, self.max, size):
            for x in range(half, self.max, size):
                s_scale = random.uniform(0, 1) * scale * 2 - scale
                self.square(x, y, half, s_scale)

        # Diamond
        for y in range(0, self.max + 1, half):
            for x in range((y + half) % size, self.max + 1, size):
                d_scale = random.uniform(0, 1) * scale * 2 - scale
                self.diamond(x, y, half, d_scale)

        self.divide(size / 2) 

    def square(self, x, y, size, scale):

        top_left = self.get(x - size, y - size)
        top_right = self.get(x + size, y - size)
        bottom_left = self.get(x + size, y + size)
        bottom_right = self.get(x - size, y + size)

        average = ((top_left + top_right + bottom_left + bottom_right) / 4)
        self.set(x, y, average + scale)

    def diamond(self, x, y, size, scale):

        """
                T

            L   X   R

                B
        """

        top = self.get(x, y - size)
        right = self.get(x + size, y)
        bottom = self.get(x, y + size)
        left = self.get(x - size, y)

        average = ((top + right + bottom + left) / 4)
        self.set(x, y, average + scale)



    def make_grid(self, size):

        self.grid = []

        for x in range(size * size):
            self.grid.append(-1)

        self.set(0, 0, self.max)
        self.set(self.max, 0, self.max /2 )
        self.set(self.max, self.max, 0)
        self.set(0, self.max, self.max / 2)

    def get_grid(self):
        return self.grid

a = DiamondSquare(7, 0.5)
print(a.get_grid())