# coding=utf-8
"""


"""

__author__ = 'soon'

from types import FunctionType
from random import random
from random import randint
from itertools import chain
from operator import itemgetter


class IntegralCalculatorGA:
    """

    Integrates a function in a given interval using the GA algorithm
    """

    def __init__(self, function=lambda: None, a=0, b=0):
        """

        :type function: FunctionType
        :param function: Function to integrate

        :type a: float
        :param a: The begin of the interval

        :type b: float
        :param b: The end of the interval
        """
        assert isinstance(function, FunctionType)
        assert isinstance(a, float) or isinstance(a, int)
        assert isinstance(b, float) or isinstance(b, int)

        self.f = function
        self.a = a
        self.b = b
        self.current_population = []
        self.number_of_parts = 0
        self.number_of_phenotypes = 0

    #region Methods

    def generate_initial_population(self, number_of_parts: int, number_of_phenotypes: int) -> list:
        """

        Generates initial population, stores in the current_population and returns it


        :type number_of_parts: int
        :param number_of_parts: The number of parts

        :type number_of_phenotypes: int
        :param number_of_phenotypes: The number of phenotypes in the population

        :return: The initial population
        :rtype : list

        """
        assert isinstance(number_of_parts, int)
        assert isinstance(number_of_phenotypes, int)

        self.number_of_parts = number_of_parts
        self.number_of_phenotypes = number_of_phenotypes

        len_of_part = (self.b - self.a) / number_of_parts

        generate_phenotype = lambda _: [(x + random()) * len_of_part + self.a for x in range(self.number_of_parts)]

        self.current_population = list(map(generate_phenotype, range(self.number_of_phenotypes)))

        return self.current_population

    def run_next_step(self) -> list:
        """

        Generates new population, sets it to the current_population and returns it
        """
        assert len(self.current_population) != 0
        assert len(self.current_population) == self.number_of_phenotypes

        make_tuple_with_fitness = lambda phenotype: (self.fitness(phenotype), phenotype)

        sorted_by_fitness = sorted(
            map(make_tuple_with_fitness, self.current_population),
            key=itemgetter(0))

        skip_number = self.number_of_phenotypes // 4

        best = sorted_by_fitness[skip_number:self.number_of_phenotypes - skip_number]

        while len(best) < self.number_of_phenotypes:
            best += map(make_tuple_with_fitness,
                        self._mutate_phenotypes(best[randint(0, len(best) - 1)][1],
                                                best[randint(0, len(best) - 1)][1]))

        sorted_by_fitness = sorted(
            chain(sorted_by_fitness[:skip_number],
                  sorted_by_fitness[:-skip_number],
                  best),
            key=itemgetter(0))

        first = (len(sorted_by_fitness) - self.number_of_phenotypes) // 2
        last = first + self.number_of_phenotypes

        self.current_population = list(map(itemgetter(1), sorted_by_fitness[first:last]))

        return self.current_population

    def fitness(self, phenotype: list) -> float:
        """

        :param phenotype:
        """
        assert isinstance(phenotype, list)
        assert self.number_of_parts != 0
        assert self.f is not None

        return sum(self.f(x) for x in phenotype) / self.number_of_parts

    #endregion Methods

    #region Properties

    @property
    def f(self) -> FunctionType:
        """

        :return: Function to integrate
        """
        return self._f

    @f.setter
    def f(self, value: FunctionType):
        """

        :type value: FunctionType
        :param value: Function to integrate
        """
        assert isinstance(value, FunctionType)

        self._f = value

    @property
    def a(self) -> float:
        """

        :return: The begin of the interval
        :rtype : float
        """
        return self._a

    @a.setter
    def a(self, value: float):
        """

        :type value: float
        :param value: The begin of the interval
        """
        assert isinstance(value, float) or isinstance(value, int)

        self._a = value

    @property
    def b(self) -> float:
        """

        :return: The end of the interval
        :rtype : float
        """
        return self._b

    @b.setter
    def b(self, value: float):
        """

        :type value: float
        :param value: The begin of the interval
        """
        assert isinstance(value, float) or isinstance(value, int)

        self._b = value

    @property
    def current_population(self) -> list:
        """

        :return: The current population
        :rtype : list
        """
        return self._current_population

    @current_population.setter
    def current_population(self, value: list):
        """

        :type value: list
        :param value: The current population
        """
        assert isinstance(value, list)

        self._current_population = value

    @property
    def number_of_parts(self) -> int:
        """


        ;return: The number of parts in the interval [a, b]
        :rtype : int
        """
        return self._number_of_parts

    @number_of_parts.setter
    def number_of_parts(self, value: int):
        """


        :type value: int
        :param value: The number of parts in the interval [a, b]
        """
        assert isinstance(value, int)

        self._number_of_parts = value

    @property
    def number_of_phenotypes(self) -> int:
        """

        :return: The number of phenotypes in the population
        :rtype : int
        """
        return self._number_of_phenotypes

    @number_of_phenotypes.setter
    def number_of_phenotypes(self, value: int):
        """

        :type value: int
        :param value: The number of phenotypes in the population
        """
        assert isinstance(value, int)

        self._number_of_phenotypes = value

    @property
    def midpoint(self) -> float:
        """

        :return: Midpoint from the current population
        """
        assert len(self.current_population) != 0

        sorted_by_fitness = sorted(map(self.fitness, self.current_population))

        return sorted_by_fitness[len(sorted_by_fitness) // 2]

    @property
    def integral(self) -> float:
        """


        """
        return (self.b - self.a) * self.midpoint

    #endregion Properties

    #region Private Methods

    @staticmethod
    def _mutate_phenotypes(phenotype_1: list, phenotype_2: list) -> list:
        """

        Mutates given phenotypes

        :param phenotype_1: First phenotype
        :type phenotype_1: list

        :param phenotype_2: Second phenotype
        :type phenotype_2: list

        :return: list of new phenotypes, mutated from given
        :rtype : list
        """
        assert isinstance(phenotype_1, list)
        assert isinstance(phenotype_2, list)
        assert len(phenotype_1) == len(phenotype_2)

        split_at = randint(0, len(phenotype_1) - 1)

        return [
            phenotype_1[:split_at] + phenotype_2[split_at:],
            phenotype_2[:split_at] + phenotype_1[split_at:]
        ]

    #endregion Private Methods