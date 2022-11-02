# Impl (Image Programming Language)
A cute but powerful little [LISP](https://en.wikipedia.org/wiki/Lisp_(programming_language)) dialect geared towards generating images.

## Inspiration
Inspired by [Norvig's lis.py](https://norvig.com/lispy.html), Impl started as a subset of [Scheme](https://www.scheme.org/), but diverged because I had an idea to make a language that produces images from language features. 

## What can it do? 
Impl has a good size [set of standard procedures](https://github.com/DanielRJohnson/Impl/blob/main/env.py) and [keywords](https://github.com/DanielRJohnson/Impl/blob/main/eval.py).

Impl supports:
 * List, Int, Float, String, and Boolean operations borrowing from Python's semantics
 * User-defined variables and first-class procedures with lexical scope
 * If-else conditionals
 * Ease of use language features like `let`, `for`, and `' quoting`
 * "keywords" like `:x`, inspired by [Clojure](https://clojure.org/)
 * etc.

## Examples
Examples can be found in [_examples/](https://github.com/DanielRJohnson/Impl/tree/main/_examples), but here are a couple of animations I generated using Impl.

#### [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)

##### [Gosper Glider Gun](https://conwaylife.com/wiki/Gosper_glider_gun)
<img src="https://github.com/DanielRJohnson/Impl/blob/main/_examples/conway/conway.gif" width="400" height="400" />

##### Random starting point with cell alive probability of 15%
<img src="https://github.com/DanielRJohnson/Impl/blob/main/_examples/conway/randomlife.gif" width="400" height="400" />

#### [Linear Regression](https://en.wikipedia.org/wiki/Linear_regression) Fitting
<img src="https://github.com/DanielRJohnson/Impl/blob/main/_examples/linear_regression/linreg.gif" width="400" height="400" />

## Usage
`python <path to impl.py> <source file name?>`

Running Impl without any arguments results in the REPL, which can evaluate expressions but is not meant for generating images. Running Impl with one filename argument executes the given file.
