from impl_types import Atom, Exp, Symbol


def tokenize_parse(program: str) -> Exp:
    """ Returns the input tokenized then parsed """
    return parse(tokenize(program))


def tokenize(program: str) -> list[str]:
    """ Tokenizes the input by splitting on whitespace """
    return space_in_parens(program).split()


def space_in_parens(line: str) -> str:
    """ Pads space on the inside of opening and closing parens """
    return line.replace("(", "( ").replace(")", " )")


def parse(tokens: list[str]) -> Exp:
    """ Parses a tokenized sexp to an 'ast' represented as an Exp """
    if len(tokens) == 0:
        raise SyntaxError("unexpected EOI")
    token = tokens.pop(0)
    if token == "(":
        sexp = []
        while (tokens[0] != ")"):
            sexp.append(parse(tokens))
        tokens.pop(0)  # pop ")"
        return sexp
    elif token == ")":
        raise SyntaxError("unexpected )")
    else:
        return atom(token)


def atom(token: str) -> Atom:
    """ Converts a token to its Atomic representation """
    # todo, add other concrete types?
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)
