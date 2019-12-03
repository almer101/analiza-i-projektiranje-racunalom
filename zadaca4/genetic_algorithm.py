from functions import *
from random import uniform, randint
from math import log, ceil, floor

class GeneticAlgorithm:

	def __init__(self, f, lower_bound, upper_bound, population_size = 50, pm = 0.01, max_iter = 8000, accuracy=1e-02, display_type='bin'):
		self.f = f
		self.lower_bound = lower_bound
		self.upper_bound = upper_bound
		self.population_size = population_size
		self.pm = pm
		self.max_iter = max_iter
		self.accuracy = accuracy
		self.display_type = display_type

	def run(self):
		population = self.initialize_population()
		# print(self.lower_bound + population[0][0] * self.accuracy)

		count = 0
		while count < self.max_iter:
			count += 1
			indexes = self.chooseThreeIndexes(population)
			worst, second_best, best = worstUnitIndex(indexes, population)

			# elitism is not needed since it is implicitly built in

			# TODO:
				# - define 2 cross operators for bin
				# - define 2 cross operators for flaot
				# - define 1 mutation operator for bin
				# - define 1 mutation operator for float
				# - each operator must take in account the constraints

			# cross best and second_best
			# mutate new child
			# evaulate child
			# population[worst] = child


	def initialize_population(self):
		population = []

		self.Ns = (self.upper_bound - self.lower_bound) * (1.0 / self.accuracy)
		self.max_Ns = (self.upper_bound - self.lower_bound) * (1.0 / self.accuracy)

		for i in range(len(self.Ns)):
			self.Ns[i] = int(ceil(log(self.Ns[i], 2)))
			self.max_Ns[i] = int(floor(self.max_Ns[i]))

		for i in range(self.population_size):
			unit = []
			for j in range(len(self.lower_bound)):
				if self.display_type == 'bin':
					n = randint(0, 2**self.Ns[j] - 1)
					n = min(n, self.max_Ns[j])
					unit.append(n)

				elif self.display_type == 'float':
					unit.append(uniform(lower_bound[j], upper_bound[j]))

			unit = Vector(unit)
			population.append((unit, self.evaluate_unit(unit)))

		return population

	def evaluate_unit(self, unit):
		if self.display_type == 'bin':
			return 1.0 / self.f(self.decode(unit))
		elif self.display_type == 'float':
			return 1.0 / self.f(unit)


	def chooseThreeIndexes(self, population):
		indexes = []
		while len(indexes) < 3:
			n = randint(0, len(population) - 1)
			if n not in indexes:
				indexes.append(n)

		return indexes

	def worstUnitIndex(self, indexes, population):
		indexes.sort(key = lambda x: population[x][1])
		return indexes[2], indexes[1], indexes[0]


	def decode(self, value):
		return self.lower_bound + value * self.accuracy
			

if __name__ == "__main__":
	
	func = F1()
	algorithm = GeneticAlgorithm(func.value, lower_bound = Vector([-4.0, -4.0]), upper_bound = Vector([6.0, 6.0]))

	algorithm.run()


