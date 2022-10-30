from impl_types import Atom, Exp, Symbol, String, Boolean
import re


def tokenize_parse(program: str) -> Exp:
    """ Returns the input tokenized then parsed """
    return parse(tokenize(program))


def tokenize(program: str) -> list[str]:
    """ Tokenizes the input by splitting on whitespace """
    program = re.sub(";;.*\n", "", program+"\n")  # comments with ;;
    program = space_in_parens(program)
    # split on whitespace or string literal
    tokens = re.split("(\s|\"[^\"]*\")", program)
    tokens = filter_whitespace(tokens)
    return tokens


def space_in_parens(program: str) -> str:
    """ Pads space on the inside of opening and closing parens and quote """
    return program.replace("(", "( ").replace(")", " )").replace("\'", "\' ")


def filter_whitespace(tokens: list[str]) -> list[str]:
    """ Removes elements from a string list that only contain whitespace """
    return [token for token in tokens if token.strip() != ""]


def parse(tokens: list[str]) -> Exp:
    """ Parses a tokenized sexp to an 'ast' represented as an Exp """
    if len(tokens) == 0:
        raise SyntaxError("unexpected EOI")
    token = tokens.pop(0)
    if token == "(":
        sexp = []
        while len(tokens) != 0 and tokens[0] != ")":
            sexp.append(parse(tokens))
        try:
            tokens.pop(0)  # pop ")"
        except IndexError:
            raise SyntaxError("expected )")
        return sexp
    elif token == "'":  # '(1 2 3) => ["quote", [1, 2, 3]]
        items = []
        tokens.pop(0)
        while len(tokens) != 0 and tokens[0] != ")":
            items.append(parse(tokens))
        try:
            tokens.pop(0)  # pop ")"
        except IndexError:
            raise SyntaxError("expected )")
        return ["quote", items]
    elif token == ")":
        raise SyntaxError("unexpected )")
    else:
        return atom(token)


def atom(token: str) -> Atom:
    """ Converts a token to its Atomic representation """
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            pass

    if token[0] == "\"" and token[-1] == "\"":
        return String(token[1:-1])  # chop off quotes
    elif token == "True":
        return Boolean(True)
    elif token == "False":
        return Boolean(False)
    else:
        return Symbol(token)
