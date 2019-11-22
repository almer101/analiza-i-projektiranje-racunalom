from optimization import *
from vector import *

class DerivableFunction(Function):

	def backward(self, x):
		pass

class F1(DerivableFunction):

	def __init__(self):
		super().__init__(f1)

	def backward(self, x):
		dx1 = -400 * x[0] * (x[1]-x[0]**2)**2 + 2 * (1 + x[0])
		dx2 = 200 * (x[1] - x[0]**2)
		return Vector([dx1, dx2])

class F2(DerivableFunction):

	def __init__(self):
		super().__init__(f2)

	def backward(self, x):
		dx1 = 2 * (x[0] - 4)
		dx2 =  8 * (x[1] - 2)
		return Vector([dx1, dx2])

class F3(DerivableFunction):

	def __init__(self):
		super().__init__(f3)

	def backward(self, x):
		dx1 = 2 * (x[0] - 2)
		dx1 = 2 * (x[1] + 3)
		return Vector([dx1, dx2])

class F4(DerivableFunction):

	def __init__(self):
		super().__init__(f4)

	def backward(self):
		dx1 = 2 * (x[0] - 3)
		dx2 = 2 * x[1]
		return Vector([dx1, dx2]) 

def f1(x):
	return 100 * (x[1]-x[0]**2)**2 + (1-x[0])**2

def f2(x):
	return (x[0]-4)**2 + 4 * (x[1] - 2)**2

def f3(x):
	return (x[0] - 2)**2 + (x[1] + 3)**2

def f4(x):
	return (x[0] - 3)**2 + x[1]**2

