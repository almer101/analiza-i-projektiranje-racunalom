from functions import *
from genetic_algorithm import *
import matplotlib.pyplot as plt
from statistics import median


def task1():
	print("=============== Task 1 ===============")

	func_names = ["F1", "F3", "F6", "F7"]
	funcs = [F1(), F3(), F6(), F7()]
	ns = [2, 5, 2, 2]
	for i, func in enumerate(funcs):
		lb = [-50.0 for j in range(ns[i])]
		ub = [150.0 for j in range(ns[i])]

		algorithm = GA(func.value, lower_bound = Vector(lb), upper_bound = Vector(ub), display_type='float')
		bestUnit = algorithm.run()

		print(f"Best unit for function {func_names[i]} and display type 'float' is:\n{bestUnit[0]} -> function value = {bestUnit[1]}")
		
		algorithm = GA(func.value, lower_bound = Vector(lb), upper_bound = Vector(ub), display_type='bin')
		bestUnit = algorithm.run()

		print(f"Best unit for function {func_names[i]} and display type 'bin' is:\n{bestUnit[0]} (decoded {algorithm.decode(bestUnit[0])}) -> function value = {bestUnit[1]}")
		print()


def task2():
	print("\n=============== Task 2 ===============")
	dimensions = [1, 3, 6, 10]
	func_names = ["F6", "F7"]
	funcs = [F6(), F7()]

	for i, func in enumerate(funcs):
		for d in dimensions:
			lb = [-50.0 for j in range(d)]
			ub = [150.0 for j in range(d)]

			algorithm = GA(func.value, lower_bound = Vector(lb), upper_bound = Vector(ub), display_type='float')
			bestUnit = algorithm.run()

			print(f"Best unit for function {func_names[i]} and dimension d = {d}:\n{bestUnit[0]} -> function value = {bestUnit[1]}")
		
		print()	

def task3():
	print("\n=============== Task 3 ===============")
	func_names = ["F6", "F7"]
	funcs = [F6(), F7()]
	dimensions = [3, 6]

	for i, func in enumerate(funcs):
		for d in dimensions:
			lb = [-50.0 for j in range(d)]
			ub = [150.0 for j in range(d)]	

			algorithm = GA(func.value, lower_bound = Vector(lb), upper_bound = Vector(ub), max_iter = 10000, display_type='float')
			bestUnit = algorithm.run()

			print(f"Best unit for function {func_names[i]} (FLOAT) and dimension d = {d}:\n{bestUnit[0]} -> function value = {bestUnit[1]}")
			
			algorithm = GA(func.value, lower_bound = Vector(lb), upper_bound = Vector(ub), max_iter = 10000, accuracy=1e-04, display_type='bin')
			bestUnit = algorithm.run()

			print(f"Best unit for function {func_names[i]} (BIN) and dimension d = {d}:\n{algorithm.decode(bestUnit[0])} -> function value = {bestUnit[1]}")
		
		print()


def task4():
	print("\n=============== Task 4 ===============")
	pop_sizes = [30, 50, 100, 200]
	pms = [0.02, 0.05, 0.1, 0.3, 0.6, 0.9]

	func_values = []

	lb = [-50.0 for j in range(2)]
	ub = [150.0 for j in range(2)]

	for pm in pms:
		func_values.append([])
		for i in range(10):
			algorithm = GA(F6().value, lower_bound = Vector(lb), upper_bound = Vector(ub), population_size = 50, pm = pm,  max_iter = 10000, display_type='float')
			bestUnit = algorithm.run()
			func_values[-1].append(bestUnit[1])

	minIndex = findMinIndex(func_values)
	ideal_pm = pms[minIndex]

	print("Ideal pm is", ideal_pm)

	func_values_1 = []
	for size in pop_sizes:
		func_values_1.append([])
		for i in range(15):
			algorithm = GA(F6().value, lower_bound = Vector(lb), upper_bound = Vector(ub), population_size = size, pm = ideal_pm,  max_iter = 10000, display_type='float')
			bestUnit = algorithm.run()
			func_values_1[-1].append(bestUnit[1])


	minIndex = findMinIndex(func_values_1)
	ideal_size = pop_sizes[minIndex]

	print("Ideal size is", ideal_size)

	return func_values


def findMinIndex(func_values):
	minIndex = None
	minSum = None

	for i in range(len(func_values)):
		med = median(func_values[i])

		if minSum is None:
			minSum = med
			minIndex = i
		elif med < minSum:
			minSum = med
			minIndex = i	

	return minIndex

def task5():
	func = F6()
	ks = [i for i in range(3, 15)]

	func_values = []
	lb = [-50.0 for j in range(2)]
	ub = [150.0 for j in range(2)]

	for k in ks:
		algorithm = GA(F6().value, lower_bound = Vector(lb), upper_bound = Vector(ub), population_size = 100, pm = 0.3,  max_iter = 10000, display_type='float', k = k)
		bestUnit = algorithm.run()
		func_values.append(bestUnit[1])

	return ks, func_values

if __name__ == "__main__":
	task1()
	task2()
	task3()
	func_values = task4()
	ks, medians = task5()

	# print(func_values)
	f, ax = plt.subplots(2,1)
	plt.subplot(2,1,1)
	plt.boxplot(func_values, labels = ["0.02", "0.05", "0.1", "0.3", "0.6", "0.9"])

	plt.subplot(2,1,2)
	plt.plot(ks, medians)
	plt.show()

