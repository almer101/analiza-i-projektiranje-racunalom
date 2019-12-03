from vector import *
from math import log, inf, sin

class Function:

	def __init__(self, func):
		self.func = func
		self.counter = 0
		self.backward_count = 0

	def value(self, x):
		self.counter += 1
		return self.func(x)

class F1(Function):

	def __init__(self):
		super().__init__(f1)


class F3(Function):

	def __init__(self):
		super().__init__(f3)


class F6(Function):

	def __init__(self):
		super().__init__(f6)


class F7(Function):

	def __init__(self):
		super().__init__(f7)


def f1(x):
	return 100 * (x[1]-x[0]**2)**2 + (1-x[0])**2

def f3(x):
	suma = 0
	for i in range(len(x)):
		suma += (x[i] - (i + 1))**2
	return suma

def f6(x):
	sumSquares = 0.0
	for i in range(len(x)):
		sumSquares += x[i] ** 2
	return 0.5 + (sin(sumSquares) ** 2 - 0.5) / (1 + 0.001 * sumSquares)**2

def f7(x):
	sumSquares = 0.0
	for i in range(len(x)):
		sumSquares += x[i]**2

	return (sumSquares)**0.25 * (1 + sin(50 * (sumSquares**0.1))**2)



