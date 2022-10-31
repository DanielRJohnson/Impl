from repl import ReplParser
from eval import eval
from parse import tokenize, parse

import sys

if __name__ == "__main__":
    if len(sys.argv) == 1:
        ReplParser().cmdloop()
    elif len(sys.argv) == 2:
        try:
            with open(sys.argv[1], "r") as f:
                prog_str = str(f.read())
                eval(parse(tokenize(prog_str)))
        except FileNotFoundError:
            print("Input file could not be found")
    else:
        print("usage: impl <filename?>")
