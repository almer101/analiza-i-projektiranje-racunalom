from matrica import *
from vector import *
from math import sqrt, cos, sin

def x_dot(x, A, B, r, t):
	if B is None or r is None or t is None:
		return Matrica.matmul(A, x)
	else:
		return Matrica.matmul(A, x) + Matrica.matmul(B, r(t))

def euler(A, B, r, x0, T, tmax, real_x = None):
	lambdas = solve_lambda(A)
	t = 0.0
	x_prev = x0.copy()
	x_dot_prev = x_dot(x_prev, A, B, r, t)

	error = Matrica([[0.0],[0.0]])

	count = 0

	while t <= tmax:
		t += T
		count += 1

		x_new = x_prev + T * x_dot_prev
		x_dot_prev = x_dot(x_new, A, B, r, t)
		x_new_true = real_x(t, x0)

		diff = x_new_true - x_dot_prev
		for i in range(len(diff)):
			diff[i][0] = abs(diff[i][0])

		error += diff

		if count % 10 == 0:
			print(f"for t={t - T} x is:\n{x_prev}")

		x_prev = x_new

	return x_prev, error


def euler_reverse():
	pass

def trapeze():
	pass

def runge_kutta_4():
	pass

def pece2():
	pass

def pece():
	pass

def solve_lambda(A):
	if len(A) == 1:
		return [A[0][0]]
	elif len(A) == 2:
		return solve_quadratic([1, -A[0][0] - A[1][1], A[0][0]*A[1][1] - A[1][0]*A[0][1]])

def solve_quadratic(coefficients):
	a, b, c = coefficients[0], coefficients[1], coefficients[2]
	first = -b / (2 * a)
	d = b**2 - 4 * a * c
	if d >= 0:
		return [first + sqrt(d) / (2 * a), first - sqrt(d) / (2 * a)]
	else:
		return [complex(first, sqrt(-d) / (2 * a)), complex(first, -sqrt(-d) / (2 * a))]

def analytic(t, x0=None):
	return Matrica([[x0[0][0] * cos(t) + x0[1][0] * sin(t)], [x0[1][0] * cos(t) - x0[0][0] * sin(t)]])

if __name__ == "__main__":
	print("aa")
	A = Matrica([[0, 1], [-1, 0]])
	x = Matrica([[1], [1]])
	print(solve_lambda(A))
	b = Matrica.matmul(A, x)
	print(b)

	A = Matrica([[0.1]])
	print(solve_lambda(A))
	print(solve_quadratic([1, 1, 1]))

	print("##################")
	A = Matrica([[0, 1], [-1, 0]])
	x0 = Matrica([[1], [1]])
	x, error = euler(A, None, None, x0, T=0.01, tmax=10, real_x=analytic)
	print(f"Error is : \n{error}")




