from eval import eval
from parse import tokenize, parse
from impl_types import Exp, List

import cmd

class ReplParser(cmd.Cmd):
    prompt = '> '
    def default(self, line):
        tokens = tokenize(line)
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


if __name__ == "__main__":
    ReplParser().cmdloop()
