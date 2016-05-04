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

    attributes: numpy subclass"""

    def __new__(cls, data):
        cells = [[Cell(z) for z in row] for row in data]
        obj = np.asarray(cells).view(cls)
        return obj


    def __array_finalize__(self,obj):
        if obj is None: return


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
        kc = 1 # sediment capacity constant
        ks = 0.5 # dissolving constant
        kd = 0.3 # deposition constant

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
        x1 = (x - self[x,y].velocity[1] * tstep) % self.shape[0]
        y1 = (y - self[x,y].velocity[2] * tstep) % self.shape[1]
        self[x,y].s = self[x1,y1].s1


    def evaporation(self,(x,y),temp_constant,tstep):
        """Removes water from simulation based on environmental temperature"""
        self[x,y].d = self[x,y].d2 * (1 - temp_constant * tstep)


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
