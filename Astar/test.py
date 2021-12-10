from queen_solver import QueenSolver
from utils import *
import time


base = 8
remain = 8
initial_string = ["0" for _ in range(base * base)]
#initial_string[24] = "1"
#initial_string[62] = "1"
#initial_string[10] = "1"
#initial_string = "".join(initial_string)

#initial_string = "0000010000" -> base = 4, 8, remain = base - user input 
e = QueenSolver(initial_state = initial_string, base = base, remain = remain, only_heuristics = False)


start = time.time()
path, expanded_list = e.solve()
end = time.time()

print("Solving time: ", end - start)
print()

if path:
	for state in path:
		draw_state(state)
		print()
else:
	print("No Solution")
