import numpy as np

class Vector2D:
	def __init__(self, x, y):
		self.x = x
		self.y = y 
	def __add__(self, other):
		return Vector2D(self.x + other.x, self.y + other.y)
	def __sub__(self, other):
		return Vector2D(self.x - other.x, self.y - other.y)
	def __mul__(self, other):
		if np.isscalar(other):
			return Vector2D(self.x * other, self.y * other)
		elif isinstance(other, Vector2D):
			return Vector2D(self.x * other.x, self.y * other.y)
		else:
			raise ("Multiplication not implemented for defined argument type")
	def __eq__(self, other):
		if (self.x == other.x) and (self.y == other.y):
			return True
		else:
			return False
	def __str__(self):
		return f"x:{self.x}, y:{self.y}"
	def toInt(self):
		return Vector2D(int(self.x), int(self.y))

class Point2D:
	def __init__(self, x, y):
		self.x = x
		self.y = y 
	def __sub__(self, other):
		return Vector2D(self.x - other.x, self.y - other.y)
	def __add__(self, other: "Vector2D"):
		if isinstance(other, Vector2D):
			return Point2D(self.x + other.x, self.y + other.y)
		else:
			raise ("Point can be added to only vector")
	def __eq__(self, other):
		if (self.x == other.x) and (self.y == other.y):
			return True
		else:
			return False
	def __str__(self):
		return f"x:{self.x}, y:{self.y}"		
	
	def __le__(self, other):
		if (self.x == other.x) and (self.y == other.y):
			return True
		else:
			return False	