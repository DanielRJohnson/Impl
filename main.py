from eval import eval
from parse import tokenize_parse
from impl_types import Exp, List


def repl(prompt="> "):
    while True:
        val = eval(tokenize_parse(input(prompt)))
        if val is not None:
            print(format_value(val))


def format_value(val: Exp) -> str:
    if isinstance(val, List):
        return "(" + " ".join(map(format_value, val)) + ")"
    else:
        return str(val)


if __name__ == "__main__":
    repl()