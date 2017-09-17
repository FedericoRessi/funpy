import pytest

from funpy import ast, var
from funpy.ast import ASTBase, make_tuple_method


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


def test_ast_make_params_with_varargs():

    with pytest.raises(TypeError):

        class SomeAST(ASTBase):

            class_name = 'some'

            @make_tuple_method
            def make_params(self, *args):
                pass


def test_ast_make_params_with_kwargs():

    with pytest.raises(TypeError):

        class SomeAST(ASTBase):

            class_name = 'some'

            @make_tuple_method
            def make_params(self, a, **othres):
                pass


def test_ast_make_params_with_defaults():

    class SomeAST(ASTBase):

        class_name = 'some'

        @make_tuple_method
        def make_params(self, x, y=0, z=0):
            pass

    assert ast.some(10) == ast.some(10, 0)
