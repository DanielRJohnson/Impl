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
    if op == "quote":
        assert len(args) == 1, "quote must have one argument"
        return args[0]
    elif op == "if":
        assert len(args) == 3, "if must have three arguments"
        (cond, tbranch, fbranch) = args
        chosen_branch = (tbranch if eval(cond, env) else fbranch)
        return eval(chosen_branch, env)
    elif op == "define":
        assert len(args) == 2, "define must have two arguments"
        (sym, exp) = args
        assert isinstance(sym, str) and sym.is_symbol(
        ), "define's first argument must be a symbol"
        env[sym] = eval(exp, env)
    elif op == "set!":
        assert len(args) == 2, "set! must have two arguments"
        (sym, exp) = args
        assert isinstance(sym, str) and sym.is_symbol(
        ), "set!'s first argument must be a symbol"
        env.find(sym)[sym] = eval(exp, env)
    elif op == "lambda":
        assert len(args) == 2, "lambda must have two arguments"
        (formals, body) = args
        for f in formals:
            assert isinstance(f, str) and f.is_symbol(
            ), "lambda's formals must be symbols"
        return Procedure(formals, body, env)
    elif op == "let":  # (let ((x 2) (y 3)) (body)) = ((lambda (x y) (body)) 2 3)
        assert len(args) == 2, "let must have two arguments"
        assert len(args[0]) > 0, "let must have at least one variable"
        # unzip formals and actuals
        formals, actuals = ([args[0][0]], [args[0][1]]) if not isinstance(
            args[0][0], list) else zip(*(args[0]))
        for f in formals:
            assert isinstance(f, str) and f.is_symbol(
            ), "let's formals must be symbols"
        desugar = [["lambda", formals, args[1]], *actuals]
        return eval(desugar, env)
    elif op == "for":
        assert len(args) == 4, "for must have four arguments"
        (sym, keyw, collection, body) = args
        assert keyw == ":in", "for's second argument must be :in"
        assert isinstance(sym, str) and sym.is_symbol(
        ), "for's first argument must be a symbol"
        coll = eval(collection, env)
        for item in coll:
            env[sym] = item
            eval(body, env)

    # image-related keywords
    elif op == "startfigure":
        assert len(args) == 2, "startfigure must have two arguments"
        env.newfig([eval(arg, env) for arg in args])
    elif op == "setpixel":
        assert len(args) == 3, "setpixel must have three arguments"
        (pos, keyw, col) = args
        assert keyw == ":to", "setpixel's second argument must be :to"
        pos = eval(pos, env)
        assert isinstance(pos, list) and len(
            pos) == 2, "positions must be length two lists"
        col = eval(col, env)
        assert isinstance(col, list) and len(
            col) == 3, "colors must be length three lists"
        env.headfig()[pos[0], pos[1]] = tuple(col)
    elif op == "setline":
        assert len(args) == 3, "setline must have three arguments"
        (keyw, line_idx, col) = args
        assert keyw in [
            ":x", ":y"], "setline's first argument must be :x or :y"
        line_idx = eval(line_idx, env)
        assert isinstance(line_idx, int), "line index must be int"
        col = eval(col, env)
        assert isinstance(col, list) and len(
            col) == 3, "colors must be length three lists"

        img = env.headfig()
        if keyw == ":x":
            for i in range(env.imgwidth()):
                img[line_idx, i] = tuple(col)
        else:  # ":y"
            for i in range(env.imgheight()):
                img[i, line_idx] = tuple(col)

    elif op == "snap!":
        assert len(args) == 0, "snap! must does not take any arguments"
        env.newfig()

    elif op == "save":
        assert len(args) in [1, 2], "save must have one or two arguments"
        env.savefigs(*[eval(arg, env) for arg in args])

    else:  # procedure call
        proc = eval(op, env)
        args = [eval(arg, env) for arg in args]
        return proc(*args)
