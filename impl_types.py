from dataclasses import dataclass
from env import Env
List = list
Number = (int, float)
String = str
Boolean = bool


class String(str):
    def is_symbol(self):
        return False


class Symbol(str):
    def is_symbol(self):
        return True


class Keyword(str):
    def is_symbol(self):
        return False


Atom = (Number, Symbol)
Exp = (Atom, List)


@dataclass
class Procedure():
    formals: List
    body: Exp
    env: Env

    def __call__(self, *args):
        from eval import eval  # defered import to avoid circular imports
        return eval(self.body, Env(self.formals, args, self.env))
