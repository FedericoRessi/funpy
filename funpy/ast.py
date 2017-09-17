from abc import abstractmethod, ABCMeta
from collections import namedtuple, OrderedDict
from inspect import formatargspec, getargspec, getcallargs
import logging

from six import add_metaclass, viewkeys


LOG = logging.getLogger(__name__)


class ASTMeta(ABCMeta):

    classes = OrderedDict()

    def __new__(mcs, name, bases, members):
        class_name = members['class_name']
        if class_name:
            init_method = members.get('__init__')
            if init_method:
                if not callable(init_method):
                    raise TypeError(
                        'Expected a callable, got {!r}'.format(init_method))

                spec = getargspec(init_method)
                if spec.varargs or spec.keywords:
                    raise TypeError(
                        'Invalid signatores in {!r}, '
                        'found varargs or keywords'.format(init_method))

                # skip self parameter
                params_cls = namedtuple(name + 'Params', spec.args[1:])
                if spec.defaults:
                    signature = formatargspec(
                        args=spec.args[1:],  # skip self parameter
                        defaults=spec.defaults)
                    LOG.debug(
                        "Extract variables from function signature:\n"
                        "  %r", signature)

                    scope = {}
                    exec('def method{}: pass'.format(signature), scope)
                    signature_method = scope['method']

                    def make_params(*args, **kwargs):
                        # LOG.debug('Make parameters:\n'
                        #           '  args: %r'
                        #           '  kwargs: %r'
                        #           '  signature: %r',
                        #           args, kwargs, signature)
                        return params_cls(
                            **getcallargs(signature_method, *args, **kwargs))

                else:
                    def make_params(*args, **kwargs):
                        return params_cls(*args, **kwargs)
            else:
                def make_params(*args):
                    return args

            def __init__(self, inject, *args, **kwargs):
                self.inject = inject
                self.params = make_params(*args, **kwargs)
                if init_method:
                    init_method(self, *args, **kwargs)

            members['__init__'] = __init__
            members['inject'] = None
            members['params'] = None

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

    @property
    @abstractmethod
    def params(self):
        raise NotImplementedError

    @abstractmethod
    def inject(self, name, *args, **kwargs):
        raise NotImplementedError

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
        return self.inject(self.class_name, *(other, self.params))

    def set_vars(self, values):
        return self.set_params(*[p.set_vars(values) for p in self.params])

    def __eq__(self, other):
        return (
            self.class_name == getattr(other, 'class_name', None) and
            self.params == getattr(other, 'params', None)
        )


class Var(ASTBase):
    """
    """

    class_name = 'var'

    def __init__(self, name):
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

    def __init__(self, value):
        pass


arr = ast.arr


class Add(ASTBase):

    class_name = 'add'

    def __add__(self, other):
        # optimize chain of additions with one single operation
        return self.append_param(other)


class Add(ASTBase):

    class_name = 'add'

    def __add__(self, other):
        # optimize chain of additions with one single operation
        return self.append_param(other)

    def __radd__(self, other):
        # optimize chain of additions with one single operation
        return self.prepend_param(other)

    def __radd__(self, other):
        # optimize chain of additions with one single operation
        return self.prepend_param(other)

    def __repr__(self):
        return ' + '.join(repr(p) for p in self.params)


add = ast.add
