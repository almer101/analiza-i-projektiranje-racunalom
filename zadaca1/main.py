from matrica import *

def LUThenLUP(A, b):
	ACopy = A.copy()
	bCopy = b.copy()

	if solveWithLU(A, b):
		print(b)
	else:
		A = ACopy
		b = bCopy
		result = lupDecomposition(A)
		if result is not None:
			print("LUP Succeeded")
			P, numberOfPermutations = result
			tmp = []
			for i in range(len(b)):
				tmp.append(b[P[i]])
			#b = np.array(tmp)
			b = Matrica(tmp)

			forwardSupstitution(A, b)
			backwardSupstitution(A, b)
			print(b)

def solveWithLU(A, b):
	success = luDecomposition(A)
	if success:
		forwardSupstitution(A,b)
		backwardSupstitution(A,b)
	return success

def solveWithLUP(A, b):
	result = lupDecomposition(A)
	if result is not None:
		print("LUP Succeeded")
		P, numberOfPermutations = result
		tmp = []
		for i in range(len(b)):
			tmp.append(b[P[i]])
		bla = np.array(tmp)
		for i in range(len(bla)):
			b[i] = bla[i]

		forwardSupstitution(A, b)
		backwardSupstitution(A, b)
	return result is not None

# 1. zadatak
print("============1. zadatak==============")
A = matrixFromFile("A.txt")
print(A)

B = A.copy()
B *= 4.5678
B *= 1.0 / 4.5678

print(A - B)

# 2. zadatak
print("============2. zadatak==============")
A = matrixFromFile("A2.txt")
b = Matrica([[12.0],[12.0],[1.0]])

LUThenLUP(A, b)

#3. zadatak
print("============3. zadatak==============")
A = matrixFromFile("A3.txt")
b = Matrica([[4.0],[6.0],[8.0]])

LUThenLUP(A, b)

#4. zadatak
print("============4. zadatak==============")
A = matrixFromFile("A4.txt")
b = Matrica([[12000000.000001],[14000000],[10000000]])

ACopy = A.copy()
bCopy = b.copy()
success = luDecomposition(A)
if success:
	forwardSupstitution(A,b)
	backwardSupstitution(A,b)
	print(b)

A = ACopy
b = bCopy
if solveWithLUP(A, b):
	print(b)

#5. zadatak
print("============5. zadatak==============")
A = matrixFromFile("A5.txt")
b = Matrica([[6.0],[9.0],[3.0]])

if solveWithLUP(A, b):
	print(b)


#6. zadatak
print("============6. zadatak==============")
A = matrixFromFile("A6.txt")
b = Matrica([[9000000000],[15.0],[0.0000000015]])
	
for i in range(len(A[0])):
	A[0][i] *= 1.0 / 1000000000
b[0][0] *= 1.0 / 1000000000

for i in range(len(A[2])):
	A[2][i] *= 10000000000
b[2][0] *= 10000000000

if solveWithLU(A, b):
	print(b)

#7. zadatak
print("============7. zadatak==============")
A = matrixFromFile("A7.txt")
inv = inverseOfMatrix(A)

#8. zadatak
print("============8. zadatak==============")
A = matrixFromFile("A8.txt")
inv = inverseOfMatrix(A)

#9. zadatak
print("============9. zadatak==============")
A = matrixFromFile("A9.txt")
det = determinantOfMatrix(A)
if det is not None:
	print("Determinant is: ", det)


#10. zadatak
print("============10. zadatak==============")
A = matrixFromFile("A10.txt")
det = determinantOfMatrix(A)
if det is not None:
	print("Determinant is: ", det)
