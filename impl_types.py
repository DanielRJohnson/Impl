from dataclasses import dataclass
from env import Env
Symbol = str
List = list
Number = (int, float)
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
