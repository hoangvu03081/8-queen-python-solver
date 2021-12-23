try:
	from .state import State
	from .create_kb import *
	from .queen_solver import QueenSolver
except:
	from state import State
	from create_kb import *
	from queen_solver import QueenSolver
	


KB = row_cnfs(8) + col_cnfs(8) + diag_cnfs(8)

inference = {}

for var in range(1, 65):
	inference[var] = False 

inference[2] = True
#inference[64] = True
#inference[50] = True


############ Display flow ################

solver = QueenSolver()
path, expanded_list, time_ = solver.solve(inference, remain = 6)

print("Search time: ", time_)

if path:

	# get true variables of each state in the search path.
	# place queens in the corresponding cells of these variables.
	for state in path:
		print(state.true_vars())

	## ignore lines 36-49. Just use for testing.
	goal = path[-1]
	queens = []
	
	for var in goal.vars:
		if goal.vars[var]:
			queens.append(var)
	

	
	for i in range(len(queens)):
		for j in range(i + 1, len(queens)):
			if [queens[i], queens[j]] in KB or [queens[j], queens[i]] in KB:
				print('Invalid !!!')
	
else:
	## A path is not found 
	print("No solution")


# generate and save CNF clauses

cnf_clauses = solver.generate_cnf(goal)

print("".join(cnf_clauses))