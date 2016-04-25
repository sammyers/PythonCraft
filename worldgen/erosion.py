"""
Hydraulic erosion simulation. Takes a heightmap, does jack shit cause it's not
written yet. Math for nerds.

Ref:
Mei, et al. Fast Hydraulic Erosion Simulation and Visualization on GPU
"""

import math as mfn
import numpy as np


class Cell(object):
    """Represents a cell in the erosion grid. Tracks relevant attributes.

    attributes: t_height, w_height, sediment, fL, fR, fT, fB (outflow
    fluxes), velocity"""

    def __init__(self, z):
        self.t_height = z
        self.w_height = 0
        self.sediment = 0
        self.fL = 0
        self.fR = 0
        self.fT = 0
        self.fB = 0
        self.velocity = [0,0]

    def __repr__(self):
        return ("Cell(t_height=%r,w_height=%r,sediment=%r,fL=%r,fR=%r,fT=%r,fB=%r,velocity=%r)"
        %(self.t_height,self.w_height,self.sediment,self.fL,self.fR,self.fT,
        self.fB,self.velocity))


class CellGrid(np.ndarray):
    """Grid of Cells with relevant functions. Represents the simulation surface.

    attributes: """

    def __new__(cls, data):
        cells = [[Cell(z) for z in row] for row in data]
        obj = np.asarray(cells).view(cls)
        return obj

    def __array_finalize__(self,obj):
        if obj is None: return

    def water_increment(dt):
        pass

    def flow_simulation(d1,bt,ft):
        pass

    def erosion_deposition(vtt,bt,st):
        pass

    def sediment_transportation(s1,vtt):
        pass

    def evaporation(d2):
        pass


if __name__ == "__main__":

    heightmap = np.array([[1,2,3],[4,5,6]])
    terrain = CellGrid(heightmap)
    print terrain
