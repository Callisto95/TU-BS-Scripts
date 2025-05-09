#!/usr/bin/python

import builtins
import sys
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Callable, Generator

from tabulate import tabulate

from tu_bs_scripts.quick_cli import Function, quick_run

NO_DATA: str = "-"
TABLE_FORMAT: str = "presto"


# disabling printing is significantly faster
class Printer:
	enabled: bool = True
	
	@classmethod
	def print(cls, *args, **kwargs):
		if cls.enabled:
			cls.force_print(*args, **kwargs)
	
	force_print = builtins.print


print = Printer.print


def indexed_print(*args, unit: str | None = None):
	if unit is None:
		print(", ".join([f"{i}: {entry}" for i, entry in enumerate(args)]))
	else:
		print(", ".join([f"{unit}{i}: {entry}" for i, entry in enumerate(args)]))


def n_alignment(n: int, alignment: str) -> list[str]:
	l: list[str] = []
	for _ in range(n):
		l.append(alignment)
	
	return l


@cache
def collatz(n: int) -> int:
	if n % 2 == 0:
		return int(n / 2)
	else:
		return 3 * n + 1


def collatz_range(begin: int, end: int = -1) -> None:
	if begin <= 0:
		print("begin cannot be less or equal than 0, using 2")
		begin = 2
	
	if end == -1:
		end = begin
	
	for i in range(begin, end + 1):
		vals = []
		current_n = i
		
		while current_n != 1:
			current_n = collatz(current_n)
			vals.append(current_n)
		
		print(i, ":", *vals)


def ggt(num1: int, num2: int, maximum_iterations: int = 100, print_multiplications: bool = False) -> int:
	data: list[list[str | int]] = []
	
	iteration: int = 1
	
	r0 = num1
	r1 = num2
	
	# must be set, but not 0 -> use invalid number
	r2: int = -1
	r2_save: int = r2
	
	while r2 != 0:
		r2_save = r2
		
		factor, r2 = divmod(r0, r1)
		
		# print(f"{iteration}:: q{iteration}: {factor} ({factor * r1}) r{iteration+2}: {r2}", end=" | ")
		
		multiplications: list[str] = []
		for i in range(2, factor + 2):
			multiplications.append(f"{i}:{r1 * i}")
		
		data.append([iteration, f"q{iteration}={factor}", f"r{iteration + 2}={r2}"])
		
		if print_multiplications:
			data[-1].append(", ".join(multiplications))
		
		r0 = r1
		r1 = r2
		
		if (iteration := iteration + 1) > maximum_iterations:
			print("max iteration depth reached")
			exit(1)
	
	headers: list[str] = ["i", "factor", "rest"]
	
	if print_multiplications:
		headers.append("multiplications")
	
	print(tabulate(data, headers=headers, tablefmt=TABLE_FORMAT))
	return r2_save


def ggt_extended(num1: int, num2: int, maximum_iterations: int = 100) -> tuple[int, int, int]:
	if num1 < 0 or num2 < 0:
		print("using absolute values instead of negatives")
	
	num1 = abs(num1)
	num2 = abs(num2)
	
	saved_ri: list[int] = [num1, num2]
	saved_qi: list[int | str] = [NO_DATA]
	saved_si: list[int | str] = [1, 0]
	saved_ti: list[int | str] = [0, 1]
	
	current_r: int = num2
	
	# no iteration 0 is done
	iteration: int = 0
	while current_r != 0:
		iteration += 1
		
		current_q, current_r = divmod(saved_ri[iteration - 1], current_r)
		
		saved_ri.append(current_r)
		saved_qi.append(current_q)
		
		if iteration == 1:
			# do not adjust s1, t1
			continue
		
		saved_si.append(-saved_qi[iteration - 1] * saved_si[iteration - 1] + saved_si[iteration - 2])
		saved_ti.append(-saved_qi[iteration - 1] * saved_ti[iteration - 1] + saved_ti[iteration - 2])
		
		if iteration > maximum_iterations:
			print("too many iterations, exiting")
			exit(1)
	
	saved_qi.append(NO_DATA)
	saved_si.append(NO_DATA)
	saved_ti.append(NO_DATA)
	
	data: list[list[str | int]] = []
	
	for i in range(iteration + 2):
		data.append([i, saved_ri[i], saved_qi[i], saved_si[i], saved_ti[i]])
	
	print(
		tabulate(
			data,
			headers=["i", "ri", "qi", "si", "ti"],
			tablefmt=TABLE_FORMAT,
			colalign=n_alignment(5, "right")
		)
	)
	
	x: int = saved_si[iteration]
	y: int = saved_ti[iteration]
	result: int = x * num1 + y * num2
	
	print(f"verifying: {x}*{num1}{"+" if y >= 0 else ""}{y}*{num2}={result}")
	
	return x, y, result


# Sieve of Eratosthenes
# Code by David Eppstein, UC Irvine, 28 Feb 2002
# http://code.activestate.com/recipes/117119/
def gen_primes():
	""" Generate an infinite sequence of prime numbers.
	"""
	# Maps composites to primes witnessing their compositeness.
	# This is memory efficient, as the sieve is not "run forward"
	# indefinitely, but only as long as required by the current
	# number being tested.
	#
	D = { }
	
	# The running integer that's checked for primeness
	q = 2
	
	while True:
		if q not in D:
			# q is a new prime.
			# Yield it and mark its first multiple that isn't
			# already marked in previous iterations
			#
			yield q
			D[q * q] = [q]
		else:
			# q is composite. D[q] is the list of primes that
			# divide it. Since we've reached q, we no longer
			# need it in the map, but we'll mark the next
			# multiples of its witnesses to prepare for larger
			# numbers
			#
			for p in D[q]:
				D.setdefault(p + q, []).append(p)
			del D[q]
		
		q += 1


PRIME_CACHE: list[int] = []


def get_prime(n: int) -> int:
	# the first prime is the 0-th element in the cache
	n -= 1
	
	cached_size: int = len(PRIME_CACHE)
	
	if n < cached_size:
		return PRIME_CACHE[n]
	
	generator: Generator[int, Any, None] = gen_primes()
	for i in range(0, n + 1):
		prime = next(generator)
		
		if i < cached_size:
			continue
		
		PRIME_CACHE.append(prime)
	
	return PRIME_CACHE[n]


def is_prime(number: int) -> bool:
	for n in range(3, number // 2, 2):
		if number % n == 0:
			return False
	
	return True


def prime_decomposition(number: int) -> dict[int, int]:
	result: dict[int, int] = {}
	
	while number > 1:
		i = 1
		while number % (prime := get_prime(i)) != 0:
			i += 1
		
		number = number // prime
		
		if prime in result:
			result[prime] += 1
		else:
			result[prime] = 1
		
		# significantly faster for big primes
		if is_prime(number):
			result[number] = 1
			break
	
	return result


def kgv(*numbers: int) -> int:
	all_primes: dict[int, int] = {}
	for number in numbers:
		number_primes: dict[int, int] = prime_decomposition(number)
		
		# merge prime factors
		for prime in number_primes:
			if prime not in all_primes or all_primes[prime] < number_primes[prime]:
				all_primes[prime] = number_primes[prime]
	
	# multiply everything together
	prime_sum: int = 1
	for prime, factor in all_primes.items():
		prime_sum *= pow(prime, factor)
	
	return prime_sum


def chinese_remainder(*remainder_mod: str) -> int:
	length: int = len(remainder_mod)
	
	as_: list[int] = []
	ms: list[int] = []
	
	big_m: int = 1
	for r in remainder_mod:
		remainder, mod = r.split(":")
		
		remainder = int(remainder)
		mod = int(mod)
		
		as_.append(remainder)
		ms.append(mod)
		
		big_m *= mod
	
	indexed_print(*as_, unit="a")
	indexed_print(*ms, unit="m")
	print("M:", big_m)
	
	big_ms: list[int] = []
	
	for i in range(length):
		m: int = 1
		for j in range(length):
			if i == j:
				continue
			m *= ms[j]
		big_ms.append(m)
	
	indexed_print(*big_ms, unit="M")
	
	ys: list[int] = []
	
	Printer.enabled = False
	
	for i in range(length):
		s, _, _ = ggt_extended(big_ms[i], ms[i])
		ys.append(s % ms[i])
	
	Printer.enabled = True
	
	indexed_print(*ys, unit="y")
	
	sum_: int = 0
	for i in range(length):
		sum_ += as_[i] * big_ms[i] * ys[i]
	
	print("sum:", sum_)
	sum_ %= big_m
	
	return sum_
	

functions: list[Function] = [
	Function("ggt", ggt, 2, 3),
	Function("ggt-multi", ggt, 2, 3, default_kwargs={"print_multiplications": True}),
	Function("ggt-ext", ggt_extended, 2),
	Function("collatz", collatz_range, 1, 2),
	Function("prime-decomp", prime_decomposition, 1),
	Function("kgv", kgv, 2, Function.MAX_ARG_COUNT),
	Function("chin", chinese_remainder, 3, Function.MAX_ARG_COUNT)
]

if __name__ == '__main__':
	quick_run(functions)
