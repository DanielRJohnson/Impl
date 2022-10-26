from env import Env, StandardEnv
from impl_types import Exp, List, Symbol, Procedure


def eval(x: Exp, env=StandardEnv()) -> Exp:
    """ Evaluate one expression in a given env """
    if isinstance(x, Symbol):
        return env.find(x)[x]
    elif not isinstance(x, List):
        return x

    op, *args = x
    if op == "quote":
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
    else:  # procedure call
        proc = eval(op, env)
        args = [eval(arg, env) for arg in args]
        return proc(*args)
