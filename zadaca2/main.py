from optimization import *
import random

def task1():
	print("============= 1. zadatak =============")
	e, x0 = readConfigFile("goldenCutConfig.txt")
	func = Function(f)
	x = goldenCutWithStartingPoint(Vector([1]), x0, func.value, e)
	print(x, func.counter)

	func = Function(f)
	x = coordinateAxesSearch(Vector([10]), e, func.value, 1)
	print(x, func.counter)

	func = Function(f)
	x0 = Vector([10])
	x = hookeJeeves(x0, e, func.value)
	print(x, func.counter)

	func = Function(f)
	x0 = Vector([10])
	x = nelderMead(x0, e, func.value)
	print(x, func.counter)

def task2():
	print("============= 2. zadatak =============")
	print("\n== Coordinate Axes Search ==")
	functions = [f1, f2, f3, f4]
	x0s = [Vector([-1.9, 2]), Vector([0.1, 0.3]), Vector.zeros(6), Vector([5.1, 1.1])]

	for i in range(len(functions)):
		func = Function(functions[i])
		x0 = x0s[i]
		x = coordinateAxesSearch(x0, e, func.value, len(x0))
		print(x, func.counter)

	# Hooke Jevees
	print("\n== Hooke Jeeves ==")

	for i in range(len(functions)):
		func = Function(functions[i])
		x0 = x0s[i]
		x = hookeJeeves(x0, e, func.value)
		print(x, func.counter)

	# Nelder Mead
	print("\n== Nelder Mead ==")

	for i in range(len(functions)):
		func = Function(functions[i])
		x0 = x0s[i]
		x = nelderMead(x0, e, func.value)
		print(x, func.counter)

def task3():
	print("============= 3. zadatak =============")
	print("\n== Hooke Jeeves ==")
	func = Function(f4)
	x0 = Vector([5.0, 5.0])
	x = hookeJeeves(x0, e, func.value)
	print(x, func.counter)

	print("\n== Nelder Mead ==")
	func = Function(f4)
	x = nelderMead(x0, e, func.value)
	print(x, func.counter)

def task4():
	print("============= 4. zadatak =============")
	func = Function(f1)
	x0 = Vector([0.5, 0.5])

	steps = [float(i) for i in range(1, 20)]
	for step in steps:
		x = nelderMead(x0, e, func.value, step = step)
		print("Step:", step, " minimum is:", x, " function evaluation count is:",func.counter)

def task5():
	print("============= 5. zadatak =============")
	n = 1
	func = Function(f6)
	x0 = Vector([random.uniform(-50, 50)])

	# x = nelderMead(x0, 1e-04, func.value)
	x = hookeJeeves(x0, 1e-04, func.value)
	# x = coordinateAxesSearch(x0, 1e-04, func.value, 1)
	print(x, func.counter)


if __name__ == "__main__":
	e = 1e-06

	task1()
	task2()
	task3()
	task4()
	task5()
	