from pysat.solvers import Solver
from collections import defaultdict

expected_set = []
N = 4

def convert(row, col):
	return N * row + col + 1

for row in range(N):
	indices  =[]
	for col in range(N):
		indices.append(convert(row, col))

	expected_set += [[val for val in indices]]

	for i in range(len(indices)):
		for j in range(i+1, len(indices)):
			expected_set.append([-indices[i], -indices[j]])


for col in range(N):
	indices = []

	for row in range(N):
		indices.append(convert(row, col))

	expected_set += [[val for val in indices]]

	for i in range(len(indices)):
		for j in range(i + 1, len(indices)):
			expected_set.append([-indices[i], -indices[j]])


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


solver = Solver(bootstrap_with = expected_set)
solver.solve()
	


solution = solver.get_model()


board = [[_ for _ in range(N)] for i in range(N)]


idx = 0
for row in range(N):
	for col in range(N):
		if solution[idx] < 0:
			board[row][col] = "| * |"
		else:
			board[row][col] = "| Q |"

		idx += 1


for row in board:
	print(" ".join(row))