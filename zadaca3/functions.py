from optimization import *
from vector import *
from matrica import *
from constraints import *
from math import log, inf

class F1(Function):

	def __init__(self):
		super().__init__(f1)

	def backward(self, x):
		self.backward_count += 1
		dx1 = -400 * x[0] * (x[1]-x[0]**2)**2 + 2 * (1 + x[0])
		dx2 = 200 * (x[1] - x[0]**2)
		return Vector([dx1, dx2])

	def hessian(self, x):
		mat = [[-400 * x[0] * x[1] + 1200 * x[0]**2 + 2, -400 * x[0]], [-400 * x[0], 200.0]]
		return Matrica(mat)

class F2(Function):

	def __init__(self):
		super().__init__(f2)

	def backward(self, x):
		self.backward_count += 1
		dx1 = 2 * (x[0] - 4)
		dx2 =  8 * (x[1] - 2)
		return Vector([dx1, dx2])

	def hessian(self, x):
		mat = [[2.0, 0.0], [0.0, 8.0]]
		return Matrica(mat)

class F3(Function):

	def __init__(self):
		super().__init__(f3)

	def backward(self, x):
		self.backward_count += 1
		dx1 = 2 * (x[0] - 2)
		dx2 = 2 * (x[1] + 3)
		return Vector([dx1, dx2])

	def hessian(self, x):
		mat = [[2.0, 0.0], [0.0, 2.0]]
		return Matrica(mat)

class F4(Function):

	def __init__(self):
		super().__init__(f4)

	def backward(self, x):
		self.backward_count += 1
		dx1 = 2 * (x[0] - 3)
		dx2 = 2 * x[1]
		return Vector([dx1, dx2]) 

	def hessian(self, x):
		mat = [[2.0, 0.0], [0.0, 2.0]]
		return Matrica(mat)

class G(Function):

	def __init__(self, constraints):
		self.constraints = []
		self.t = 1.0

		for c in constraints:
			if c.constraint_type == "inequity":
				self.constraints.append(c)


	def value(self, x):
		suma = 0.0
		for c in self.constraints:
			if not c.isSatisfied(x):
				suma += self.t * c.g(x)

		return -suma

class U(Function):

	def __init__(self, f, constraints, t):
		self.f = f
		self.t = t
		self.gs = []
		self.hs = []

		for c in constraints:
			if c.constraint_type == "inequity":
				self.gs.append(c)
			if c.constraint_type == "equation":
				self.hs.append(c)


	def value(self, x):
		value = self.f.value(x)
		gSum = 0.0
		hSum = 0.0

		for c in self.gs:
			a = c.g(x)
			if a <= 0.0:
				return inf
			else:
				gSum += log(a)

		for c in self.hs:
			hSum += (c.g(x))**2

		value = value - 1.0 / self.t * gSum + self.t * hSum

		return value



def f1(x):
	return 100 * (x[1]-x[0]**2)**2 + (1-x[0])**2

def f2(x):
	return (x[0]-4)**2 + 4 * (x[1] - 2)**2

def f3(x):
	return (x[0] - 2)**2 + (x[1] + 3)**2

def f4(x):
	return (x[0] - 3)**2 + x[1]**2

