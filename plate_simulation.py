"""
Testing plate tectonics library
"""
import platec
import numpy as np


def generate_heightmap(seed, width, height):
    """Takes seed, width, height (other variables built in), returns a giant
    shitty list instead of an actual heightmap"""

    sea_level = 0.65
    erosion_period = 60
    folding_ratio = 0.02
    aggr_overlap_abs = 1000000
    aggr_overlap_rel = 0.33
    cycle_count = 2
    num_plates = 10

    p = platec.create(seed, width, height, sea_level, erosion_period,
                        folding_ratio, aggr_overlap_abs,
                        aggr_overlap_rel, cycle_count, num_plates)
    while platec.is_finished(p) == 0:
        platec.step(p)

    hm = platec.get_heightmap(p)
    pm = platec.get_platesmap(p)

    platec.destroy(p)
    return hm,pm



if __name__ == "__main__":
    seed = 3
    width = 100
    height = 100

    hmap,pmap = generate_heightmap(seed,width,height)
    int_hmap = [int(round(h)) for h in hmap]

    heightmap = np.reshape(int_hmap,(width,height))

    height_dict = {(x,y,z):1 for y in range(h) for x, h in enumerate(row)
                    for z, row in enumerate(heightmap)}
