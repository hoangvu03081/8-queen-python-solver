from queen_solver import QueenSolver
from utils import *
import time
import numpy as np


run_time = []
for _ in range(70):	
	base = 8
	remain = 8
	initial_string = ["0" for _ in range(base * base)]

	e = QueenSolver(initial_state = initial_string, base = base, remain = remain, only_heuristics = False)

	start = time.time()
	path, expanded_list = e.solve()
	end = time.time()

	run_time.append(end - start)

print("Average time: ", np.mean(run_time))