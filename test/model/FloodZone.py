import numpy as np


def PolyArea(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


x = np.arange(0, 1, 0.001)
y = np.sqrt(1 - x ** 2)
print(f"{x}")
print(PolyArea(x, y))

points = [[0, 0], [-610, 610], [620, 620], [610, 610], [710, 710]]
x = []
y = []
for point in points:
    x.append(point[0])
    y.append(point[1])
    print(f"{x}")

from shapely.geometry import Polygon
pgon = Polygon(zip(x, y))  # Assuming the OP's x,y coordinates

print(pgon.area)
