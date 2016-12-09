import numpy as np

def ll(v):
	return np.sqrt(v[0]**2 + v[1]**2)

pos = (5, 3)
com = (0, 0)
speed = 2

vec = (com[0] - pos[0], com[1] - pos[1])
l = 2/ll(vec)
vec2 = (vec[0]*l, vec[1]*l)
print ll(vec2)

