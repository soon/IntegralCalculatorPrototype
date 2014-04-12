# coding=utf-8

__author__ = 'soon'

from calculator.IntegralCalculatorGA import IntegralCalculatorGA
from math import pi
from math import cos
from math import sin
from math import e

def main():
    alpha = 8

    function = lambda x: e * (x * e)
    a = -pi
    b = pi**(1/2)

    calculator = IntegralCalculatorGA(function, a, b)

    calculator.generate_initial_population(number_of_parts=100, number_of_phenotypes=50)

    while True:
        midpoint = calculator.midpoint

        print()
        print('Midpoint: {0}, F(Midpoint): {1}'.format(midpoint, function(midpoint)))
        print('Integral: {0}'.format(calculator.integral))
        input()

        calculator.run_next_step()

if __name__ == '__main__':
    main()