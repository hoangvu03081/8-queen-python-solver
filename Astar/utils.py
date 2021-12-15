def draw_state(state):
	board = [[_ for _ in range(state.base)] for i in range(state.base)]

	idx = 0
	for row in range(state.base):
		for col in range(state.base):
			if state[idx] == "0":
				board[row][col] = "| * |"
			else:
				board[row][col] = "| Q |"
			
			idx += 1

	for row in board:
		print(" ".join(row))


def convert_to_cnf_format(x, y):
	if x == y:
		return '{}\n'.format(x)

	if x > y:
		x,y = y, x
	return '-{} v -{}\n'.format(x,y)

def generate_cnf_clauses(state):

	cnf_clauses = []
	for i in state.queen_places:
		cnf_clauses.append(convert_to_cnf_format(i, i))
		row, col = i // state.base , int(i % state.base)
		for col_ in range(state.base):
			index = 8 * row + col_
			if index != i:
				cnf_clauses.append(convert_to_cnf_format(i, index))

		for row_ in range(state.base):
			index = 8 * row_ + col
			if index != i:
				cnf_clauses.append(convert_to_cnf_format(i, index))

		for row_ in range(state.base):
			for col_ in range(state.base):
				if row_ + col_ == row + col or row_ - col_ == row - col:
					index = 8 * row_ + col_
					if index != i:
						cnf_clauses.append(convert_to_cnf_format(i, index))

	return cnf_clauses


