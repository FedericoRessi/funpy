import numpy
from funpy import ast, func


def test_with_parameter():

    @func
    def my_func(x, y=2):
        return ast.arr([1, 2, 3, 4]) + x + y

    assert my_func.ast == (
        ast.arr([1, 2, 3, 4]) + ast.var('x') + ast.var('y', 2))
    assert my_func.ast == ast.add(
        ast.arr([1, 2, 3, 4]), ast.var('x'), ast.var('y', 2))
    # assert my_func(5) == numpy.arange(8, 12)
