from functools import reduce
from math import factorial

from tu_bs_scripts.quick_cli import Function, quick_run


def binomialkoeffizient(n: int, k: int) -> int:
	return factorial(n) // (factorial(k) * factorial(n - k))


def multinomialkoeffizient(n: int, *m: int) -> int:
	if sum(m) != n:
		raise ArithmeticError(f"m's must match n! is {sum(m)}, should be {n}")
	return factorial(n) // reduce(lambda a, b: a * b, map(lambda x: factorial(x), m))


functions: list[Function] = [
	Function("binom", binomialkoeffizient, 2),
	Function("multinom", multinomialkoeffizient, 2, Function.MAX_ARG_COUNT)
]

if __name__ == '__main__':
	quick_run(functions)
