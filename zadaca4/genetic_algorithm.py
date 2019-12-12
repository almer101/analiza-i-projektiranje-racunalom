from functions import *
from random import uniform, randint, random, gauss
from math import log, ceil, floor

class GA:

	def __init__(self, f, lower_bound, upper_bound, population_size = 50, pm = 0.02, max_iter = 20000, accuracy=1e-03, display_type='float'):
		self.f = f
		self.lower_bound = lower_bound
		self.upper_bound = upper_bound
		self.population_size = population_size
		self.pm = pm
		self.max_iter = max_iter
		self.accuracy = accuracy
		self.display_type = display_type
		self.bin_cross_type = 'uniform' # uniform one_break
		self.bin_mutation_type = 'simple_bitwise'
		self.float_cross_type = 'arithmetic' # heuristic arithmetic
		self.float_mutation_type = 'gaussian'

	def run(self):
		population = self.initialize_population()
		# print(self.lower_bound + population[0][0] * self.accuracy)
		# print(self.max_Ns)

		count = 0
		# print(self.Ns)
		# print(population[0][0])
		while count < self.max_iter:
			count += 1
			indexes = self.chooseThreeIndexes(population)
			worst, second_best, best = self.worstUnitIndex(indexes, population)
			# elitism is not needed since it is implicitly built in

			# TODO:
				# - define 2 cross operators for bin
				# - define 1 mutation operator for bin
				# - define 2 cross operators for flaot *
				# - define 1 mutation operator for float *

			# cross best and second_best
			child = self.cross(population[best], population[second_best])

			# mutate new child
			self.mutate(child)
			
			# check constraints
			self.satisfy_constraints(child)

			# evaulate child
			child = (child, self.evaluate_unit(child))

			# put it in the population
			# if count % 1000 == 0:
			# 	print("Iter ============ ", count, " ================")

			if child[1] < 1e-08:
				return self.bestUnit(population)

			if child[1] < population[worst][1]:
				population[worst] = child


		return self.bestUnit(population)


	def initialize_population(self):
		population = []

		self.Ns = (self.upper_bound - self.lower_bound) * (1.0 / self.accuracy)
		self.max_Ns = (self.upper_bound - self.lower_bound) * (1.0 / self.accuracy)

		nSum = 0
		for i in range(len(self.Ns)):
			self.Ns[i] = int(ceil(log(self.Ns[i], 2)))
			nSum += self.Ns[i]
			self.max_Ns[i] = int(floor(self.max_Ns[i]))

		self.N_sum = nSum

		for i in range(self.population_size):
			unit = []
			for j in range(len(self.lower_bound)):
				if self.display_type == 'bin':
					n = randint(0, 2**self.Ns[j] - 1)
					n = min(n, self.max_Ns[j])
					unit.append(n)

				elif self.display_type == 'float':
					unit.append(uniform(self.lower_bound[j], self.upper_bound[j]))

			unit = Vector(unit)
			population.append((unit, self.evaluate_unit(unit)))

		return population

	def evaluate_unit(self, unit):
		if self.display_type == 'bin':
			return self.f(self.decode(unit))
		elif self.display_type == 'float':
			return self.f(unit)


	def chooseThreeIndexes(self, population):
		indexes = []
		while len(indexes) < 3:
			n = randint(0, len(population) - 1)
			if n not in indexes:
				indexes.append(n)

		return indexes

	def bestUnit(self, population):
		bestIndex = 0
		for i, unit in enumerate(population):
			if unit[1] < population[bestIndex][1]:
				bestIndex = i

		return population[bestIndex]

	def worstUnitIndex(self, indexes, population):
		indexes.sort(key = lambda x: population[x][1])
		# print(population[indexes[0]][1], " must be < ", population[indexes[1]][1])
		return indexes[2], indexes[1], indexes[0]


	def decode(self, value):
		return self.lower_bound + value * self.accuracy


	def cross(self, unit1, unit2):
		if self.display_type == 'bin':
			return self.binary_cross(unit1, unit2)
		elif self.display_type == 'float':
			return self.float_cross(unit1, unit2)
			
	def binary_cross(self, unit1, unit2):
		if self.bin_cross_type == 'one_break':
			return self.one_break_cross(unit1, unit2)
		elif self.bin_cross_type == 'uniform':
			return self.uniform_cross(unit1, unit2)

	def one_break_cross(self, unit1, unit2):
		# print("Ns are = ", self.Ns)
		break_line = randint(1, self.N_sum - 1)
		# print("Break line is = ", break_line)
		# print(f"[{unit1[0][0]:>09b}, {unit1[0][1]:>09b}]")
		# print(f"[{unit2[0][0]:>09b}, {unit2[0][1]:>09b}]")
		c1 = []
		c2 = []

		help_var = 0
		did_cross = False

		for i in range(len(self.Ns)):
			if not did_cross and break_line < self.Ns[i]:
				# on this item the number is broken
				help_var = 1
				did_cross = True

				mask1 = ((2**break_line) - 1) << (self.Ns[i] - break_line)
				mask2 = 2**(self.Ns[i] - break_line) - 1
				
				elt = 0
				# print(" {0:09b} mask1".format(mask1))
				# print(" {0:09b} mask2".format(mask2))
				elt += unit1[0][i] & mask1
				elt += unit2[0][i] & mask2
				c1.append(elt)
				# print(" {0:09b}".format(unit1[0][i] & mask1))
				# print(" {0:09b}".format(unit2[0][i] & mask2))
				
				elt = 0
				elt += unit2[0][i] & mask1
				elt += unit1[0][i] & mask2
				c2.append(elt)

			else:
				c1.append(unit1[0][i] if help_var == 0 else unit2[0][i])
				c2.append(unit2[0][i] if help_var == 0 else unit1[0][i])
				break_line -= self.Ns[i]

		c1 = Vector(c1)
		c2 = Vector(c2)

		if self.evaluate_unit(c1) < self.evaluate_unit(c2):
			return c1
		else:
			return c2

	def uniform_cross(self, unit1, unit2):
		R = []
		for i in range(len(self.Ns)):
			 N = self.Ns[i]
			 r = 0
			 for j in range(N):
			 	r <<= 1
			 	r += 1 if GA.flip_coin(self.pm) else 0

			 R.append(r)

		child = []
		for i in range(len(self.Ns)):
			value = (unit1[0][i] & unit2[0][i]) | (R[i] & (unit1[0][i] | unit2[0][i]))
			child.append(value)

		return Vector(child)

	def float_cross(self, unit1, unit2):
		if self.float_cross_type == 'arithmetic':
			alpha = 0.5
			return alpha * unit1[0] + (1 - alpha) * unit2[0]
		elif self.float_cross_type == 'heuristic':
			alpha = 0.5
			if unit1[1] < unit2[1]:
				# unit1 is better
				return unit1[0] + alpha * (unit1[0] - unit2[0])
			else:
				# unit2 is better
				return unit2[0] + alpha * (unit2[0] - unit1[0])
			
	def mutate(self, unit):
		if self.display_type == 'bin':
			return self.binary_mutate(unit)
		elif self.display_type == 'float':
			return self.float_mutate(unit)


	def binary_mutate(self, unit):
		R = []
		for i in range(len(self.Ns)):
			 N = self.Ns[i]
			 r = 0
			 for j in range(N):
			 	r <<= 1
			 	r += 1 if GA.flip_coin(0.5) else 0

			 R.append(r)

		for i in range(len(self.Ns)):
			# flip the chosen bits
			# print(f"{unit[i]:>09b} \n{R[i]:>09b} ^ \n=======\n{unit[i]^R[i]}")
			unit[i] ^= R[i]


	def float_mutate(self, unit):
		for i in range(len(unit)):
			if GA.flip_coin(self.pm):
				unit[i] += gauss(0, 1)


	def flip_coin(p):
		return random() < p


	def satisfy_constraints(self, unit):
		if self.display_type == 'bin':
			for i in range(len(unit)):
				unit[i] = min(unit[i], self.max_Ns[i])

		elif self.display_type == 'float':
			for i in range(len(unit)):
				unit[i] = min(unit[i], self.upper_bound[i])
				unit[i] = max(unit[i], self.lower_bound[i])

if __name__ == "__main__":
	
	func = F7()
	algorithm = GA(func.value, lower_bound = Vector([-5.0, -5.0]), upper_bound = Vector([15.0, 15.0]), display_type='bin')

	bestUnit = algorithm.run()
	print(bestUnit)
	print(algorithm.decode(bestUnit[0]))

	print("======= Test ======")

	a = 43
	b = 26
	bits = ceil(log(43, 2))
	mask = 2**bits - 1

	break_line = randint(1, bits - 1)

	mask1 = (2**break_line - 1) << (bits - break_line)
	mask2 = 2**(bits - break_line) - 1

	# print(break_line)
	# print("{0:06b}".format(mask1))
	# print("{0:06b}".format(mask2))
	# print("=========")
	# print("{0:06b}".format(a | mask))
	# print("{0:06b}".format(b & mask))
	# print("{0:06b}".format(a & mask))

	# unit1 = (Vector([43, 26]), None)
	# unit2 = (Vector([22, 10]), None)

	# child = algorithm.binary_cross(unit1, unit2)

	
	# print(child)

	# algorithm.binary_mutate(child)
	# algorithm.satisfy_constraints(child)
	# print(child)

