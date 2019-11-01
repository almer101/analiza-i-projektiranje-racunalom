from math import sqrt

class Vector:

	def __init__(self, array):
		self.array = array

	def __getitem__(self, index):
		return self.array[index]

	def __setitem__(self, index, value):
		self.array[index] = value

	def __len__(self):
		return len(self.array)

	def __str__(self):
		s = "["
		for i in range(len(self.array)):
			s += str(round(self.array[i], 8))
			s += ", " if i != len(self.array) - 1 else ""

		s += "]"
		return s

	def __add__(self, other):
		if len(self.array) != len(other):
			print(len(self.array), len(other))
			raise ValueError("Cannot add 2 arrays which are not the same dimensions")

		result = []
		for i in range(len(other)):
			result.append(self.array[i] + other[i])

		return Vector(result)

	def __sub__(self, other):	
		if len(self.array) != len(other):
			print(len(self.array), len(other))
			raise ValueError("Cannot sub 2 arrays which are not the same dimensions, self.size=", len(self.array), " other.size",len(other))

		result = []
		for i in range(len(other)):
			result.append(self.array[i] - other[i])

		return Vector(result)

	def __mul__(self, other):
		return self.mul(other)

	def __rmul__(self, other):
		return self.mul(other)

	def mul(self, other):
		res = []
		for i in range(len(self.array)):
			res.append(self.array[i] * other)

		return Vector(res)

	def module(self):
		module = 0
		for i in range(len(self.array)):
			module += self.array[i] ** 2
		return sqrt(module)

	def copy(self):
		array = [i for i in self.array]
		return Vector(array)

	def unit(n, index):
		unit = []
		for i in range(n):
			unit.append(1 if i == index else 0)

		return Vector(unit)

	def zeros(n):
		zeros = []
		for i in range(n):
			zeros.append(0.0)

		return Vector(zeros)
