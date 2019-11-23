from gradientOptimization import *

def task1():
	print("=============== Task 1 ===============")
	f = F3()
	x0 = Vector([0.0, 0.0])
	
	print("Not optimal step")
	xmin = gradient_descent(f, x0, 1E-06, line_search = False, eta = 1.0)
	print(xmin, " evaluation count: ", f.counter, " gradient count: ", f.backward_count)

	f = F3()
	x0 = Vector([0.0, 0.0])
	print("Optimal step")
	xmin = gradient_descent(f, x0, 1E-06, line_search = True, eta = 1.0)
	print(xmin, " evaluation count: ", f.counter, " gradient count: ", f.backward_count)

def task2():
	print("=============== Task 2 ===============")

	print("Function 1")
	f = F1()
	x0 = Vector([-1.9, 2.0])

	print("Gradient descent")
	xmin = gradient_descent(f, x0, 1E-06, line_search = True)
	print(xmin, " evaluation count: ", f.counter, " gradient count: ", f.backward_count)

	f = F1()
	x0 = Vector([-1.9, 2.0])
	print("Newton Raphson")
	xmin = newton_raphson(f, x0, 1E-06, line_search = True)
	print(xmin, " evaluation count: ", f.counter, " gradient count: ", f.backward_count)

	print("\nFunction 2")
	f = F2()
	x0 = Vector([0.1, 0.3])

	print("Gradient descent")
	xmin = gradient_descent(f, x0, 1E-06, line_search = True)
	print(xmin, " evaluation count: ", f.counter, " gradient count: ", f.backward_count)

	f = F2()
	x0 = Vector([0.1, 0.3])
	print("Newton Raphson")
	xmin = newton_raphson(f, x0, 1E-06, line_search = True)
	print(xmin, " evaluation count: ", f.counter, " gradient count: ", f.backward_count)

def task3():
	print("=============== Task 3 ===============")

	f = F1()
	x0 = Vector([-1.9, 2.0])

	g1 = ImplicitConstraint(lambda x: x[1] - x[0], "inequity")
	g2 = ImplicitConstraint(lambda x: 2 - x[0], "inequity")
	xd = Vector([-100, -100])
	xg = Vector([100, 100])
	ec = ExplicitConstraint(xd, xg)

	print("Function 1")
	xmin = box(f, x0, 1E-06, ec, [g1, g2])
	print(xmin, " evaluation count: ", f.counter, " gradient count: ", f.backward_count)

	f = F2()
	x0 = Vector([0.1, 0.3])

	print("Function 2")
	xmin = box(f, x0, 1E-06, ec, [g1, g2])
	print(xmin, " evaluation count: ", f.counter, " gradient count: ", f.backward_count)

def task4():
	print("=============== Task 4 ===============")

	g1 = ImplicitConstraint(lambda x: x[1] - x[0], "inequity")
	g2 = ImplicitConstraint(lambda x: 2 - x[0], "inequity")

	f = F1()
	print("Function 1")
	x0 = Vector([-1.9, 2.0])
	xmin = mixedNoConstraints(f, x0, 1E-06, [g1, g2])
	print(xmin, " evaluation count: ", f.counter, " gradient count: ", f.backward_count)

	f = F2()
	x0 = Vector([0.1, 0.3])
	print("Function 2")
	xmin = mixedNoConstraints(f, x0, 1E-06, [g1, g2])
	print(xmin, " evaluation count: ", f.counter, " gradient count: ", f.backward_count)

def task5():
	print("=============== Task 5 ===============")

	g1 = ImplicitConstraint(lambda x: 3 - x[0] - x[1], "inequity")
	g2 = ImplicitConstraint(lambda x: 3 + 1.5 * x[0] - x[1], "inequity")
	g3 = ImplicitConstraint(lambda x: x[1] - 1, "inequity")

	f = F4()
	x0 = Vector([0.0, 0.0])

	xmin = mixedNoConstraints(f, x0, 1E-06, [g1, g2, g3])
	print(xmin, " evaluation count: ", f.counter, " gradient count: ", f.backward_count)

if __name__ == "__main__":
	task1()
	task2()
	task3()
	task4()
	task5()

