from vector import *
from functools import reduce
from math import sin

class Function:

	def __init__(self, func):
		self.func = func
		self.counter = 0

	def value(self, x):
		self.counter += 1
		return self.func(x)

def findUnimodalInterval(h, x, f):
	l = x - h
	r = x + h
	m = x
	step = 1

	fm = f(m)
	fl = f(l)
	fr = f(r)

	if fm < fl and fm < fr:
		return (l, r)

	elif fm > fr:
		while fm > fr:
			l = m
			m = r
			fm = fr
			r = x + h * step
			step *= 2
			fr = f(r)
	else:
		while fm > fl:
			r = m
			m = l
			l = x - h * step
			step *= 2
			fl = f(l)

	return (l, r)


def goldenCutWithStartingPoint(h, starting_point, f, e):
	l, r = findUnimodalInterval(h, starting_point, f)
	return goldenCut(l, r, f, e)


def goldenCut(a, b, f, e):
	k = 0.5 * (sqrt(5) - 1)
	c = b - k * (b - a)
	d = a + k * (b - a)

	fc = f(c)
	fd = f(d)
	diff = b - a

	while diff.module() > e:
		if fc < fd:
			b = d
			d = c
			c = b - k *  (b - a)
			fd = fc
			fc = f(c)
		else:
			a = c
			c = d
			d = a + k * (b - a)
			fc = fd
			fd = f(d)
		
		diff = b - a

	return (a + b) * 0.5

def coordinateAxesSearch(x0, eps, f, n):
	x = x0
	xs = x
	diff = Vector([5])

	while diff.module() > eps:
		xs = x
		for i in range(n):
			ei = Vector.unit(n, i)
			x = goldenCutWithStartingPoint(ei, x, f, eps)
		
		diff = x - xs

	# print("Diff is: ", diff.module(), " values are: ", x, xs)
	return x

def hookeJeeves(x0, eps, f):
	xp = x0.copy()
	xb = x0.copy()
	dx = Vector([0.5 for i in range(len(x0))])

	while dx[0] >= eps:
		xn = explore(f, xp, dx)
		if f(xn) < f(xb):
			xp = 2 * xn - xb
			xb = xn
		else:
			dx *= 0.5
			xp = xb

	return xb

def explore(f, xp, dx):
	x = xp.copy()
	for i in range(len(x)):
		P = f(x)
		x[i] += dx[i]
		N = f(x)
		if N > P:
			x[i] -= 2 * dx[i]
			N = f(x)
			if N > P:
				x[i] += dx[i]
	return x

def nelderMead(x0, eps, f, alpha=1, beta=0.5, gamma=2, sigma=0.5, step=1.0):
	maxCount = 10000
	n = len(x0)
	
	simplex = [x0]

	for i in range(n):
		a = x0.copy()
		a[i] += step
		simplex.append(a)

	simplex = Vector(simplex)

	h, l = highestLowestValue(simplex, f)
	counter = 0

	while condition(simplex, f, h) > eps and counter < maxCount:
		counter += 1
		h, l = highestLowestValue(simplex, f)

		xc = centroid(simplex, h)
		xr = (1 + alpha) * xc - alpha * simplex[h]

		if f(xr) < f(simplex[l]):
			xe = (1 - gamma) * xc + gamma * xr
			if f(xe) < f(simplex[l]):
				simplex[h] = xe
			else:
				simplex[h] = xr
		else:
			for i in range(len(simplex)):
				if i == h: continue
				if f(xr) > f(simplex[i]):
					if f(xr) < f(simplex[h]):
						simplex[h] = xr
					xk = (1 - beta) * xc + beta * simplex[h]
					if f(xk) < f(simplex[h]):
						simplex[h] = xk
					else:
						for j in range(len(simplex)):
							if j == h: continue
							v = simplex[l] - simplex[j]
							simplex[j] += v * sigma
				else:
					simplex[h] = xr

	if counter == maxCount:
		print("Max count exceeded (", maxCount,")")

	suma = Vector([0.0 for i in range(len(simplex[0]))])
	for s in simplex:
		suma += s
	suma *= 1.0 / len(simplex)

	return suma

def condition(simplex, f, h):
	xc = centroid(simplex, h)
	suma = 0
	for i in range(len(simplex)):
		suma += (f(simplex[i]) - f(xc)) ** 2

	suma *= 1.0 / len(simplex)
	return sqrt(suma)

def centroid(simplex, h):
	xc = Vector([0.0 for i in range(len(simplex[0]))])
	for i in range(len(simplex)):
		if i == h: continue
		xc += simplex[i]

	xc *= 1.0 / (len(simplex) - 1)
	return xc

def highestLowestValue(simplex, f):
	maxIndex = 0
	minIndex = 0
	maxValue = f(simplex[maxIndex])
	minValue = f(simplex[minIndex])

	for i in range(len(simplex)):
		fx = f(simplex[i])
		if fx > maxValue:
			maxValue = fx
			maxIndex = i
		if fx < minValue:
			minValue= fx
			minIndex = i

	return maxIndex, minIndex

def readConfigFile(file):
	order = ["eps", "x0", "step", "alpha", "beta", "gamma", "sigma", "dx"]
	dictionary = {}

	lines = linesFromFile(file)

	for line in lines:
		if line.startswith("eps"):
			dictionary["eps"] = float(line.split()[1].strip())
		if line.startswith("x0"):
			values = line.split()[1:]
			x0 = []
			for value in values:
				x0.append(float(value.strip()))
			dictionary["x0"] = Vector(x0)
		if line.startswith("step"):
			dictionary["step"] = int(line.split()[1].strip())
		if line.startswith("alpha"):
			dictionary["alpha"] = float(line.split()[1].strip())
		if line.startswith("beta"):
			dictionary["beta"] = float(line.split()[1].strip())
		if line.startswith("gamma"):
			dictionary["gamma"] = float(line.split()[1].strip())
		if line.startswith("sigma"):
			dictionary["sigma"] = float(line.split()[1].strip())
		if line.startswith("dx"):
			values = line.split()[1:]
			dx = []
			for value in values:
				dx.append(float(value.strip()))
			dictionary["dx"] = Vector(dx)

	arr = []
	for key in order:
		if key in dictionary.keys():
			arr.append(dictionary[key])

	return tuple(arr)


def linesFromFile(file):
	f = open(file, "r")
	l = f.read()
	l = l.split("\n")
	lines = []
	for i in range(len(l)):
		if l[i].strip():
			lines.append(l[i])
	return lines


def f(x):
	return x[0]**2 - 6 * x[0] + 9

def f1(x):
	return 100 * (x[1] - x[0]**2)**2 + (1 - x[0])**2

def f2(x):
	return (x[0] - 4)**2 + 4 * (x[1] - 2)**2

def f3(x):
	suma = 0
	for i in range(len(x)):
		suma += (x[i] - (i + 1))**2
	return suma

def f4(x):
	return abs((x[0] - x[1]) * (x[0] + x[1])) + sqrt(x[0]**2 + x[1]**2)

def f6(x):
	sumSquares = 0.0
	for i in range(len(x)):
		sumSquares += x[i] ** 2
	return 0.5 + (sin(sumSquares) ** 2 - 0.5) / (1 + 0.001 * sumSquares)**2

