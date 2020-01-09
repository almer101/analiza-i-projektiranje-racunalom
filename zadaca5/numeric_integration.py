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

		diff = x_new_true - x_new
		for i in range(len(diff)):
			diff[i][0] = abs(diff[i][0])

		error += diff

		if count % 100 == 0:
			print(f"for t={t - T} x is:\n{x_prev}")

		x_prev = x_new

	return x_prev, error


def euler_reverse(A, B, r, x0, T, tmax, real_x = None):
	lambdas = solve_lambda(A)
	t = 0.0
	x_prev = x0.copy()
	x_dot_prev = x_dot(x_prev, A, B, r, t)

	error = Matrica([[0.0],[0.0]])

	count = 0

	while t <= tmax:
		t += T
		count += 1

		I = Matrica.identity(len(A))
		inv = inverseOfMatrix(I - T * A)

		second_part = x_prev
		if B is not None and r is not None:
			second_part += T * Matrica.matmul(B, r(t))

		x_new = Matrica.matmul(inv, second_part)
		x_dot_prev = x_dot(x_new, A, B, r, t)
		x_new_true = real_x(t, x0)
		
		diff = x_new_true - x_new

		for i in range(len(diff)):
			diff[i][0] = abs(diff[i][0])

		error += diff

		if count % 100 == 1:
			print(f"for t={t - T:.2f} x is:\n{x_prev}")

		x_prev = x_new

	return x_prev, error

def trapeze(A, B, r, x0, T, tmax, real_x = None):
	lambdas = solve_lambda(A)
	t = 0.0
	x_prev = x0.copy()
	x_dot_prev = x_dot(x_prev, A, B, r, t)

	error = Matrica([[0.0],[0.0]])

	count = 0

	while t <= tmax:
		t += T
		count += 1

		I = Matrica.identity(len(A))
		inv = inverseOfMatrix(I - (T * 0.5) * A)

		second_part = Matrica.matmul(I + (T * 0.5) * A, x_prev)
		if B is not None and r is not None:
			second_part += T * 0.5 * Matrica.matmul(B, r(t))

		x_new = Matrica.matmul(inv, second_part)
		x_dot_prev = x_dot(x_new, A, B, r, t)
		x_new_true = real_x(t, x0)
		
		diff = x_new_true - x_new

		for i in range(len(diff)):
			diff[i][0] = abs(diff[i][0])

		error += diff

		if count % 100 == 1:
			print(f"for t={t - T:.2f} x is:\n{x_prev}")

		x_prev = x_new

	return x_prev, error

def runge_kutta_4(A, B, r, x0, T, tmax, real_x = None):
	t = 0.0
	x_prev = x0.copy()

	error = Matrica([[0.0],[0.0]])
	count = 0

	while t <= tmax:
		count += 1

		m1, m2, m3, m4 = calculate_ms(A, B, r, x_prev, t, T)
		t += T

		x_new = x_prev + T / 6.0 * (m1 + 2 * m2 + 2 * m3 + m4)
		x_new_true = real_x(t, x0)
		
		diff = x_new_true - x_new

		for i in range(len(diff)):
			diff[i][0] = abs(diff[i][0])

		error += diff

		if count % 100 == 1:
			print(f"for t={t - T:.2f} x is:\n{x_prev}")

		x_prev = x_new

	return x_prev, error

def calculate_ms(A, B, r, x, t, T):
	m1 = x_dot(x, A, B, r, t)
	m2 = Matrica.matmul(A, x + T * 0.5 * m1)
	if B is not None and r is not None:
		 m2 += Matrica.matmul(B, r(t + T * 0.5))
	
	m3 = Matrica.matmul(A, x + T * 0.5 * m2)
	if B is not None and r is not None:
		 m3 += Matrica.matmul(B, r(t + T * 0.5))

	m4 = Matrica.matmul(A, x + T * m3)
	if B is not None and r is not None:
		 m4 += Matrica.matmul(B, r(t + T))
	
	return m1, m2, m3, m4


def pece(A, B, r, x0, T, tmax, real_x = None):
	t = 0.0
	x_prev = x0.copy()

	error = Matrica([[0.0],[0.0]])
	count = 0

	while t <= tmax:
		count += 1

		x_new_0 = x_prev + T * x_dot(x_prev, A, B, r, t)
		x_new = x_prev + 0.5 * T * (x_dot(x_prev, A, B, r, t) + x_dot(x_new_0, A, B, r, t + T))
		x_new_true = real_x(t + T, x0)

		if count == 1:
			print(f"x_kapa je \n", x_new_0)
			print(f"x je \n", x_new_0)

		t += T
		
		diff = x_new_true - x_new

		for i in range(len(diff)):
			diff[i][0] = abs(diff[i][0])

		error += diff

		if count % 100 == 1:
			print(f"for t={t - T:.2f} x is:\n{x_prev}")

		x_prev = x_new

	return x_prev, error


def pece2(A, B, r, x0, T, tmax, real_x = None):
	t = 0.0
	x_prev = x0.copy()

	error = Matrica([[0.0],[0.0]])
	count = 0

	while t <= tmax:
		count += 1

		x_new_0 = x_prev + T * x_dot(x_prev, A, B, r, t)
		x_new_1 = x_prev + T * x_dot(x_new_0, A, B, r, t + T)
		x_new = x_prev + T * x_dot(x_new_1, A, B, r, t + T)
		x_new_true = real_x(t + T, x0)

		t += T
		
		diff = x_new_true - x_new

		for i in range(len(diff)):
			diff[i][0] = abs(diff[i][0])

		error += diff

		if count % 100 == 1:
			print(f"for t={t - T:.2f} x is:\n{x_prev}")

		x_prev = x_new

	return x_prev, error


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
	print("=========== EULER ===========")
	x, error = euler(A, None, None, x0, T=0.01, tmax=10, real_x=analytic)
	print(f"Error is : \n{error}")
	
	print("=========== EULER REVERSE ===========")
	x, error = euler_reverse(A, None, None, x0, T=0.01, tmax=10, real_x=analytic)
	print(f"Error is : \n{error}")

	print("=========== TRAPEZE ===========")
	x, error = trapeze(A, None, None, x0, T=0.01, tmax=10, real_x=analytic)
	print(f"Error is : \n{error}")

	print("=========== RUNGE-KUTTA 4 ===========")
	x, error = runge_kutta_4(A, None, None, x0, T=0.01, tmax=10, real_x=analytic)
	print(f"Error is : \n{error}")

	print("=========== PECE ===========")
	x, error = pece(A, None, None, x0, T=0.01, tmax=10, real_x=analytic)
	print(f"Error is : \n{error}")

	print("=========== PE(CE)^2 ===========")
	x, error = pece2(A, None, None, x0, T=0.01, tmax=10, real_x=analytic)
	print(f"Error is : \n{error}")

