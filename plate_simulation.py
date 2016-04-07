import platec

p = platec.create(3, 1000, 800,
                      0.65, 60,
                      0.02, 1000000,
                      0.33, 2, 10)
while platec.is_finished(p) == 0:
    platec.step(p)
hm = platec.get_heightmap(p)
platec.destroy(p)
