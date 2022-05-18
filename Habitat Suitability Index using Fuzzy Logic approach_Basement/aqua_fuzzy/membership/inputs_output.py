from .variables import Variable


class InputVariable(Variable):

	def __init__(self, name, min_value, max_value, resolution):
		Variable.__init__(self, name, min_value, max_value, resolution)


class OutputVariable(Variable):

	def __init__(self, name, min_value, max_value, resolution):
		Variable.__init__(self, name, min_value, max_value, resolution)
