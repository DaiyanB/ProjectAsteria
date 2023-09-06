# from k import update_const, obj, Constant

# for _ in range(16):
#     for i in obj:
#         i.printc()

# Constant.update_const(Constant(), 17)

# for _ in range(16):
#     for i in obj:
#         i.printc()

import numpy as np
import math

from math import radians, sin, cos

r = np.array([5, 2])

theta = radians(float(input("Enter theta: ")))

rotation_matrix = np.array([[cos(theta), -sin(theta)], 
                            [sin(theta), cos(theta)]])

print(np.matmul(rotation_matrix, r))