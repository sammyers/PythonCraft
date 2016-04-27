"""
Hydraulic erosion simulation. Takes a heightmap, does jack shit cause it's not
written yet. Math for nerds.

Ref:
Mei, et al. Fast Hydraulic Erosion Simulation and Visualization on GPU
"""

import math as mfn
import numpy as np
from fractal_height_map import terrain


class Cell(object):
    """Represents a cell in the erosion grid. Tracks relevant attributes.

    attributes: b (terrain height), d (water height), s (sediment), fL, fR, fT, fB
    (outflow fluxes), velocity
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

    attributes: numpy subclass"""

    def __new__(cls, data):
        cells = [[Cell(z) for z in row] for row in data]
        obj = np.asarray(cells).view(cls)
        return obj

    def __array_finalize__(self,obj):
        if obj is None: return

    def water_increment(self,(x,y),waterRate,tstep):
        # update temp water level with added water
        self[x,y].d1 = self[x,y].d + waterRate * tstep

    def flow_simulation(self,(x,y),tstep):
        A = 0.785 # cross-sectional area of virtual "pipe"

        # calculate total height differences with adjacent cells
        hL = self[x,y].b + self[x,y].d1 - self[x-1,y].b - self[x-1,y].d1
        hR = self[x,y].b + self[x,y].d1 - self[x+1,y].b - self[x+1,y].d1
        hB = self[x,y].b + self[x,y].d1 - self[x,y-1].b - self[x,y-1].d1
        hT = self[x,y].b + self[x,y].d1 - self[x,y+1].b - self[x,y+1].d1

        # fluxes outwards to adjacent cells (note: coordinate system is rotated)
        self[x,y].fL = max(0, self[x,y].fL + tstep * A * 9.81 * hL)
        self[x,y].fR = max(0, self[x,y].fR + tstep * A * 9.81 * hR)
        self[x,y].fB = max(0, self[x,y].fB + tstep * A * 9.81 * hB)
        self[x,y].fT = max(0, self[x,y].fT + tstep * A * 9.81 * hT)

        # total flux, calculate k constant to prevent negative water values
        fTotal = self[x,y].fL + self[x,y].fR + self[x,y].fB + self[x,y].fT
        if  fTotal != 0:
            k = min(1, self[x,y].d1 / (fTotal * tstep))
        else:
            k = 1

        self[x,y].fL *= k
        self[x,y].fR *= k
        self[x,y].fB *= k
        self[x,y].fT *= k

        # change in water level based on total flux in and out
        total_fin = self[x-1,y].fR +self[x+1,y].fL +self[x,y-1].fT +self[x,y+1].fB
        total_fout = self[x,y].fL +self[x,y].fR +self[x,y].fB +self[x,y].fT
        deltaVolume = tstep * (total_fin - total_fout)

        # update new temp water level, find average of start/end levels
        self[x,y].d2 = self[x,y].d1 + deltaVolume
        dBar = (self[x,y].d1 + self[x,y].d2) / 2

        # find average flux/direction of water passing through cell
        avFluxX = (self[x-1,y].fR -self[x,y].fL +self[x,y].fR -self[x+1,y].fL) / 2
        avFluxY = (self[x,y-1].fT -self[x,y].fB +self[x,y].fT -self[x,y+1].fB) / 2

        # find velocity vector based on flux and average water level
        if avFluxX != 0:
            u = avFluxX / dBar
        else:
            u = 0
        if avFluxY != 0:
            v = avFluxY / dBar
        else:
            v = 0

        # update local velocity vector
        self[x,y].velocity = [u,v]


    def erosion_deposition(self,(x,y),tstep):
        kc = 1 # sediment capacity constant
        ks = 0.5 # dissolving constant
        kd = 0.3 # deposition constant

        # find local tilt angle by averaging absolutes of opposite pairs of angles
        alpha = (abs(mfn.atan(self[x,y].b - self[x-1,y].b) - mfn.atan(self[x,y].b
        - self[x+1,y].b)) + abs(mfn.atan(self[x,y].b - self[x,y-1].b) -
        mfn.atan(self[x,y].b - self[x,y+1].b))) / 4

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


    def sediment_transportation(self,s1,vtt):
        pass

    def evaporation(self,d2):
        pass


if __name__ == "__main__":

    heightmap = terrain(5)
    step = 1
    t = CellGrid(heightmap)
    t.water_increment((3,4),4.0,step)
    t.flow_simulation((3,4),step)
    t.flow_simulation((2,3),step)
    t.flow_simulation((2,4),step)
    t.flow_simulation((2,5),step)
    t.flow_simulation((3,3),step)
    t.flow_simulation((3,5),step)
    t.flow_simulation((4,3),step)
    t.flow_simulation((4,4),step)
    t.flow_simulation((4,5),step)
    print t[2,3].b, t[2,4].b, t[2,5].b
    print t[3,3].b, t[3,4].b, t[3,5].b
    print t[4,3].b, t[4,4].b, t[4,5].b
    print t[3,4].velocity
    t.erosion_deposition((3,4),step)
    t.erosion_deposition((2,3),step)
    t.erosion_deposition((2,4),step)
    t.erosion_deposition((2,5),step)
    t.erosion_deposition((3,3),step)
    t.erosion_deposition((3,5),step)
    t.erosion_deposition((4,3),step)
    t.erosion_deposition((4,4),step)
    t.erosion_deposition((4,5),step)
    print t[2,3].s1, t[2,4].s1, t[2,5].s1
    print t[3,3].s1, t[3,4].s1, t[3,5].s1
    print t[4,3].s1, t[4,4].s1, t[4,5].s1
