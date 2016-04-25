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

    int_hmap = [int(round(h)) for h in hmap]

    heightmap = np.reshape(int_hmap,(width,height))
    

    print max(hmap)

    # height_dict = {}
    # for z, row in enumerate(heightmap):
    #     for x, h in enumerate(row):
    #         for y in range(h + 1):
    #             height_dict[(x, y, z)] = 6 if h == 0 else (1 if y == h else (3 if y <= h - 3 else 2))

    return hmap


if __name__ == "__main__":
    seed = 3
    width = 1000
    height = 1000

    height_map = generate_heightmap(seed, width, height)
    np.set_printoptions(linewidth=200)

    #np.savetxt('dump.txt', height_map, delimiter=' ') 
    
    #matrix = ''

    np.savetxt('dump.csv', height_map, delimiter=',') # fmt='%i'

    # text_file = open("dump.txt", "w")
    # for i in range (len(height_map)):
    #     row = str(height_map[i,:])
    #     row = row.replace("[", "")
    #     row = row.replace("]", "")
  
    #     row = row + '; ' + '\n'
    #     text_file.write(row)
    #     #text_file.write('\n')


    # text_file.close()

  
