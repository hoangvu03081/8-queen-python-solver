from pysat.solvers import Solver
from collections import defaultdict
import argparse

def convert(row, col):
	return N * row + col + 1

def decode(idx):
	idx -= 1
	return idx // N, int(idx % N)

def generate_row_constraint(N):
	expected_set = []
	for row in range(N):
		indices  =[]
		for col in range(N):
			indices.append(convert(row, col))

		expected_set += [[val for val in indices]]

		for i in range(len(indices)):
			for j in range(i+1, len(indices)):
				expected_set.append([-indices[i], -indices[j]])

	return expected_set

def generate_column_constraint(N):
	expected_set = []
	for col in range(N):
		indices = []

		for row in range(N):
			indices.append(convert(row, col))

		expected_set += [[val for val in indices]]

		for i in range(len(indices)):
			for j in range(i + 1, len(indices)):
				expected_set.append([-indices[i], -indices[j]])

	return expected_set


def generate_diagonal_constraint(N):
	expected_set = []
	diag1 = defaultdict(lambda: [])
	diag2 = defaultdict(lambda: [])

	for row in range(N):
		for col in range(N):
			diag1[row - col].append((row, col))
			diag2[row + col].append((row, col))

	keys = diag1.keys()

	for key in keys:
		temp = diag1[key]

		for i in range(len(temp)):
			row1, col1 = temp[i]
			for j in range(i + 1, len(temp)):
				row2, col2 = temp[j]
				v1 = convert(row1, col1)
				v2 = convert(row2, col2)
				expected_set.append([-v1, -v2])

	keys = diag2.keys()


	for key in keys:
		temp = diag2[key]

		for i in range(len(temp)):
			row1, col1 = temp[i]

			for j in range(i + 1, len(temp)):
				row2, col2 = temp[j]
				v1 = convert(row1, col1)
				v2 = convert(row2, col2)
				expected_set.append([-v1, -v2])

	return expected_set

def draw_board(N, solution):
	board = [[_ for _ in range(N)] for _ in range(N)]

	for val in solution:
		row, col = decode(abs(val))
		if val < 0:
			board[row][col] = '| * |'
		else:
			board[row][col] = '| Q |'

	for row in board:
		print("".join(row))



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = "8-Queen SAT")
	parser.add_argument('--assumptions', type = int,default = [], nargs = '+',  help = "1-CNF")
	parser.add_argument('--base', type = int, default = 8, help = 'Base')

	args = parser.parse_args()

	N = args.base
	
	expected_set = generate_row_constraint(N) + generate_column_constraint(N) + generate_diagonal_constraint(N)

	solver = Solver(bootstrap_with = expected_set)
	solver.solve(assumptions =  args.assumptions)
	solution = solver.get_model()

	if solution:
		draw_board(N, solution)
	else:
		print("No solution")