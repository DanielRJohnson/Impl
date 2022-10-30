from env import Env, StandardEnv
from impl_types import Exp, List, Symbol, Procedure


def eval(x: Exp, env=StandardEnv()) -> Exp:
    """ Evaluate one expression in a given env """
    if isinstance(x, str) and x.is_symbol():
        try:
            return env.find(x)[x]
        except AttributeError:
            raise Exception(f"Symbol {x} is not set.")
    elif not isinstance(x, List):
        return x

    op, *args = x
    if op == "quote" or op == "'":
        return args[0]
    elif op == "if":
        (cond, tbranch, fbranch) = args
        chosen_branch = (tbranch if eval(cond, env) else fbranch)
        return eval(chosen_branch, env)
    elif op == "define":
        (sym, exp) = args
        env[sym] = eval(exp, env)
    elif op == "set!":
        (sym, exp) = args
        env.find(sym)[sym] = eval(exp, env)
    elif op == "lambda":
        (formals, body) = args
        return Procedure(formals, body, env)
    elif op == "let":  # (let ( (x 2) (y 3) ) (body)) = ((lambda (x y) (body)) 2 3)
        formals, actuals = zip(*(args[0]))  # unzip formals and actuals
        desugar = [["lambda", formals, args[1]], *actuals]
        return eval(desugar, env)
    else:  # procedure call
        proc = eval(op, env)
        args = [eval(arg, env) for arg in args]
        return proc(*args)
