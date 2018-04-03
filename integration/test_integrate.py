from math_class import LeftRektAngles, MiddleRektAngles, RightRektAngles, ArrayIntegration, ChunkArrayIntegration

from math import sin, pi

def linear_func(x):
	return  sin(x)


lra = LeftRektAngles(linear_func, -.5*pi, .5*pi, 50)
mra = MiddleRektAngles(linear_func, -.5*pi, .5*pi, 50)
rra = LeftRektAngles(linear_func, -.5*pi, .5*pi, 10000)

ari = ArrayIntegration(linear_func,  -.5*pi, .5*pi, 1000)
cari = ChunkArrayIntegration(linear_func, -.5 * pi, .5 * pi, 1000, 1000)

lra.integrate()
mra.integrate()
rra.integrate()

ari.integrate()
cari.integrate()

print("Left Rectangles: {}\n".format(lra.result))
print("Right Rectangles: {}\n".format(rra.result))
print("Middle Rectangles: {}\n".format(mra.result))
print("Array Integration: {}\n".format(ari.result))
print("Chunk Array Integration: {}\n".format(cari.result))