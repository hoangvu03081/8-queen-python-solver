
import copy
import random

class State:
	def __init__(self, inference, base = 8):
		self.base = base

		self.vars = {}

		for i in range(1, self.base ** 2 + 1):
			self.vars[i] = inference[i]

		self.num_true = sum(map((True).__eq__, self.vars.values()))

	def __repr__(self):
		return ""

	def is_goal(self):
		return  self.num_true == 8

	def num_of_true_vars(self):
		return self.num_true

	def __hash__(self):
		return hash(sum(self.true_vars()))

	def true_vars(self):
		return [i for i in range(1, self.base ** 2 + 1) if self.vars[i]]
	
	def generate_neighbors(self, kb):
		
		next_true_vars = set([_ for _ in range(1, self.base ** 2 + 1)])
		
		for a,b in kb:
			if self.vars[a] and b in next_true_vars:
				next_true_vars.remove(b)
			elif self.vars[b] and a in next_true_vars:
				next_true_vars.remove(a)

		neighbors = set()

		for var in next_true_vars:
			if self.vars[var] == False:
				inference = copy.copy(self.vars)
				inference[var] = True
				neighbors.add(State(inference))

		return neighbors

	def make_random_move(self):
		n = random.choice([_ for _ in range(1, self.base ** 2 + 1)])
		self.vars[n] = True