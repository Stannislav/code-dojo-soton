import numpy as np
import copy
import random

whowins = 1 # 1 = Blue, 2 = Red
data = []
districts = []
new_districts = []

def read_data():
	global data
	f = open("input.txt",'r')
	for line in f:
		data.append([int(c) for c in line[:-1]])
	# print data
	f.close()

def output_districts():
	fout = open("output.txt",'w')
	for l in districts:
		for c in l:
			fout.write("" + str(c))
		fout.write("\n")
	fout.close()

def init_stripes():
	global districts
	global new_districts
	# districts = copy.deepcopy(data)
	for i in range(100):
		districts.append([i/10 for x in range(100)])
	new_districts = copy.deepcopy(districts)

def deform():
	global districts
	global new_districts
	new_districts = copy.deepcopy(districts)
	# vertically
	for i in range(0,99):
		for j in range(100):
			if new_districts[i][j] != new_districts[i+1][j]:
				if random.random() < 0.5:
					new_districts[i+1][j] = new_districts[i][j]
	# horizontally
	for i in range(0,100):
		for j in range(99):
			if new_districts[i][j] != new_districts[i][j+1]:
				if random.random() < 0.5:
					new_districts[i][j+1] = new_districts[i][j]

def score():
	totals = [[0 for i in range(10)] for j in range(3)]
	distric_wins = []

	for i in range(99):
		for j in range(100):
			totals[data[i][j]][districts[i][j]] += 1
			# print str(i) + "," + str(j) + ":" + str(data[i][j])
			pass
	for i in range(10):
		if totals[1][i] > totals[2][i]:
			distric_wins.append(1)
		else:
			distric_wins.append(2)

	print totals
	print distric_wins
	# print sum(distric_wins)
	if sum(distric_wins) < 15:
		return 1
	elif sum(distric_wins) == 15:
		return 0
	else:
		return 2

def do_work():
	global districts
	init_stripes()
	for i in range(100):
		deform()
		districts = copy.deepcopy(new_districts)
		print score()
		if score() == whowins:
			break

if __name__ == '__main__':
	read_data()
	do_work()
	output_districts()