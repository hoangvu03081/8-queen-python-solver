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
