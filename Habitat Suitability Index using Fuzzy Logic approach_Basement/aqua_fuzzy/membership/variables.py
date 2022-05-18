from .set_variable import SetFuzzyLogic
import matplotlib.pyplot as plt


class Variable:
    """
    Made by Diego Beramendi Ortega.
    """

    def __init__(self, name, min_value, max_value, resolution):
        """
        Creates a new universe variable of fuzzy logic.
        Parameters
        ----------
        :name: str, name fo the universe variable
        :min_value: float, minimum value of the universe variable
        :max_value: float, maximum value of the universe variable
        :resolution: int, resolution of the variable
        """
        self._sets = {}
        self._name = name
        self._max_val = max_value
        self._min_val = min_value
        self._resolution = resolution

    @property
    def name(self):
        return self._name

    def _add_set(self, name, sets):
        """
        Adds a fuzzy logic set to the variable
        Parameters
        ----------
        name: str, name of the set
        sets: Fuzzy set
        """
        self._sets[name] = sets

    def get_set(self, name):
        """
        Gets the set of variables.
        Parameters
        ----------
        :name: str, set the name of the variable

        :Return: fuzzy sets
        -------
        """
        return self._sets[name]

    def add_trapezoid(self, name, w, x, y, z):
        """
        Add the input and output trapezoidal membership functions.
        Parameters
        ----------
        :name: str, name of the variable
        :w, x, y, z: float, elements of trapezoids (a <= b <= c <= d)

        :Returns: 1D array, trapezoidal membership function
        -------
        """
        new_membership = SetFuzzyLogic.make_trapezoid(name,
                                                      self._min_val,
                                                      self._max_val,
                                                      self._resolution,
                                                      w, x, y, z)
        self._add_set(name, new_membership)
        return new_membership

    def plot_variable(self):
        """
        Visualize the antecedent and consequent membership functions.
        -------
        """
        ax = plt.subplot(111)

        for m, n in self._sets.items():
            ax.plot(n.domain_elements(), n.dom_elements(), label=m,
                    linestyle=(0, (5, 1)))

        ax.grid(True, which='both', alpha=0.4)
        ax.set_title(self._name)
        ax.set(xlabel='x', ylabel='$\mu(x)$')
        ax.legend(loc='upper right', bbox_to_anchor=(1, 0.5), fancybox=True)
        plt.show()
