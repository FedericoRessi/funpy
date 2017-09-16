import numpy
from funpy import ast


def test_var():

    x = ast.var('x')

    assert x.params == ('x', None)
    assert x.params.name == 'x'
    assert x.params.value is None
    assert x == ast('var', 'x')
    assert repr(x) == "var('x', None)"
