import math
import operator as op
from typing import TypeVar
EnvType = TypeVar("Env")


class Env(dict):
    """ Env is a chained dictionary representing nested scopes """

    def __init__(self, keys=(), values=(), outer=None) -> None:
        self.update(zip(keys, values))
        self.outer = outer

    def find(self, var: str) -> EnvType:
        """
        Traverse out in scopes until the var is found.
        Then, return that Env.
        """
        return self if var in self else self.outer.find(var)


class StandardEnv(Env):
    """ An environment with a set of standard procedures """

    def __init__(self, keys=(), values=(), outer=None):
        #  defered import to avoid circular imports
        from impl_types import List, Symbol, Number
        super().__init__(keys, values, outer)
        self.update(vars(math))  # use math vars like pi, cos, sqrt, etc
        self.update({  # set of standard procedures
            '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
            '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
            'abs': abs,
            'append': op.add,
            'apply': lambda proc, args: proc(*args),
            'do': lambda *x: x[-1],
            'head': lambda x: x[0],
            'tail': lambda x: x[1:],
            'cons': lambda x, y: [x] + y,
            'eq?': op.is_,
            'pow': pow,
            'equal?': op.eq,
            'length': len,
            'list': lambda *x: List(x),
            'list?': lambda x: isinstance(x, List),
            'map': lambda f, x: list(map(f, x)),
            'filter': lambda f, x: list(filter(f, x)),
            'max': max,
            'min': min,
            'not': op.not_,
            'null?': lambda x: x == [],
            'number?': lambda x: isinstance(x, Number),
            'print': print,
            'procedure?': callable,
            'round': round,
            'symbol?': lambda x: isinstance(x, Symbol),
        })
