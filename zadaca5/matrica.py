import numpy as np

class Matrica:

	def __init__(self, mat):
		self.mat = mat

	def get(self, i,j):
		return self.mat[i][j]

	def set(self, i, j, value):
		self.mat[i][j] = value

	def __getitem__(self, index):
		return self.mat[index]

	def __setitem__(self, index, value):
		self.mat[index] = value

	def __len__(self):
		return len(self.mat)

	def __str__(self):
		s = ""
		for i in range(len(self.mat)):
			for j in range(len(self.mat[i])):
				s += str(self.mat[i][j]) + "   "
			s += "\n"
		return s

	def __eq__(self, other):
		if (len(self.mat) != len(other)) or (len(self.mat[0]) != len(other[0])):
			return False
		for i in range(len(self.mat)):
			for j in range(len(self.mat[i])):
				if self.mat[i][j] != other[i][j]: return False

		return True

	def __add__(self, other):
		if (len(self.mat) != len(other)) or (len(self.mat[0]) != len(other[0])):
			print("Cannot add")
			return

		res = []
		for i in range(len(self.mat)):
			res.append([])
			for j in range(len(self.mat[i])):
				res[i].append(self.mat[i][j] + other[i][j])

		return Matrica(res)

	def __sub__(self, other):
		if (len(self.mat) != len(other)) or (len(self.mat[0]) != len(other[0])):
			print("Cannot sub")
			return

		res = []
		for i in range(len(self.mat)):
			res.append([])
			for j in range(len(self.mat[i])):
				res[i].append(self.mat[i][j] - other[i][j])

		return Matrica(res)

	def transpose(self):
		new = []
		for i in range(len(self.mat[0])):
			new.append([])
			for j in range(len(self.mat)):
				new[i].append(self.mat[j][i])

		self.mat = new

	def matmul(a, b):
		if len(a[0]) != len(b):
			print("Cannot do matmul")
			return None

		new = []
		for i in range(len(a)):
			new.append([])
			for j in range(len(b[0])):
				suma = 0
				for k in range(len(b)):
					suma += a[i][k] * b[k][j]
				new[i].append(suma)

		return Matrica(new)

	def __mul__(self, other):
		return self.mul(other)

	def __rmul__(self, other):
		return self.mul(other)

	def mul(self, other):
		res = []
		for i in range(len(self.mat)):
			res.append([])
			for j in range(len(self.mat[i])):
				res[i].append(self.mat[i][j] * other)
		return Matrica(res)

	def copy(self):
		new = []
		for i in range(len(self.mat)):
			new.append([])
			for j in range(len(self.mat[i])):
				new[i].append(self.mat[i][j])

		newMat = Matrica(new)
		return newMat

	def printToFile(self, file):
		f = open(file, 'w')
		for i in range(len(self.mat)):
			s = ""
			for j in range(len(self.mat[i])):
				s += str(self.mat[i][j])
				if j != len(self.mat[i]) - 1:
					s += " "
			s += "\n"
			f.write(s)

def linesFromFile(file):
	f = open(file, "r")
	l = f.read()
	l = l.split("\n")
	lines = []
	for i in range(len(l)):
		if l[i].strip():
			lines.append(l[i])
	return lines

def matrixFromFile(file):
	lines = linesFromFile(file)
	mat = []

	for i in range(len(lines)):
		line = lines[i]
		stringValues = line.split()
		mat.append([])	
		for value in stringValues:
			mat[i].append(float(value))

	return Matrica(mat)
	#return np.array(mat)	

def equals(a, b):	
	if a.shape != b.shape: return False
	for i in range(len(a)):
		for j in range(len(b)):
			if a[i][j] != b[i][j]: return False

	return True

def equalsZero(value):
	return abs(value) < 1e-06

def forwardSupstitution(L, b):
	for i in range(len(b)):
		for j in range(i):
			b[i][0] -= L[i][j] * b[j][0]

def backwardSupstitution(U, y):
	for i in range(len(y) - 1, -1, -1):
		for j in range(i + 1, len(U)):
			y[i][0] -= U[i][j] * y[j][0]
		y[i][0] /= U[i][i]

def luDecomposition(A):
	for i in range(len(A) - 1):
		for j in range(i + 1, len(A)):
			if equalsZero(A[i][i]):
				print("Zero appeared on the main diagonal - LU decomposition failed!")
				return False

			A[j][i] /= A[i][i]
			for k in range(i + 1, len(A)):
				A[j][k] -= A[j][i] * A[i][k]

	for i in range(len(A)):
		if abs(A[i][i]) < 1e-06:
			print("Matrix must not contain 0 (zero) on the main diagonal!")
			return False
	
	return True

def lupDecomposition(A):
	P = []
	counter = 0
	for i in range(len(A)):
		P.append(i)

	for i in range(len(A) - 1):
		# swap the rows
		pivotIndex = findPivotInColumnWithIndex(A, i)
		counter += 1 if i != pivotIndex else 0
		P[i], P[pivotIndex] = P[pivotIndex], P[i]
		tmp = A[i].copy()
		A[i] = A[pivotIndex]
		A[pivotIndex] = tmp

		for j in range(i + 1, len(A)):
			if equalsZero(A[i][i]):
				print("Zero appeared on the main diagonal - LUP decomposition failed!")
				return None

			A[j][i] /= A[i][i]
			#print(A[j][i], "/=", A[i][i])
			for k in range(i + 1, len(A)):
				A[j][k] -= A[j][i] * A[i][k]

	# print("Number of permutations", counter)
	for i in range(len(A)):
		if abs(A[i][i]) < 1e-06:
			print("Zero appeared on the main diagonal - LUP decomposition failed!")
			return None

	return P, counter


def findPivotInColumnWithIndex(A, index):
	maxElement = abs(A[index][index])
	maxIndex = index
	for i in range(index, len(A)):
		if abs(A[i][index]) > maxElement:
			maxElement = abs(A[i][index])
			maxIndex = i

	return maxIndex 

def inverseOfMatrix(A):
	LU = A.copy()
	result = lupDecomposition(LU)

	if result is None:
		print("Inverse cannot be calculated")
		return None

	P, numberOfPermutations = result

	X = []

	for i in range(len(A)):
		e = []
		for j in range(len(A)):
			e.append([0.0])
		e = Matrica(e)
		for j in range(len(P)):
			if P[j] == i:
				e[j][0] = 1

		forwardSupstitution(LU, e)
		backwardSupstitution(LU, e)
		
		a = []
		for j in range(len(e)):
			a.append(e[j][0])
		X.append(a)

	X = Matrica(X)
	X.transpose()
	# print(X)
	return X

def determinantOfMatrix(A):
	result = lupDecomposition(A)
	if result is not None:
		P, numberOfPermutations = result
		det = determinantOfMatrixWithComponents(A, numberOfPermutations)
		return det
	return None

def determinantOfMatrixWithComponents(LU, numberOfPermutations):
	product = 1
	for i in range(len(LU)):
		product *= LU[i][i]
	return product if numberOfPermutations % 2 == 0 else -product


if __name__ == "__main__":
	mat = Matrica([[1,2,3],[4,5,6],[7,8,9]])
	mat1 = mat.copy()

	c = mat + mat1
	
	a = Matrica([[1,2], [3,4]])
	b = Matrica([[5,6,3,3], [3,2,4,1]])

	print(Matrica.matmul(a,b))

	print(mat)
	tmp = mat[0].copy()
	mat[0] = mat[1]
	mat[1] = tmp
	print(mat)

	mat.printToFile("mat.txt")



