from math import sqrt
from vector import *

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
	# print("Unimodal interval for direction ", h, " is ", l, r)
	return goldenCut(l, r, f, e)


def goldenCut(a, b, f, e):
	k = 0.5 * (sqrt(5) - 1)
	c = b - k * (b - a)
	d = a + k * (b - a)

	fc = f(c)
	fd = f(d)
	count = 2
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
		count += 1

	# print("Golden cut method evaluation count: ", count)
	return ((a + b) * 0.5, count)

def coordinateAxesSearch(x0, eps, f, n):
	evaluationCount = 0
	x = x0
	xs = x
	diff = Vector([5])

	while diff.module() > eps:
		xs = x
		for i in range(n):
			ei = Vector.unit(n, i)
			x, count = goldenCutWithStartingPoint(ei, x, f, e)
			evaluationCount += count
			# print(x)
		
		diff = x - xs

	# print("Diff is: ", diff.module(), " values are: ", x, xs)
	return (x, evaluationCount)

e = 1e-06

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

# ============= 1. zadatak ============= 
print(goldenCutWithStartingPoint(Vector([1]), Vector([1000]), f, e))

# ============= 2. zadatak ============= 
print("============= Coordinate Axes Search ============")
x0 = Vector([-1.9, 2])
x, count = coordinateAxesSearch(x0, e, f1, 2)
print(x, count)

x0 = Vector([0.1, 0.3])
x, count = coordinateAxesSearch(x0, e, f2, 2)
print(x, count)

n = 5
x0 = Vector.zeros(n)
x, count = coordinateAxesSearch(x0, e, f3, n)
print(x, count)

x0 = Vector([5.1, 1.1])
x, count = coordinateAxesSearch(x0, e, f4, 2)
print(x, count)


