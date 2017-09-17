import pytest

from funpy import add, arr, func, var


def test_with_parameter():

    @func
    def my_func(x, y=2):
        return arr([1, 2, 3, 4]) + x + y

    assert my_func.ast == arr([1, 2, 3, 4]) + var('x') + var('y')
    assert my_func.ast == add(arr([1, 2, 3, 4]), var('x'), var('y'))
    assert repr(my_func) == (
        "def my_func(x, y=2): return arr([1, 2, 3, 4]) + var('x') + var('y')")

    with pytest.raises(NotImplementedError):
        my_func(5)

    # assert my_func(5) == numpy.arange(8, 12)


def test_without_callable():
    with pytest.raises(TypeError):
        func(1)


def test_with_varargs_callable():
    with pytest.raises(TypeError):
        @func
        def my_func(a, b, *others):
            return a + b + sum(others)


def test_with_kwargs_callable():
    with pytest.raises(TypeError):

        @func
        def my_func(a, b, **kwargs):
            return a + b
