import numpy as np
import time

a = np.array((0,0,0))
b = np.array((1,1,0))

start = time.time()
for x in range(0, 100):
    for y in range(0, 100):
        for z in range(0, 100):
            v1 = np.array((x, y, z))
            v2 = np.array((z, y, x))
print("Time numpy: ", time.time() - start)

start = time.time()
for x in range(0, 100):
    for y in range(0, 100):
        for z in range(0, 100):
            d = (x**2 + y**2 + z**2)**0.5
print("Time built-in:", time.time() - start)