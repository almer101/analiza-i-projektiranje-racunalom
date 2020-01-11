from matrica import *
from vector import *
from math import sqrt, cos, sin
import matplotlib.pyplot as plt

def x_dot(x, A, B, r, t):
	if B is None or r is None or t is None:
		return Matrica.matmul(A, x)
	else:
		return Matrica.matmul(A, x) + Matrica.matmul(B, r(t))

def integrate(A, B, r, x0, T, tmax, method, real_x = None):
	t = 0.0
	x_prev = x0.copy()
	x_dot_prev = x_dot(x_prev, A, B, r, t)
	xs = [x_prev]

	error = Matrica([[0.0],[0.0]])

	count = 0

	while t < tmax:
		count += 1
		
		x_new = None
		if method == 'euler':
			x_new = euler_x_new(x_prev, t, A, B, r, T)
		elif method == 'euler_reverse':
			x_new = euler_reverse_x_new(x_prev, t, A, B, r, T)
		elif method == 'trapeze':
			x_new = trapeze_x_new(x_prev, t, A, B, r, T)
		elif method == 'runge_kutta_4':
			x_new = runge_kutta_4_x_new(x_prev, t, A, B, r, T)
		elif method == 'pece':
			x_new = pece_x_new(x_prev, t, A, B, r, T)
		elif method == 'pece2':
			x_new = pece2_x_new(x_prev, t, A, B, r, T)
		
		t += T
		x_new_true = real_x(t, x0)
		xs.append(x_new)

		diff = x_new_true - x_new
		for i in range(len(diff)):
			diff[i][0] = abs(diff[i][0])

		error += diff

		if count % 100 == 0:
			print(f"for t={t} x is:\n{x_new}")

		x_prev = x_new

	return xs, error


def euler_x_new(x_prev, t_prev, A, B, r, T):
	x_dot_prev = x_dot(x_prev, A, B, r, t_prev)
	x_new = x_prev + T * x_dot_prev
	return x_new


def euler_reverse_x_new(x_prev, t_prev, A, B, r, T):
	I = Matrica.identity(len(A))
	inv = inverseOfMatrix(I - T * A)

	second_part = x_prev
	if B is not None and r is not None:
		second_part += T * Matrica.matmul(B, r(t_prev + T))

	x_new = Matrica.matmul(inv, second_part)
	return x_new


def trapeze_x_new(x_prev, t_prev, A, B, r, T):
	I = Matrica.identity(len(A))
	inv = inverseOfMatrix(I - (T * 0.5) * A)

	second_part = Matrica.matmul(I + (T * 0.5) * A, x_prev)
	if B is not None and r is not None:
		second_part += T * 0.5 * Matrica.matmul(B, r(t_prev + T))

	x_new = Matrica.matmul(inv, second_part)
	return x_new


def runge_kutta_4_x_new(x_prev, t_prev, A, B, r, T):
	m1, m2, m3, m4 = calculate_ms(A, B, r, x_prev, t_prev, T)
	x_new = x_prev + T / 6.0 * (m1 + 2 * m2 + 2 * m3 + m4)	
	return x_new


def pece_x_new(x_prev, t_prev, A, B, r, T):
	x_new_0 = x_prev + T * x_dot(x_prev, A, B, r, t_prev)
	x_new = x_prev + 0.5 * T * (x_dot(x_prev, A, B, r, t_prev) + x_dot(x_new_0, A, B, r, t_prev + T))	
	return x_new


def pece2_x_new(x_prev, t_prev, A, B, r, T):
	x_new_0 = x_prev + T * x_dot(x_prev, A, B, r, t_prev)
	x_new_1 = x_prev + T * x_dot(x_new_0, A, B, r, t_prev + T)
	x_new = x_prev + T * x_dot(x_new_1, A, B, r, t_prev + T)
	return x_new


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


def analytic(t, x0=None):
	return Matrica([[x0[0][0] * cos(t) + x0[1][0] * sin(t)], [x0[1][0] * cos(t) - x0[0][0] * sin(t)]])


def plot_xs(ts, xs, title=None):
	x1s = [xs[i][0][0] for i in range(len(xs))]
	x2s = [xs[i][1][0] for i in range(len(xs))]

	x1s = x1s[0:len(ts)]
	x2s = x2s[0:len(ts)]

	plt.plot(ts, x1s)
	plt.plot(ts, x2s)
	if title is not None:
		plt.title(title)

	plt.show()

