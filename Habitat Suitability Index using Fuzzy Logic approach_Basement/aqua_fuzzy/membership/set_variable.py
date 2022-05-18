import numpy as np


class SetFuzzyLogic:
    """
    Made by Yomer Cisneros Aguirre.
    """
    _adjust: int = 5

    def __init__(self, name, minimum, maximum, samples):

        self._name = name
        self._min = minimum
        self._max = maximum
        self._samples = samples

        self._space = np.linspace(minimum, maximum, samples)
        self._sp = np.zeros(self._space.shape)

    def __getitem__(self, x_value):
        return self._sp[np.abs(self._space - x_value).argmin()]

    def __setitem__(self, x_value, dom):
        self._sp[np.abs(self._space - x_value).argmin()] =\
            round(dom, self._adjust)

    @property
    def name(self):
        return self._name

    @classmethod
    def make_trapezoid(cls, name, min, max, samples, w, x, y, z):
        """
        Create trapezoids for antecedent and consequent membership functions.
        Parameters
        ----------
        :name: str, specify the name if the variable
        :min: float, minimum or starting value of universe membership function
        :max: float, maximum or ending value of universe membership function
        :samples: int, number of equally spaced samples in the interval
        :w, x, y, z: float, elements of trapezoids (a <= b <= c <= d)

        :Return: 1D array, trapezoidal membership function
        -------
        """
        universe = cls(name, min, max, samples)

        with np.errstate(divide='ignore', invalid='ignore'):
            try:
                universe._sp = np.round(np.minimum(np.maximum(np.minimum(
                    (universe._space - w) / (x - w),
                    (z - universe._space) / (z - y)), 0), 1),
                    universe._adjust)
            except FloatingPointError:
                pass

        return universe

    def domain_elements(self):
        return self._space

    def dom_elements(self):
        return self._sp
