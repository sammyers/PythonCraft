"""
Testing plate tectonics library
"""
import platec
import numpy as np


def generate_heightmap(seed, width, height):
    """Takes seed, width, height (other variables built in), returns a dictionary heightmap"""

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

    hmap = platec.get_heightmap(p)
    # pm = platec.get_platesmap(p)

    platec.destroy(p)
    
    int_hmap = [int(round(h*2)) for h in hmap]

    heightmap = np.reshape(int_hmap,(width,height))

    height_dict = {}
    for z, row in enumerate(heightmap):
        for x, h in enumerate(row):
            for y in range(h + 1):
                height_dict[(x, y, z)] = 6 if h == 0 else (1 if y == h else (3 if y <= h - 3 else 2))

    return height_dict


if __name__ == "__main__":
    seed = 3
    width = 100
    height = 100

    height_dict = generate_heightmap(seed, width, height)

    zeros = filter(lambda x: x[1] == 0, height_dict)
    print len(zeros)

    # print height_dict