from collections import namedtuple
from inspect import getargspec, getcallargs, formatargspec
import logging

from funpy import ast
from funpy import compute


LOG = logging.getLogger(__name__)


def func(_callable):
    if not callable(_callable):
        raise TypeError(
            'Expected a function or a method, got {!r}'.format(
                _callable))

    spec = getargspec(_callable)
    if spec.varargs or spec.keywords:
        raise TypeError(
            'Invalid signatores in {!r}, found varargs or keywords'.format(
                _callable))

    LOG.debug(
        "Extract variables from function signature:\n"
        "  names=%r\n"
        "  values=%r",
        spec.args, spec.defaults)

    # variables without default values
    variables = (
        [ast.var(name)
         for name in _variables_without_values(spec.args, spec.defaults)] +
        [ast.var(name, value)
         for name, value in _variables_with_values(spec.args, spec.defaults)])
    LOG.debug(
        "Extracted variables:\n"
        "  %s",
        '\n  '.join(repr(v) for v in variables))
    # signature = formatargspec(args=spec.args, defaults=spec.defaults)
    return Func(_callable(*variables), _callable)


def _variables_without_values(names, values):
    if values:
        return names[:-len(values)]
    else:
        return names


def _variables_with_values(names, values):
    if values:
        return zip(names[-len(values):], values)
    else:
        return []


class Func(namedtuple('Func', ['ast', 'signature'])):

    def __repr__(self):
        return 'func({!r})'.format(self.ast)

    def __call__(self, *args, **kwargs):
        args = getcallargs(self.signature, *args, **kwargs)
        raise NotImplementedError
        # return Func(self.ast.set_vars(args), self.signature)
