from optimization import *
from vector import *
from functions import *
from matrica import *
from constraints import *
from math import log
import random

def gradient_descent(f, x0, e, line_search = False, eta = 0.001, max_iter = 10000):
	x = x0
	grad = f.backward(x)
	count = 0

	last = x.copy()

	while grad.module() > e:
		max_iter -= 1
		if max_iter <= 0:
			print("Max iter exceeded... ")		
			break

		if line_search:
			grad = grad * (1.0 / grad.module())
			x = goldenCutWithStartingPoint(grad, x, f, 1E-06)
		else:
			x = x - grad * eta

		if (x - last).module() < 1e-05:
			count += 1
			if count > 100: break
		else:
			count = 0

		last = x.copy()
		grad = f.backward(x)

	return x

def newton_raphson(f, x0, e, line_search = False, eta = 1.0):
	x = x0
	count = 0
	hessian = f.hessian(x)
	hessian = inverseOfMatrix(hessian)
	grad = Matrica([f.backward(x).array])

	dx = Matrica.matmul(grad, hessian)
	dx = Vector(dx[0])
	last = x.copy()

	while dx.module() > e:
		last = x.copy()
		if line_search:
			x = goldenCutWithStartingPoint(-dx, x, f, 1E-06)
		else:
			x = x - dx * eta

		if abs(f.value(x) - f.value(last)) < 1e-06:
			count += 1
			if count > 100: break
		else:
			count = 0

		hessian = inverseOfMatrix(f.hessian(x))
		grad = Matrica([f.backward(x).array])

		dx = Matrica.matmul(grad, hessian)
		dx = Vector(dx[0])

	return x

def box(f, x0, e, explicitConstraint, implicitConstraints, alpha = 1.3):
	count = 0
	if not explicitConstraint.isSatisfied(x0):
		raise ValueError("Explicit constraints not initially satisfied")
	
	for c in implicitConstraints:
		if not c.isSatisfied(x0):
			raise ValueError("Implicit constraints not initially satisfied")

	xc = x0.copy()
	points = [x0.copy()]

	for i in range(2 * len(x0) - 1):
		x = []
		for j in range(len(x0)):
			r = random.uniform(0.0, 1.0)
			value = explicitConstraint.xd[j] + r * (explicitConstraint.xg[j] - explicitConstraint.xd[j])
			x.append(value)

		x = Vector(x)
		while not constraintsSatisfied(implicitConstraints, x):
			x = 0.5 * (x + xc)

		points.append(x)
		xc = centroid(points)

	h, h2 = worst2points(points, f)

	last = xc.copy()

	while condition(points, f, h):
		xc = centroid(points, withoutIndex = h)
		xr = (1 + alpha) * xc - alpha * points[h]
		for i in range(len(explicitConstraint.xd)):
			if xr[i] < explicitConstraint.xd[i]:
				xr[i] = explicitConstraint.xd[i]
			elif xr[i] > explicitConstraint.xg[i]:
				xr[i] = explicitConstraint.xg[i]

		while not constraintsSatisfied(implicitConstraints, xr):
			xr = 0.5 * (xr + xc)

		if f.value(xr) > f.value(points[h2]):
			xr = 0.5 * (xr + xc)

		points[h] = xr

		h, h2 = worst2points(points, f)

		if (xc - last).module() < 1E-06:
			count += 1
			if count > 100: break
		else:
			count = 0

		last = xc.copy()
		# print(xc)

	return centroid(points)


def mixedNoConstraints(f, x0, e, implicitConstraints, t = 1.0):	
	count = 0
	x = findInternatPoint(x0, implicitConstraints)
	print("Internal point is =========> ", x)
	previous = None
	u = U(f, implicitConstraints, t)

	while previous is None or (x - previous).module() > e:
		previous = x.copy()
		x = hookeJeeves(x, 1E-06, u)
		t *= 10.0
		u.t = t

		if abs(f.value(x) - f.value(previous)) < 1E-02:
			count += 1
			if count > 100: break
		else:
			count = 0
	
	return x


def findInternatPoint(x0, implicitConstraints):
	func = G(implicitConstraints)
	result = hookeJeeves(x0, 1E-06, func)

	return result

def constraintsSatisfied(constraints, x):
	for c in constraints:
		if not c.isSatisfied(x):
			return False

	return True


def centroid(points, withoutIndex = -1):
	suma = Vector.zeros(len(points[0]))
	count = 0
	for i in range(len(points)):
		if i == withoutIndex: continue

		count += 1
		suma += points[i]
		
	return suma * (1.0 / count)


def condition(simplex, f, h):
	xc = centroid(simplex, withoutIndex = h)
	suma = 0
	for i in range(len(simplex)):
		suma += (f.value(simplex[i]) - f.value(xc)) ** 2

	suma *= 1.0 / len(simplex)
	return sqrt(suma)


def worst2points(points, f):
	h = 0
	h2 = 0

	for i in range(len(points)):
		if f.value(points[i]) > f.value(points[h]):
			h = i

	for i in range(len(points)):
		if i == h: continue
		if f.value(points[i]) > f.value(points[h2]):
			h2 = i

	return h, h2


if __name__ == "__main__":

	f = F1()
	x0 = Vector([-1.9, 2.0])

	print("Gradient descent")
	xmin = gradient_descent(f, x0, 1E-06, line_search = True)
	print(xmin)

	print("\nNewton Raphson")
	xmin = newton_raphson(f, x0, 1E-06, line_search = True)
	print(xmin)

	g1 = ImplicitConstraint(lambda x: x[1] - x[0], "inequity")
	g2 = ImplicitConstraint(lambda x: 2 - x[0], "inequity")
	xd = Vector([-100, -100])
	xg = Vector([100, 100])
	ec = ExplicitConstraint(xd, xg)

	print("\nBox")
	xmin = box(f, x0, 1E-06, ec, [g1, g2])
	print(xmin)

	print("\nMixed no constraints")
	xmin = mixedNoConstraints(f, x0, 1E-06, [g1, g2])
	print(xmin)

