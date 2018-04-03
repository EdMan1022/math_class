import numpy

class MathClass(object):
	pass
	
	
class Integreater(MathClass):
	
	result = 0.
	
	def __init__(self, function, lower_bound: float, upper_bound: float, number_demarcations=1000):
		"""
		Base class for several classes that implement integration methods
		
		function: function to be integrated.
		upper_bound: (float) upper limit of integration input
		lower_bound: (float) lower limit of integration input
		number_demarcations: (int) number of integration demarcations
		"""
		
		self.function = function
		self.upper_bound = upper_bound
		self.lower_bound = lower_bound
		self.number_demarcations = number_demarcations
		
		# Derived attribute calculations
		self.range = self.upper_bound - self.lower_bound
		self.step_size = self.range / self.number_demarcations


class LeftRektAngles(Integreater):
	"""
	Subclass of integrator that uses the left side rectangle method
	"""
	
	def _calculate_bound(self, i):
		return self.lower_bound + (i * self.step_size)
	
	def integrate(self):
		"""
		Numerically estimates the integral value of the input function
		
		Uses the left side rectangle method,
		dividing the area under the curve into n rectangles,
		with height equivalent to the left hand side function value,
		and width equal to the step size
		
		Sums these rectangle values up to find the integral value
		"""
		
		for i in range(self.number_demarcations):
			bound = self._calculate_bound(i)
			rect_area = self.function(bound) * self.step_size
			
			self.result += rect_area
		

class RightRektAngles(LeftRektAngles):
		def _calculate_bound(self, i):
			return self.lower_bound + ((i + 1) * self.step_size)
		
class MiddleRektAngles(LeftRektAngles):
		def _calculate_bound(self, i):
			return self.lower_bound + ((i + .5) * self.step_size)


class ArrayIntegration(Integreater):
	"""
	Implements integration method by separating the integration range
	into a 1-dimensional array, composed of number_demarcations equally
	spaced values.
	
	The function is then applied to this array,
	which should be a fast operation thanks to numpy.
	This final array is then summed to get the integration result.
	"""
	
	_result_array = None
	
	def _init_result_array(self):
		"""
		Creates a linspace result array with number_demarcations between the bounds
		
		Move to super on class __init__
		"""
		self._result_array = numpy.linspace(self.lower_bound, self.upper_bound, self.number_demarcations)
	
	def _vectorize_function(self):
		"""
		Converts the function attribute to a numpy vectorized function
		"""
		self.function = numpy.vectorize(self.function)
	
	def integrate(self):
		
		self._init_result_array()
		self._vectorize_function()
		
		self._result_array = self.function(self._result_array)
		self.result = numpy.sum(self._result_array)


class ChunkArrayIntegration(ArrayIntegration):
	"""
	Implements the array integration method with chunking to prevent memory issues
	
	The chunk_size attribute defines the size of the arrays that the
	integration range is broken up into.
	
	if n = 1000 and chunk_size = 10,
	then an array of length 100 is formed of equally spaced values between the lower bound and upper_bound/10.
	The integral result is calculated for this range, and added to the total.
	This is repeated across the entire range for all chunks.
	"""
	
	_chunk_lower_bound = None
	_chunk_upper_bound = None
	_chunk_result_array= None
	_last_chunk_size = None
	
	def __init__(self, function, lower_bound: float, upper_bound: float, number_demarcations=10000, chunk_size=1000):
		
		super().__init__(function, lower_bound, upper_bound)
		self.chunk_size = chunk_size
		self._current_chunk = 0
		
		if self.chunk_size > self.number_demarcations:
			raise ValueError("Chunk size cannot be greater than the number of demarcations")
		
	
	def _set_n_chunks(self):
		"""
		Calculates how many chunks there are from the given chunk_size and n
		"""
		self._n_chunks = int(numpy.floor(self.number_demarcations / self.chunk_size))
		
		chunk_modulo = self.number_demarcations % self.chunk_size
		
		if chunk_modulo > 0:
			self._last_chunk_size = chunk_modulo
		pass
		
	def _set_chunk_bounds(self):
		"""
		Sets the lower and upper bounds for the current chunk
		"""
		
		self._chunk_lower_bound = self.lower_bound + self._current_chunk * self.chunk_size * self.step_size
		
		self._chunk_upper_bound = self.lower_bound + (self._current_chunk + 1) * self.chunk_size * self.step_size
		
	def _set_last_chunk_bounds(self):

		self._chunk_lower_bound = self.lower_bound + self._current_chunk * self.chunk_size * self.step_size
		
		self._chunk_upper_bound = self._chunk_lower_bound + self.last_chunk_size * self.step_size
		
	def _init_chunk_array(self):
		"""
		Creates an array for the current chunk
		"""
		self._chunk_array = numpy.linspace(self._chunk_lower_bound,
		self._chunk_upper_bound, self.chunk_size)
		
	def _init_last_chunk_array(self):
		self._chunk_array = numpy.linspace(self._chunk_lower_bound,
		self._chunk_upper_bound, self._last_chunk_size)
		
	def _calculate_chunk_integral(self, chunk_array):
		result_array = self.function(chunk_array)
		return numpy.sum(result_array)
		
		
	def integrate(self):
		"""
		Calculates the integral result for the given function and bounds
		"""
		self._vectorize_function()
		
		self._set_n_chunks()
		
		for chunk in range(self._n_chunks):
			self._current_chunk = chunk
			
			self._set_chunk_bounds()
			self._init_chunk_array()
			
			self.result += self._calculate_chunk_integral(self._chunk_array)
			
		if self._last_chunk_size:
			self._set_last_chunk_bounds()
			self._init_last_chunk_array()
			self.result += self_calculate_chunk_integral(self._chunk_array)

		