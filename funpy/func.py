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
    variables = [ast.var(name)for name in spec.args]

    LOG.debug(
        "Extracted variables:\n"
        "  %s",
        '\n  '.join(repr(v) for v in variables))
    signature = formatargspec(args=spec.args, defaults=spec.defaults)
    return Func(
        name=_callable.__name__,
        ast=_callable(*variables),
        signature=signature,
        callable=_callable
    )


class Func(namedtuple('Func', ['name', 'ast', 'signature', 'callable'])):

    def __repr__(self):
        return 'def {name}{signature}: return {ast}'.format(
            name=self.name,
            signature=self.signature,
            ast=self.ast)

    def __call__(self, *args, **kwargs):
        args = getcallargs(self.callable, *args, **kwargs)
        raise NotImplementedError
        # return Func(self.ast.set_vars(args), self.signature)
