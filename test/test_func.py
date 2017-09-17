import numpy
from funpy import add, arr, func, var


def test_with_parameter():

    @func
    def my_func(x, y=2):
        return arr([1, 2, 3, 4]) + x + y

    assert my_func.ast == arr([1, 2, 3, 4]) + var('x') + var('y')
    assert my_func.ast == add(arr([1, 2, 3, 4]), var('x'), var('y'))
    assert repr(my_func) == (
        "def my_func(x, y=2): return arr([1, 2, 3, 4]) + var('x') + var('y')")
    # assert my_func(5) == numpy.arange(8, 12)
