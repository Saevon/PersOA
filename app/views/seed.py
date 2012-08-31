from random import randint

class Seed(int):
	"""
	A random seed for randomizing
	same limits as an int
	"""

	INT_MIN = 0
	INT_MAX = 10

	def __init__(self, num=None):
		"""
		Creates a new seed, if no number is passed in then every new number generated
		isn't based on the previous
		"""
		if num is None:
			self.__algorithm = Seed._randint
		else:
			self.__algorithm = Seed._new
			self.__val == num
	
	def __call__(self):
		"""
		Returns the current seed and generates a new one
		"""
		seed = self.__val
		self.__val = self.__algorithm(seed)

		return seed

	def _new(self, seed):
		"""
		Creates a new seed based on the given value
		"""
		return NotImplemented

	def _randint(self, seed):
		"""
		Creates a new seed using random.randint
		"""
		return randint(Seed.INT_MIN, Seed.INT_MAX)