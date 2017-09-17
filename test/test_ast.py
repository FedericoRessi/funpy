import pytest

from funpy import ast, var
from funpy.ast import ASTBase


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


def test_reverse_add_of_add():

    y = 1 + (var('x') + var('y'))

    assert y.params == (1, var('x'), var('y'))
    assert y == ast('add', 1, var('x'), var('y'))
    assert repr(y) == "1 + var('x') + var('y')"


def test_ast_init_is_callable():

    with pytest.raises(TypeError):

        class SomeAST(ASTBase):

            class_name = 'some'

            __init__ = 1


def test_ast_init_with_varargs():

    with pytest.raises(TypeError):

        class SomeAST(ASTBase):

            class_name = 'some'

            def __init__(self, a, *othres):
                pass


def test_ast_init_with_kwargs():

    with pytest.raises(TypeError):

        class SomeAST(ASTBase):

            class_name = 'some'

            def __init__(self, a, **othres):
                pass


def test_ast_init_with_defaults():

    class SomeAST(ASTBase):

        class_name = 'some'

        def __init__(self, x, y=0, z=0):
            pass

    assert ast.some(10) == ast.some(10, 0)
