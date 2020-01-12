from numeric_integration import *

def analytic1(t, x0=None):
	return Matrica([[x0[0][0] * cos(t) + x0[1][0] * sin(t)], [x0[1][0] * cos(t) - x0[0][0] * sin(t)]])

def task1():
	names = ['euler', 'euler_reverse', 'trapeze', 'runge_kutta_4', 'pece', 'pece2']

	T = 0.01
	tmax = 10
	ts = [(T * i) for i in range(int(tmax / T) + 1)]

	A = Matrica([[0, 1], [-1, 0]])
	x0 = Matrica([[1], [1]])

	for name in names:
		xs, error = integrate(A, None, None, x0, T=T, tmax=tmax, method=name, real_x=analytic1)
		print(f"Error is : \n{error}")
		plot_xs(ts, xs, title=name)
		

def task2():
	names = ['euler', 'euler_reverse', 'trapeze', 'runge_kutta_4', 'pece', 'pece2']

	T = 0.1
	tmax = 1
	ts = [(T * i) for i in range(int(tmax / T) + 1)]

	A = Matrica([[0, 1], [-200, -102]])
	x0 = Matrica([[1], [-2]])

	for name in names:
		xs, error = integrate(A, None, None, x0, T=T, tmax=tmax, method=name, real_x=analytic1)
		print(f"Error is : \n{error}")
		plot_xs(ts, xs, title=name)
		

def task3():
	names = ['euler', 'euler_reverse', 'trapeze', 'runge_kutta_4', 'pece', 'pece2']

	T = 0.01
	tmax = 10
	ts = [(T * i) for i in range(int(tmax / T) + 1)]

	A = Matrica([[0, -2], [1, -3]])
	B = Matrica([[2, 0], [0, 3]])
	x0 = Matrica([[1], [3]])

	for name in names:
		xs, error = integrate(A, B, r3, x0, T=T, tmax=tmax, method=name, real_x=analytic1)
		print(f"Error is : \n{error}")
		plot_xs(ts, xs, title=name)
		

def r3(t):
	return Matrica([[1], [1]])

def task4():
	names = ['euler', 'euler_reverse', 'trapeze', 'runge_kutta_4', 'pece', 'pece2']

	T = 0.01
	tmax = 1
	ts = [(T * i) for i in range(int(tmax / T) + 1)]

	A = Matrica([[1, -5], [1, -7]])
	B = Matrica([[5, 0], [0, 3]])
	x0 = Matrica([[-1], [3]])

	for name in names:
		xs, error = integrate(A, B, r3, x0, T=T, tmax=tmax, method=name, real_x=analytic1)
		print(f"Error is : \n{error}")
		plot_xs(ts, xs, title=name)


def r4(t):
	return Matrica([[t], [t]])

if __name__ == "__main__":
	task1()
	task2()
	task3()
	task4()
