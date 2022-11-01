import math
import random
import operator as op
from typing import Self
from PIL import Image


class Env(dict):
    """ Env is a chained dictionary representing nested scopes """

    def __init__(self, keys=(), values=(), outer=None) -> None:
        self.update(zip(keys, values))
        self.outer = outer
        self.images = []
        self.figures = []

    def find(self, var: str) -> Self:
        """
        Traverse out in scopes until the var is found.
        Then, return that Env.
        """
        return self if var in self else self.outer.find(var)

    def headfig(self) -> Image:
        assert len(self.images) > 0, "no figures exist"
        return self.figures[0]

    def newfig(self, figsize=None) -> None:
        if len(self.images) == 0:
            assert figsize != None, "figsize must be set if creating new figure"
            self.images.append(Image.new("RGB", figsize, (0, 0, 0, 255)))
        else:
            self.images.insert(0, self.images[0].copy())
        self.figures.insert(0, self.images[0].load())

    def savefigs(self, fn: str, dur=10) -> None:
        assert len(self.images) > 0, "no figures exist"
        if len(self.images) == 1:
            self.images[0].save(fn)
        else:
            chron_order = self.images[::-1]
            chron_order[0].save(fn, save_all=True, append_images=chron_order[1:],
                                optimize=False, duration=dur, loop=True)

    def imgwidth(self) -> int:
        assert len(self.images) > 0, "no figures exist"
        return self.images[0].width

    def imgheight(self) -> int:
        assert len(self.images) > 0, "no figures exist"
        return self.images[0].height


class StandardEnv(Env):
    """ An environment with a set of standard procedures """

    def __init__(self, keys=(), values=(), outer=None):
        #  defered import to avoid circular imports
        from impl_types import List, Symbol, Number
        super().__init__(keys, values, outer)
        self.update(vars(math))  # use math vars like pi, cos, sqrt, etc
        self.update(vars(random))  # use random vars like uniform, randint, etc
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
            'range': lambda *args: list(range(*args)),
            'nth': lambda n, l: l[n],
        })
