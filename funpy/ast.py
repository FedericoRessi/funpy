from abc import abstractmethod, ABCMeta
from collections import namedtuple, OrderedDict
from inspect import formatargspec, getargspec, getcallargs
import logging

from six import add_metaclass


LOG = logging.getLogger(__name__)


class ASTMeta(ABCMeta):

    classes = OrderedDict()

    def __new__(mcs, name, bases, members):
        class_name = members.get('class_name')
        cls = ABCMeta.__new__(mcs, name, bases, members)
        if class_name:
            mcs.classes[class_name] = cls
        LOG.debug('Ast class registered: %r -> %r', class_name, cls)
        return cls


class ASTInjector(object):

    def inject(self, class_name, *args, **kwargs):
        # TODO: implement singleton injection
        return self._inject_method(class_name)(*args, **kwargs)

    __call__ = inject

    _methods = OrderedDict()
    _meta = ASTMeta

    @classmethod
    def ast_class(cls, class_name):
        try:
            return cls._meta.classes[class_name]
        except KeyError:
            raise AttributeError(
                'Invalid AST class name: {!r}.'.format(class_name))

    def _inject_method(self, class_name):
        try:
            return self._methods[class_name]

        except KeyError:
            cls = self.ast_class(class_name)

            def method(*args, **kwargs):
                return cls(self, *args, **kwargs)

            method.__name__ = class_name
            self._methods[class_name] = method
            return method

    __getattr__ = _inject_method


ast = ASTInjector()


@add_metaclass(ASTMeta)
class ASTBase(object):

    class_name = None

    @abstractmethod
    def make_params(self, *args, **kwargs):
        raise NotImplementedError

    def __init__(self, inject, *args, **kwargs):
        self.inject = inject
        self.params = self.make_params(*args, **kwargs)

    def __add__(self, other):
        return self.inject('add', self, other)

    def __radd__(self, other):
        return self.inject('add', other, self)

    def __repr__(self):
        return '{class_name}({params})'.format(
            class_name=self.class_name,
            params=', '.join(repr(p) for p in self.params))

    def set_params(self, *params):
        if params == self.params:
            return self
        else:
            return self.inject(self.class_name, *params)

    def append_param(self, other):
        return self.inject(self.class_name, *(self.params + (other,)))

    def prepend_param(self, other):
        return self.inject(self.class_name, *((other,) + self.params))

    def set_vars(self, values):
        return self.set_params(*[p.set_vars(values) for p in self.params])

    def __eq__(self, other):
        return (
            self.class_name == getattr(other, 'class_name', None) and
            self.params == getattr(other, 'params', None)
        )


_UNDEFINED_PARAM = object()


def make_tuple_function(_callable, class_name='nametuple', exclude=None):
    spec = getargspec(_callable)
    if spec.varargs or spec.keywords:
        raise TypeError(
            'Invalid signatores in {!r}, '
            'found varargs or keywords'.format(_callable))

    tuple_args = spec.args
    tuple_defaults = spec.defaults
    if exclude:
        # Eventually exclude some parameters
        tuple_args = [a for a in tuple_args if a not in exclude]
        if tuple_defaults:
            # Eventually exclude some default value
            tuple_defaults = [
                d
                for d, a in zip(spec.defaults, spec.args[-len(tuple_args):])
                if a not in exclude]

    # skip self parameter
    tuple_class = namedtuple(class_name, tuple_args)
    function_name = getattr(_callable, '__name__', class_name.lower())
    function_code = (
        'def {function_name}{signature}: return __make_tuple__({tuple_args})'.
        format(
            function_name=function_name,
            signature=formatargspec(args=spec.args, defaults=spec.defaults),
            tuple_args=', '.join(tuple_args)))

    LOG.debug(
        "Generated function code:\n"
        "%s", function_code)

    exec_scope = {'__make_tuple__': tuple_class}
    exec(function_code, exec_scope)
    return exec_scope[function_name]


def make_tuple_method(method):
    return  make_tuple_function(method, exclude='self')


class Var(ASTBase):
    """
    """

    class_name = 'var'

    @make_tuple_method
    def make_params(self, name):
        pass

    def set_vars(self, values):
        name = self.params.name
        try:
            return self.set_params(name, values[name])
        except KeyError:
            return self


var = ast.var


class Array(ASTBase):
    """
    """

    class_name = 'arr'

    @make_tuple_method
    def make_params(self, value):
        pass


arr = ast.arr


class Add(ASTBase):

    class_name = 'add'

    def make_params(self, *args):
        return args

    def __add__(self, other):
        # optimize chain of additions with one single operation
        return self.append_param(other)

    def __radd__(self, other):
        # optimize chain of additions with one single operation
        return self.prepend_param(other)

    def __repr__(self):
        return ' + '.join(repr(p) for p in self.params)


add = ast.add
