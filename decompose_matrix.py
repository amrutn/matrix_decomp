
class Z_sqrt_2_i:
	values = []
	def __init__(self, a, b, c, d, n):
		#values[0] = constant factor, values[1] = imaginary factor, values[2] = sqrt_factor, values[3] = imaginary and square root factor
		self.values = [a,b,c,d,n]


	def change_exponent(self, _exponent):
		if (_exponent > self.values[4]):
			raise Exception ("Cannot change n for 1/2^n in front of integer ring without breaking the integer property.")
		exponent_diff = -(self.values[4] - _exponent)
		self.values[4] = _exponent
		self.values[0] *= 2**exponent_diff
		self.values[1] *= 2**exponent_diff
		self.values[2] *= 2**exponent_diff
		self.values[3] *= 2**exponent_diff

	def add (self, ring2):
			if (self.values[4] > ring2.values[4]):
				self.change_exponent(ring2.values[4])
			else:
				ring2.change_exponent(self.values[4])
			self.values[0] = self.values[0] + ring2.values[0]
			self.values[1] = self.values[1] + ring2.values[1]
			self.values[2] = self.values[2] + ring2.values[2]
			self.values[3] = self.values[3] + ring2.values[3]
	def multiply_int(self, factor):
		self.values[0] *= factor
		self.values[1] *= factor
		self.values[2] *= factor
		self.values[3] *= factor
	def multiply(self, ring2):
		self.values[4] = self.values[4] + ring2.values[4]
		a0 = self.values[0]
		b0 = self.values[1]
		c0 = self.values[2]
		d0 = self.values[3]
		a1 = ring2.values[0]
		b1 = ring2.values[1]
		c1 = ring2.values[2]
		d1 = ring2.values[3]
		self.values[0] = (a0*a1 - b0*b1 + 2* c0 * c1 - 2 * d0 * d1)
		self.values[1] = (a0 * b1 + a1 * b0 + 2*c0*d1 + 2*c1*d0)
		self.values[2] = (a0*c1 + a1*c0 - b0 * d1 - b1 * d0)
		self.values[3] = (a0*d1 + a1*d0 + b0*c1 + b1*c0)

	def convert(self):
		return  D_w(self.values[3] - self.values[2], self.values[1], self.values[3] + self.values[2], self.values[0], self.values[4])

	def type(self):
		return "Ring of diadic? integers in i and sqrt 2"
class D_w:
	values = []
	def __init__(self, a, b, c, d, n):
		#const fctr = values[0], w factor = values[1] and so on.. fraction exponent = values[4]
		self.values = [d,c,b,a,n]
	

	def convert(self):
		return  Z_sqrt_2_i(self.values[0], self.values[2], (self.values[1] - self.values[3])/2, (self.values[1] + self.values[3])/2, self.values[4])
	

	def change_exponent(self, _exponent):
		if (_exponent > self.values[4]):
			raise Exception ("Cannot change n for 1/2^n in front of integer ring without breaking the integer property.")
		exponent_diff = -(self.values[4] - _exponent)
		self.values[4] = _exponent
		self.values[0] *= 2**exponent_diff
		self.values[1] *= 2**exponent_diff
		self.values[2] *= 2**exponent_diff
		self.values[3] *= 2**exponent_diff
	

	def add(self, ring2):
		if (self.values[4] > ring2.values[4]):
				self.change_exponent(ring2.values[4])
		else:
			ring2.change_exponent(self.values[4])
		self.values[0] += ring2.values[0]
		self.values[1] += ring2.values[1]
		self.values[2] += ring2.values[2]
		self.values[3] = ring2.values[3]

	def multiply_int(self, factor):
		self.values[0] *= factor
		self.values[1] *= factor
		self.values[2] *= factor
		self.values[3] *= factor

	def multiply(self, ring2):
		_ring1 = self.convert()
		_ring2 = ring2.convert()
		_ring1.multiply(_ring2)
		self = _ring1.convert()
	
	def reduce(self):
		canReduce = True
		while(canReduce):
			divisible_by_2 = True
			i = 0
			while i < len(self.values) - 1:
				if self.values[i] % 2 == 1:
					divisible_by_2 = False
				i += 1
			if divisible_by_2:
				self.values[4] -= 1
				i = 0
				while i < len(self.values) - 1:
					self.values[i] /= 2
					i += 1

			else:
				canReduce = False
				break;

	def residue(self):
		return Residue(self)

	def type(self):
		return "Ring of polynomials with the 8th roots of unity"

class Residue:
	self.residue_array = []
	def __init__ (value):
		self.residue_array = [value.values[3] % 2, value.values[2] % 2, value.values[1] % 2, value.values[0] % 2]

	def getBit(self, bitNum):
		return self.residue_array[bitNum]

	#Rotates bits in residue by numBits units to the left (imitates a T^n gate)
	def rotate(self, numBits):
		assert numBits < 4, "Rotating by too many bits"
		i = 0
		while i < numBits:
			temp[i] = self.residue_array[i]
			i += 1

		i = 0
		while i < len(residue_array) - numBits:
			self.residue_array[i] = residue_array[i + numBits]
			self.residue_array[i + numBits] = temp[i]
			i += 1


	def add (self, residue2):
		i = 0
		while i < len(self.residue_array):
			self.residue_array[i] += residue2.residue_array[i]
			self.residue_array[i] = self.residue_array[i] % 2
			i += 1

	def subtract(self, residue2):
		self.add(residue2)
	def mul_sqrt_2(self):
		if self.values[0] == 1:
			if self.values[1] == 1:
				if self.values[2] == 1:
					if self.values[3] == 1:
						self.values[0] = 0
						self.values[1] = 0
						self.values[2] = 0
						self.values[3] = 0
					else:
						self.values[0] = 1
						self.values[1] = 0
						self.values[2] = 1
						self.values[3] = 0
				else:
					if self.values[3] == 1:
						self.values[0] = 0
						self.values[1] = 1
						self.values[2] = 0
						self.values[3] = 1
					else:
						self.values[0] = 1
						self.values[1] = 1
						self.values[2] = 1
						self.values[3] = 1
			else:
				if self.values[2] == 1:
					if self.values[3] == 1:
						self.values[0] = 1
						self.values[1] = 0
						self.values[2] = 1
						self.values[3] = 0
					else:
						self.values[0] = 0
						self.values[1] = 0
						self.values[2] = 0
						self.values[3] = 0
				else:
					if self.values[3] == 1:
						self.values[0] = 1
						self.values[1] = 1
						self.values[2] = 1
						self.values[3] = 1
					else:
						self.values[0] = 0
						self.values[1] = 1
						self.values[2] = 0
						self.values[3] = 1

		else:
			if self.values[1] == 1:
				if self.values[2] == 1:
					if self.values[3] == 1:
						self.values[0] = 0
						self.values[1] = 1
						self.values[2] = 0
						self.values[3] = 1
					else:
						self.values[0] = 1
						self.values[1] = 1
						self.values[2] = 1
						self.values[3] = 1
				else:
					if self.values[3] == 1:
						self.values[0] = 0
						self.values[1] = 0
						self.values[2] = 0
						self.values[3] = 0
					else:
						self.values[0] = 1
						self.values[1] = 0
						self.values[2] = 1
						self.values[3] = 0
			else:
				if self.values[2] == 1:
					if self.values[3] == 1:
						self.values[0] = 1
						self.values[1] = 1
						self.values[2] = 1
						self.values[3] = 1
					else:
						self.values[0] = 0
						self.values[1] = 1
						self.values[2] = 0
						self.values[3] = 1
				else:
					if self.values[3] == 1:
						self.values[0] = 1
						self.values[1] = 0
						self.values[2] = 1
						self.values[3] = 0
					else:
						self.values[0] = 0
						self.values[1] = 0
						self.values[2] = 0
						self.values[3] = 0

	def norm(self):
		vals = []
		if self.values[0] == 1:
			if self.values[1] == 1:
				if self.values[2] == 1:
					if self.values[3] == 1:
						vals[0] = 0
						vals[1] = 0
						vals[2] = 0
						vals[3] = 0
					else:
						vals[0] = 0
						vals[1] = 0
						vals[2] = 0
						vals[3] = 1
				else:
					if self.values[3] == 1:
						vals[0] = 0
						vals[1] = 0
						vals[2] = 0
						vals[3] = 1
					else:
						vals[0] = 1
						vals[1] = 0
						vals[2] = 1
						vals[3] = 0
			else:
				if self.values[2] == 1:
					if self.values[3] == 1:
						vals[0] = 0
						vals[1] = 0
						vals[2] = 0
						vals[3] = 1
					else:
						vals[0] = 0
						vals[1] = 0
						vals[2] = 0
						vals[3] = 0
				else:
					if self.values[3] == 1:
						vals[0] = 1
						vals[1] = 0
						vals[2] = 1
						vals[3] = 0
					else:
						vals[0] = 0
						vals[1] = 0
						vals[2] = 0
						vals[3] = 1

		else:
			if self.values[1] == 1:
				if self.values[2] == 1:
					if self.values[3] == 1:
						vals[0] = 0
						vals[1] = 0
						vals[2] = 0
						vals[3] = 1
					else:
						vals[0] = 1
						vals[1] = 0
						vals[2] = 1
						vals[3] = 0
				else:
					if self.values[3] == 1:
						vals[0] = 0
						vals[1] = 0
						vals[2] = 0
						vals[3] = 0
					else:
						vals[0] = 0
						vals[1] = 0
						vals[2] = 0
						vals[3] = 1
			else:
				if self.values[2] == 1:
					if self.values[3] == 1:
						vals[0] = 1
						vals[1] = 0
						vals[2] = 1
						vals[3] = 0
					else:
						vals[0] = 0
						vals[1] = 0
						vals[2] = 0
						vals[3] = 1
				else:
					if self.values[3] == 1:
						vals[0] = 0
						vals[1] = 0
						vals[2] = 0
						vals[3] = 1
					else:
						vals[0] = 0
						vals[1] = 0
						vals[2] = 0
						vals[3] = 0		
		return Residue(vals)
	def equals(self, res2):
		return (self.residue_array[0] == res2.residue_array[0]) && (self.residue_array[1] == res2.residue_array[1]) && (self.residue_array[2] == res2.residue_array[2]) && (self.residue_array[3] == res2.residue_array[3])
class Matrix:
	#k is the 1/sqrt(2)^k factor in front of the matrix given.
	def __init__ (arr, k):
		self.matrix_array = arr
		self.exp = k
		max_exp = 0
		for row in self.matrix_array:
			for element in row:
				if element.type() == "Ring of diadic? integers in i and sqrt 2":
					element.convert()
					element.reduce()
					if element.values[4] > max_exp:
						max_exp = element.values[4]
		for row in self.matrix_array:
			for element in row:
				element.change_exponent(max_exp)
		self.values = matrix_array
		self.exp += max_exp * 2 
	def createResidue(self):
		residue_array = []
		for row in self.matrix_array:
			residue_row = []
			for element in row:
				residue_row += [element.residue()]
			residue_array += [residue_row]
		return Residue_Matrix(residue_array)
	def k_res(self, k):
		if (k < self.exp):
			raise Exception ("Cannot take residue of matrix with a 1/sqrt(2) factor")
		else if (k == self.exp):
			return self.createResidue()
		else if (k == self.exp + 1):
			res = self.createResidue()
			res_arr = res.residue_array
			for row in res_arr:
				for element in row:
					element = element.mul_sqrt_2()
			return Residue_Matrix(res_arr)
		else:
			res = self.createResidue()
			res_arr = res.residue_array
			for row in res_arr:
				for element in row:
					element = Residue([0,0,0,0])
			return Residue_Matrix(res_arr)
class Residue_Matrix:
	def __init__(matrix_array, exp):
		self.residue_array = matrix_array




#Tests

#For Z_sqrt_2_i

ring1 =  Z_sqrt_2_i(1, 2, 3, 4, 5)
ring2 =  Z_sqrt_2_i(2, 4, 6, 8, 6)
ring1.add(ring2)
ring2 = ring2.convert()
ring2.multiply_int(4)
ring2.reduce()
ring2 = ring2.convert()
print(ring2.values)









