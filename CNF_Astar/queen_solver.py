try:
	from .state import State
	from .create_kb import *
except:
	from state import State
	from create_kb import *

from collections import defaultdict
import random
import time


class QueenSolver:
	def __init__(self, base = 8):
		self.kb = row_cnfs(base) + col_cnfs(8) + diag_cnfs(8)
		self.base = base

	def export_path(self, trace, goal):
		path = []
		state = goal
		while state:
			path.append(state)
			state = trace[state]

		return path[::-1]

	def __solve(self, initial_state, remain = 8, const  = 10):
		frontier = []
		expanded_list = []
		trace = {}
		f = {}
		f = defaultdict(lambda : float('inf'), f) 
		initial_state = State(initial_state)

		if initial_state.num_of_true_vars() == 0:
			initial_state.make_random_move()

		f[initial_state] = remain - initial_state.num_of_true_vars()

		frontier.append((f[initial_state], 0, initial_state, None))
		seen = set()

		while frontier:
			f_n, g_n, state, parent_state = frontier.pop(0)

			if state in seen: 
				continue

			trace[state] = parent_state
			expanded_list.append(state)
			seen.add(state)

			if state.is_goal():
				return self.export_path(trace, state), expanded_list

			
			neighbors = state.generate_neighbors(self.kb)

			if len(neighbors) == 0:
				continue
				
			for neighbor in neighbors:
				
				if neighbor in seen:
					continue
				
				g_ = g_n + 1
				h_ = const * (remain - state.num_of_true_vars())
				f_ = h_ + g_

				if f[neighbor] > f_:
					f[neighbor] = f_
					frontier.append((f_, g_, neighbor, state))

			frontier.sort(key = lambda x : x[0])
			
			
		return [], expanded_list

	def solve(self, initial_state, remain = 8, const = 10):
		start = time.time()
		path, expanded_list = self.__solve(initial_state, remain, const)
		end = time.time()

		return path, expanded_list, end - start


	def generate_cnf(self, state):
		true_vars = state.true_vars()
		clauses = []
		for var in true_vars:
			clauses += [list(map(lambda x: "-" + str(x), clause)) for clause in self.kb if var in clause]

		clauses = list(map(lambda x: str(x) + '\n', true_vars)) + list(map(lambda x: " ".join(x) + '\n', clauses))

		return clauses