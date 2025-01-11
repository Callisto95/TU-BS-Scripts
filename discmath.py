#!/usr/bin/python

import sys
from dataclasses import dataclass
from functools import cache
from typing import Any, Callable

from tabulate import tabulate

NO_DATA: str = "-"
TABLE_FORMAT: str = "presto"


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


def ggt(num1: int, num2: int, maximum_iterations: int = 100) -> int:
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
		
		data.append([iteration, f"q{iteration}={factor}", f"r{iteration + 2}={r2}", ", ".join(multiplications)])
		
		r0 = r1
		r1 = r2
		
		if (iteration := iteration + 1) > maximum_iterations:
			print("max iteration depth reached")
			exit(1)
	
	print(tabulate(data, headers=["iter", "factor", "rest", "multiplications"], tablefmt=TABLE_FORMAT))
	return r2_save


def ggt_extended(num1: int, num2: int, maximum_iterations: int = 100) -> tuple[int, int]:
	saved_ri: list[int] = [num1, num2]
	saved_qi: list[int | str] = [NO_DATA]
	saved_si: list[int | str] = [1, 0]
	saved_ti: list[int | str] = [0, 1]
	
	current_r: int = num2
	current_q: int = -1  # set anyway, ignore -1
	
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
			headers=["iter", "ri", "qi", "si", "ti"],
			tablefmt=TABLE_FORMAT,
			colalign=n_alignment(5, "right")
		)
	)
	
	x: int = saved_si[iteration]
	y: int = saved_ti[iteration]
	
	print(f"verifying: {x}*{num1}{"+" if y >= 0 else ""}{y}*{num2}={x*num1+y*num2}")
	
	return x, y


@dataclass
class Function:
	name: str
	method: Callable
	min_args: int
	max_args: int = None  # NOSONAR
	
	def __post_init__(self):
		if self.max_args is None:
			self.max_args = self.min_args
	
	def call(self, args: list[Any]) -> Any:
		return self.method(*args)


FUNCTIONS: list[Function] = [
	Function("ggt", ggt, 2, 3),
	Function("ggt_ext", ggt_extended, 2),
	Function("collatz_range", collatz_range, 1, 2)
]


def convert_if_possible(input_: list[str]) -> list[str | int | float]:
	output: list[str | int | float] = []
	
	def is_float(s: str) -> bool:
		try:
			float(s)
			return True
		except ValueError:
			return False
	
	for x in input_:
		if x.isdigit():
			output.append(int(x))
		elif is_float(x):
			output.append(float(x))
		
		else:
			output.append(x)
	
	return output


def main() -> bool:
	args = sys.argv[1:]
	if len(args) > 0:
		function_name = args[0].lower()
		function_args = args[1:]
		
		new_function_args = convert_if_possible(function_args)
		
		found_function: bool = False
		for function in FUNCTIONS:
			if function.name == function_name:
				found_function = True
				
				if len(new_function_args) < function.min_args or len(new_function_args) > function.max_args:
					print(
						"args are bad, expected",
						function.min_args,
						"to",
						function.max_args,
						"got",
						len(new_function_args)
					)
					exit(1)
				
				result: Any = function.call(new_function_args)
				
				if result is not None:
					print("result:", result)
		
		return found_function


if __name__ == '__main__' and not main():
	print("cannot find function, available are:")
	for f in FUNCTIONS:
		print(f"\t{f.name} (args: {f.min_args} to {f.max_args})")
