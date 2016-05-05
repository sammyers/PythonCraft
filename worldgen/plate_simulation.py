"""
Platec plate tectonics library implementation, testing code in __main__.
Used in PythonCraft world generator.
"""
import platec
import numpy as np


def generate_heightmap(seed, width, height):
    """Takes seed, width, height (other variables built in), returns a
    dictionary heightmap. Keys: (x,y,z) coordinate tuples, Values: block IDs"""

    # various built-in tectonics variables
    sea_level = 0.65
    erosion_period = 60
    folding_ratio = 0.02
    aggr_overlap_abs = 1000000
    aggr_overlap_rel = 0.33
    cycle_count = 2
    num_plates = 10

    # runs plate tectonics simulation based on given and built in variables,
    # assigned to simulation variable p
    p = platec.create(seed, width, height, sea_level, erosion_period,
                        folding_ratio, aggr_overlap_abs,
                        aggr_overlap_rel, cycle_count, num_plates)
    while platec.is_finished(p) == 0:
        platec.step(p)

    # grabs a list of height values from p, assigns to hmap
    hmap = platec.get_heightmap(p)
    #pmap = platec.get_platesmap(p)

    # removes simulation from memory
    platec.destroy(p)

    # converts to other useful formats, including an actual array instead of a list
    # int_hmap = [int(round(h)) for h in hmap]
    heightmap = np.reshape(hmap,(width,height))

    # for testing
    # print max(hmap)

    # builds height dictionary from int_hmap coordinates and block IDs
    return heightmap


if __name__ == "__main__":
    seed = 7487670
    width = 1000
    height = 1000

    # from tempfile import TemporaryFile()
    # plates_ten_thousand.npy = TemporaryFile()

    heightmap = generate_heightmap(seed, width, height)
    np.save("plates_1000.npy",heightmap)

    # zeros = filter(lambda x: x[1] == 0, height_dict)
    # print len(zeros)

    # print height_dict
