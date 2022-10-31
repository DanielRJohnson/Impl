import cmd
import sys
from eval import eval
from parse import tokenize, parse
from impl_types import Exp, List


class ReplParser(cmd.Cmd):
    prompt = '> '

    def default(self, line):
        if line == "":
            return
        if line == "EOF":
            sys.exit(0)

        tokens = tokenize(line, is_multiexpr=False)
        print("Tokens:", tokens)
        ast = parse(tokens)
        print("Ast:", ast)
        val = eval(ast)
        if val is not None:
            print(format_value(val))


def format_value(val: Exp) -> str:
    if isinstance(val, List):
        return "(" + " ".join(map(format_value, val)) + ")"
    else:
        return str(val)
