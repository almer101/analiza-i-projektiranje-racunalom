class A:
	def __init__(self):
		self.value = 3
		print("A")

class B(A):
	def __init__(self):
		print("B")

class C(A):
	def __init__(self):
		super().__init__()
		print(self.value)
		print("C")
		self.value = 5
		print(self.value)

C()