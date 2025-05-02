import sys
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class Function:
	name: str
	method: Callable
	min_args: int
	max_args: int = -1
	default_kwargs: dict[str, Any] = field(default_factory=dict)
	
	MAX_ARG_COUNT: int = 100
	
	def __post_init__(self):
		if self.max_args == -1:
			self.max_args = self.min_args
	
	def call(self, *args, **kwargs) -> Any:
		return self.method(*args, **kwargs)


def convert_if_possible(input_: list[str]) -> list[str | int | float]:
	output: list[str | int | float] = []
	
	def is_float(s: str) -> bool:
		try:
			float(s)
			return True
		except ValueError:
			return False
	
	def is_int(s: str) -> bool:
		try:
			int(s)
			return True
		except ValueError:
			return False
	
	for x in input_:
		if is_int(x):
			output.append(int(x))
		elif is_float(x):
			output.append(float(x))
		
		else:
			output.append(x)
	
	return output


def run_function(functions: list[Function], function_name: str, *args: str) -> bool:
	if len(args) > 0:
		function_name: str = function_name.lower()
		function_args: list[str] = list(args)
		
		new_function_args = convert_if_possible(function_args)
		
		found_function: bool = False
		for function in functions:
			if function.name == function_name:
				found_function = True
				
				if not (function.min_args <= len(new_function_args) <= function.max_args):
					print(
						"args are bad, expected",
						function.min_args,
						"to",
						function.max_args,
						"got",
						len(new_function_args)
					)
					exit(1)
				
				result: Any = function.call(*new_function_args, **function.default_kwargs)
				
				if result is not None:
					print("result:", result)
		
		return found_function
	return False


def quick_run(functions: list[Function]) -> None:
	function_name: str = sys.argv[1]
	function_args: list[str] = sys.argv[2:]
	
	if run_function(functions, function_name, *function_args):
		return
	
	print(f"cannot find function '{function_name}', available are:")
	for f in functions:
		print(f"\t{f.name} (args: {f.min_args} to {f.max_args})")
