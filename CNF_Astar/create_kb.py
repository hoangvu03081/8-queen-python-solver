from collections import defaultdict

def convert(row, col, N = 8):
	return N * row + col + 1

def row_cnfs(N = 8):
	expected_set = []

	for row in range(N):
		indices  =[]
		for col in range(N):
			indices.append(convert(row, col))

		#expected_set += [[val for val in indices]]

		for i in range(len(indices)):
			for j in range(i+1, len(indices)):
				expected_set.append([indices[i], indices[j]])

	return expected_set

def col_cnfs(N):
	expected_set = []
	for col in range(N):
		indices = []

		for row in range(N):
			indices.append(convert(row, col))

		#expected_set += [[val for val in indices]]

		for i in range(len(indices)):
			for j in range(i + 1, len(indices)):
				expected_set.append([indices[i], indices[j]])

	return expected_set

def diag_cnfs(N):
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
				expected_set.append([v1, v2])

	keys = diag2.keys()


	for key in keys:
		temp = diag2[key]

		for i in range(len(temp)):
			row1, col1 = temp[i]

			for j in range(i + 1, len(temp)):
				row2, col2 = temp[j]
				v1 = convert(row1, col1)
				v2 = convert(row2, col2)
				expected_set.append([v1, v2])

	return expected_set