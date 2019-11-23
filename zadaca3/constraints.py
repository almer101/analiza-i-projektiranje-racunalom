from vector import *

class Constraint:

	def __init__(self, satisfies):
		self.satisfies = satisfies

	def isSatisfied(self, x):
		pass

class ExplicitConstraint(Constraint):

	def __init__(self, xd, xg):
		'''
		it is expected for xd and xg to be vectors
		'''
		self.xd = xd
		self.xg = xg

	def isSatisfied(self, x):
		if len(x) != len(self.xd) or len(x) != len(self.xg):
			raise ValueError("Constraints and point are not the same dimensions")

		for i in range(len(x)):
			if x[i] < self.xd[i] or x[i] > self.xg[i]:
				return False

		return True

class ImplicitConstraint(Constraint):

	def __init__(self, g, constraint_type):
		self.constraint_type = constraint_type
		self.g = g

	def isSatisfied(self, x):
		if self.constraint_type == "inequity":
			return self.g(x) >= 0
		elif self.constraint_type == "equation":
			return self.g(x) == 0



if __name__ == "__main__":

	xd = Vector([1.0, 0.0])
	xg = Vector([1.5, 3.0])
	v = Vector([2.0, 2.3])

	c1 = ExplicitConstraint(xd, xg)
	print(c1.isSatisfied(v))



		