from funpy import ast, var


def test_var():

    x = var('x')

    assert x.params == ('x',)
    assert x.params.name == 'x'
    assert x == ast('var', 'x')
    assert repr(x) == "var('x')"


def test_add():

    y = var('x') + 5

    assert y.params == (var('x'), 5)
    assert y == ast('add', var('x'), 5)
    assert repr(y) == "var('x') + 5"


def test_reverse_add():

    y = 1 + var('x')

    assert y.params == (1, var('x'))
    assert y == ast('add', 1, var('x'))
    assert repr(y) == "1 + var('x')"
