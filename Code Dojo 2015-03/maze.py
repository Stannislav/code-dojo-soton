from random import randint

sq = "#"
size = 15

class Node:
	def __init__(self, state, px, py, pred):
		self.state = state
		self.px = px
		self.py = py
		self.pred = pred

def generage_initial():
	maze = []
	sx = 0
	sy = size/2
	ex = size-1
	ey = size/2
	for i in range(size):
		maze.append([])
		for j in range(size):
			maze[i].append(sq)
	maze[sy][sx] = " "
	maze[sy][sx+1] = " "
	maze[ey][ex] = " "
	maze[ey][ex-1] = " "

	return Node(maze, sx+1, sy, None)

def print_maze(node):
	for line in node.state:
		print ''.join(line)

	print ""
	print "Done"

def generate_succesor(node, direction):
	x = node.px
	y = node.py
	state = node.state;
	# 0 = down, 1 = left, 2 = up, 3 = right

	for i in range(2):
		if direction == 0:
			y += 1
		elif direction == 1:
			x -= 1
		elif direction == 2:
			y -= 1
		elif direction == 3:
			x += 1
		state[y][x] = " "

	return Node(state, x, y, node)

def make_initial_path():
	pass

def main():
	curr_node = generage_initial()
	for i in range(50):
		curr_node = generate_succesor(curr_node, randint(0,3))
	print_maze(curr_node)

	#is_explored()

if __name__ == '__main__':
	main()



