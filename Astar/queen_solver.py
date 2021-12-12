from .state import State
from collections import defaultdict
import heapq
import random

class QueenSolver():
	def __init__(self, initial_state : str, base : int = 8, remain : int = 8, only_heuristics : bool = False):

		self.base = base
		self.column = self._create_column_string(initial_state)
		self.initial_state = State(initial_state, self.column, base)
		self.remain = remain
		self.base = base
		self.only_heuristics = only_heuristics
		self.constraint = set()
		self._generate_constraint()

	def count_attacking_pairs(self, state, initial = False):	
		if initial:
			return self.remain * (self.remain - 1) // 2

		count = 0
		queen_cells = state.queen_places

		for i in range(len(queen_cells)):
			for j in range(i + 1, len(queen_cells)):
				if (queen_cells[i], queen_cells[j]) in self.constraint:
					count += 1
				elif (queen_cells[j], queen_cells[i]) in self.constraint:
					count += 1

		return count

	def _create_column_string(self, initial_state):
		column = ['0' for i in range(self.base)]

		for idx in range(len(initial_state)):
			if initial_state[idx] == "1":
				col = int(idx % self.base)
				column[col] = "1"

		return column

	def _encode_cell(self, idx):
		return idx // self.base, int(idx % self.base)


	def export_path(self, trace, goal):
		path = []
		state = goal
		while state:
			path.append(state)
			state = trace[state]

		return path[::-1]


	def solve(self):

		frontier = []
		expanded_list = []
		trace = {}
		f = {}
		f = defaultdict(lambda : float('inf'), f)
		f[self.initial_state] = self.count_attacking_pairs(self.initial_state, initial = True)
		frontier.append((f[self.initial_state], self.remain, self.initial_state, None))
		seen = set()

		while frontier:
			f_n, g_n, state, parent_state = frontier.pop(0)

			if state in seen: 
				continue

			trace[state] = parent_state
			expanded_list.append(state)
			seen.add(state)

			if self._is_goal(state):
				return self.export_path(trace, state), expanded_list

			
			neighbors = state.generate_neighbors()

			if len(neighbors) == 0:
				continue
				
			for neighbor in neighbors:
				
				if neighbor in seen:
					continue
				
				g_ = g_n - 1 
				h_ = self.count_attacking_pairs(neighbor)
				f_ = h_ if self.only_heuristics else g_ + h_

				if f[neighbor] > f_:
					f[neighbor] = f_
					frontier.append((f_, g_, neighbor, state))

			frontier.sort(key = lambda x : x[0])
			
			
		return [], expanded_list

	def _is_goal(self, state):
		return state.count_queens() == self.base and self.count_attacking_pairs(state) == 0

	def _generate_constraint(self):
		self._generate_row_constraint()
		self._generate_col_constraint()
		self._generate_diagonal_constraint()

	def _generate_row_constraint(self):
		
		for row in range(self.base):
			cells = []
			for col in range(self.base):
				cells.append(self._encode(row, col))

			for i in range(len(cells)):
				for j in range(i + 1, len(cells)):
					self.constraint.add((cells[i], cells[j]))

	def _generate_col_constraint(self):
		for col in range(self.base):
			cells = []
			for row in range(self.base):
				cells.append(self._encode(row, col))

			for i in range(len(cells)):
				for j in range(i + 1, len(cells)):
					self.constraint.add((cells[i], cells[j]))

	def _generate_diagonal_constraint(self):
		
		diag1 = defaultdict(lambda: [])
		diag2 = defaultdict(lambda: [])

		for row in range(self.base):
			for col in range(self.base):
				diag1[row - col].append((row, col))
				diag2[row + col].append((row, col))

		keys = diag1.keys()
		for key in keys:
			temp = diag1[key]

			for i in range(len(temp)):
				row1, col1 = temp[i]
				for j in range(i + 1, len(temp)):
					row2, col2 = temp[j]
					v1 = self._encode(row1, col1)
					v2 = self._encode(row2, col2)
					self.constraint.add((v1, v2))

		keys = diag2.keys()
		for key in keys:
			temp = diag2[key]

			for i in range(len(temp)):
				row1, col1 = temp[i]

				for j in range(i + 1, len(temp)):
					row2, col2 = temp[j]
					v1 = self._encode(row1, col1)
					v2 = self._encode(row2, col2)
					self.constraint.add((v1, v2))


	def _encode(self, row, col):
		return self.base * row + col



