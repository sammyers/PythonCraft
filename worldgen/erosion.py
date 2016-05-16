"""
Hydraulic erosion simulation. Takes a heightmap, does jack shit cause it's not
written yet. Math for nerds.

Ref:
Mei, et al. Fast Hydraulic Erosion Simulation and Visualization on GPU
"""

import math as mfn
import numpy as np
from fractal_height_map import terrain
import random


class Cell(object):
    """Represents a cell in the erosion grid. Tracks relevant attributes.

    attributes: b (terrain height), d (water height), s (sediment),
    fL, fR, fT, fB (outflow fluxes), velocity
    temp attributes: d1, d2, s1"""

    def __init__(self, z):
        self.b = z
        self.d = 0
        self.s = 0
        self.fL = 0
        self.fR = 0
        self.fT = 0
        self.fB = 0
        self.velocity = [0,0]

        self.d1 = 0
        self.d2 = 0
        self.s1 = 0

    def __repr__(self):
        return ("Cell(b=%r,d=%r,s=%r,fL=%r,fR=%r,fT=%r,fB=%r,velocity=%r)"
        %(self.b,self.d,self.s,self.fL,self.fR,self.fT,
        self.fB,self.velocity))


class CellGrid(np.ndarray):
    """Grid of Cells with relevant functions. Represents the simulation surface.

    attributes: ndarray subclass"""

    def __new__(cls, data):
        cells = [[Cell(z) for z in row] for row in data]
        obj = np.asarray(cells).view(cls)
        return obj


    def __array_finalize__(self,obj):
        if obj is None: return

    def run_simulation(self,tstep,ttotal):
        """runs the erosion simulation for ttotal time at tstep intervals"""
        steps = int(ttotal/tstep)
        for step in range(steps):
            it = np.nditer(self, flags=['refs_ok','multi_index'], op_flags=['readwrite'])
            while not it.finished:
                if random.random() < 0.1:
                    self.water_increment(it.multi_index, 1.0, tstep)
                self.flow_simulation(it.multi_index, tstep)
                self.erosion_deposition(it.multi_index, tstep)
                self.sediment_transportation(it.multi_index, tstep)
                # self.evaporation(index, 0.1, tstep)
                it.iternext()
        for i in range(100):
            for index in np.ndindex(*self.shape):
                self.evaporation(index, 0.1, tstep)

    def water_increment(self,(x,y),water_rate,tstep):
        """Adds water to a specified point, at water_rate amount per time"""
        self[x,y].d1 = self[x,y].d + water_rate * tstep


    def flow_simulation(self,(x,y),tstep):
        """Calculates outward flux of water to four neighboring cells and
        velocity field at point (x,y)"""
        A = 0.785 # cross-sectional area of virtual "pipe"

        # modulus wrapped indices in both directions
        xMinus = (x-1) % self.shape[0]
        xPlus = (x+1) % self.shape[0]
        yMinus = (y-1) % self.shape[1]
        yPlus = (y+1) % self.shape[1]

        # calculate total height differences with adjacent cells
        hL = self[x,y].b + self[x,y].d1 - self[xMinus,y].b - self[xMinus,y].d1
        hR = self[x,y].b + self[x,y].d1 - self[xPlus,y].b - self[xPlus,y].d1
        hB = self[x,y].b + self[x,y].d1 - self[x,yMinus].b - self[x,yMinus].d1
        hT = self[x,y].b + self[x,y].d1 - self[x,yPlus].b - self[x,yPlus].d1

        # fluxes outwards to adjacent cells (note: coordinate system is rotated)
        self[x,y].fL = max(0, self[x,y].fL + tstep * A * 9.81 * hL)
        self[x,y].fR = max(0, self[x,y].fR + tstep * A * 9.81 * hR)
        self[x,y].fB = max(0, self[x,y].fB + tstep * A * 9.81 * hB)
        self[x,y].fT = max(0, self[x,y].fT + tstep * A * 9.81 * hT)

        # total outflux, calculate k constant to prevent negative water values
        f_total = self[x,y].fL + self[x,y].fR + self[x,y].fB + self[x,y].fT
        if  f_total != 0:
            k = min(1, self[x,y].d1 / (f_total * tstep))
        else:
            k = 1

        self[x,y].fL *= k
        self[x,y].fR *= k
        self[x,y].fB *= k
        self[x,y].fT *= k

        # change in water level based on total flux in and out
        total_fin = (self[xMinus,y].fR + self[xPlus,y].fL + self[x,yMinus].fT
                    + self[x,yPlus].fB)
        total_fout = self[x,y].fL + self[x,y].fR + self[x,y].fB + self[x,y].fT
        delta_volume = tstep * (total_fin - total_fout)

        # update new temp water level, find average of start/end levels
        self[x,y].d2 = self[x,y].d1 + delta_volume
        dBar = (self[x,y].d1 + self[x,y].d2) / 2

        # find average flux/direction of water passing through cell
        av_flux_x = (self[xMinus,y].fR - self[x,y].fL + self[x,y].fR
                    - self[xPlus,y].fL) / 2
        av_flux_y = (self[x,yMinus].fT - self[x,y].fB + self[x,y].fT
                    - self[x,yPlus].fB) / 2

        # find velocity vector based on flux and average water level
        if av_flux_x != 0:
            u = av_flux_x / dBar
        else:
            u = 0
        if av_flux_y != 0:
            v = av_flux_y / dBar
        else:
            v = 0

        # update local velocity vector
        self[x,y].velocity = [u,v]


    def erosion_deposition(self,(x,y),tstep):
        """Calculates whether/how much sediment is picked up or deposited at
        each point based on constants, local tilt angle and velocity field"""
        kc = 0.5 # sediment capacity constant
        ks = 0.1 # dissolving constant
        kd = 0.1 # deposition constant

        # find local tilt angle by averaging absolutes of opposite pairs of angles
        alpha = (abs(mfn.atan(self[x,y].b - self[(x-1) % self.shape[0],y].b)
            - mfn.atan(self[x,y].b - self[(x+1) % self.shape[0],y].b))
            + abs(mfn.atan(self[x,y].b - self[x,(y-1) % self.shape[1]].b)
            - mfn.atan(self[x,y].b - self[x,(y+1) % self.shape[1]].b))) / 4

        # threshold of tilt before no sediment is picked up
        if alpha < 0.1:
            alpha = 0

        # carrying capacity based on tilt angle and velocity field
        capacity = kc * mfn.sin(alpha) * np.linalg.norm(self[x,y].velocity)

        # pick up sediment and add to suspended sediment with excess capacity
        if capacity > self[x,y].s:
            self[x,y].b = self[x,y].b - ks * (capacity - self[x,y].s)
            self[x,y].s1 = self[x,y].s + ks * (capacity - self[x,y].s)

        # deposit sediment if at or exceeding capacity
        if capacity <= self[x,y].s:
            self[x,y].b = self[x,y].b + kd * (self[x,y].s - capacity)
            self[x,y].s1 = self[x,y].s - kd * (self[x,y].s - capacity)


    def sediment_transportation(self,(x,y),tstep):
        """Takes new sediment level values from sediment in previous locations.
        Calculates previous location through velocity field, time step"""
        x1 = int((x - self[x,y].velocity[0] * tstep)) % self.shape[0]
        y1 = int((y - self[x,y].velocity[1] * tstep)) % self.shape[1]
        self[x,y].s = self[x1,y1].s1


    def evaporation(self,(x,y),temp_constant,tstep):
        """Removes water from simulation based on environmental temperature"""
        self[x,y].d = self[x,y].d2 * (1 - temp_constant * tstep)


if __name__ == "__main__":

    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    import scipy.io as sio

    # mountain = CellGrid(np.load("mountain.npy"))
    # mountain.run_simulation(0.1,10)
    # print "simulation complete"
    # heights = np.array([[cell.b for cell in row] for row in mountain])
    # print "height conversion finished"

    # continents = CellGrid(np.load("plates_1000.npy"))
    # continents.run_simulation(0.2,10)
    # heights = np.array([[cell.b for cell in row] for row in continents])
    # np.save("plates_1000_eroded.npy", heights)

    heights = np.load("plates_1000_eroded.npy")
    sio.savemat("plates_1000_eroded.mat", {'heights':heights})

    # X = np.arange(0, heights.shape[0])
    # Y = np.arange(0, heights.shape[1])
    # X, Y = np.meshgrid(X, Y)
    # Z = heights[X,Y]
    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='gist_earth', linewidth=0, antialiased=False)
    # # ax.set_zlim(-1.01, 1.01)
    #
    # fig.colorbar(surf, shrink=0.5, aspect=5)
    # plt.show()
