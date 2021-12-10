class State:
	def __init__(self, binary_string, column, base = 8):
		assert len(binary_string) == base ** 2
		self.binary_string = binary_string # exact coordinates of the queens
		self.base = base
		self.column = column 
		self.queen_places = self._get_queen_places()

	def __getitem__(self,idx):
		return self.binary_string[idx]

	def _get_queen_places(self):
		return [idx for idx in range(len(self.binary_string)) if self.binary_string[idx] == "1"]

	def __eq__(self, other):
		return int("".join(self.binary_string),2) == int("".join(other.binary_string),2)

	def __lt__(self, other):
		return int("".join(self.binary_string),2) < int("".join(other.binary_string),2)
 
	def __hash__(self):
		return hash("".join(self.binary_string))

	def __repr__(self):
		return "".join(self.binary_string)

	def generate_neighbors(self):

		index = -1

		for col in range(self.base):
			if self.column[col] == "0":
				index = col 
				break

		if index == -1:
			return []

		neighbors = set()

		for i in range(index, index + self.base * self.base, self.base):
			new_binary_string = self.binary_string[:]
			new_binary_string[i] = '1'
			col = int(i % self.base)
			new_column = self.column[:]
			new_column[col] = "1" 
			neighbors.add(State(new_binary_string, new_column, self.base))

		return neighbors

	def count_queens(self):
		return self.binary_string.count("1")