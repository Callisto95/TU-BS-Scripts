import inspect
import sys
from dataclasses import dataclass, field
from inspect import Parameter, Signature
from typing import Any, Callable


@dataclass(frozen=True)
class Function:
    method: Callable
    min_args: int
    max_args: int
    default_kwargs: dict[str, Any] = field(default_factory=dict)
    
    MAX_ARG_COUNT: int = field(default=100, repr=False, init=False, hash=False)


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


registered_functions: dict[str, Function] = { }


def cli(
    name: str | Callable,
    default_kwargs: dict[str, Any] | None = None,
    force_min: int | None = None,
    force_max: int | None = None,
) -> Any:
    if (force_min is not None and force_min < 0) or (force_max is not None and force_max < 0):
        raise RuntimeError(
            f"cannot use a value of less than 0 for overwrites. (min is set to {force_min}, max is set to {force_max})",
        )
    
    if default_kwargs is None:
        default_kwargs = { }
    
    if callable(name):
        func_ = name
        name = func_.__name__
    else:
        func_ = None
    
    def decorator(func) -> Callable:
        function_name: str = name if name is not None else func.__name__
        function_name = function_name.replace("_", "-")
        
        if function_name in registered_functions:
            # TODO: change this to a good error
            raise KeyError(f"a function with the name '{function_name}' has already been registered")
        
        sig: Signature = inspect.signature(func)
        
        min_args: int = 0
        max_args: int = 0
        
        for param in sig.parameters.values():
            if param.kind == Parameter.VAR_POSITIONAL:
                max_args = Function.MAX_ARG_COUNT
                continue
            
            if param.kind not in (Parameter.POSITIONAL_OR_KEYWORD, Parameter.POSITIONAL_ONLY):
                continue
            
            if param.default is inspect.Parameter.empty:
                # required (your "positional")
                min_args += 1
            
            max_args += 1
        
        if max_args > Function.MAX_ARG_COUNT:
            max_args = Function.MAX_ARG_COUNT
        if force_min is not None:
            min_args = force_min
        if force_max is not None:
            max_args = force_max
        
        registered_functions[function_name] = Function(func, min_args, max_args, default_kwargs)
        
        return func
    
    if callable(func_):
        return decorator(func_)
    
    return decorator


def run_function(function_name: str, *args: str) -> bool:
    function_name = function_name.lower()
    function_args: list[str] = list(args)
    
    new_function_args: list[str | int | float] = convert_if_possible(function_args)
    
    if function_name not in registered_functions:
        return False
    
    function: Function = registered_functions[function_name]
    
    if not (function.min_args <= len(new_function_args) <= function.max_args):
        print(
            "args are bad, expected",
            function.min_args,
            "to",
            function.max_args,
            "got",
            len(new_function_args),
        )
        return False
    
    result: Any = function.method(*new_function_args, **function.default_kwargs)
    
    if result is not None:
        print("result:", result)
    
    return True


def list_functions() -> None:
    for name, info in sorted(registered_functions.items()):
        if info.min_args == info.max_args:
            print(f"\t{name} (args: {info.min_args})")
        else:
            print(f"\t{name} (args: {info.min_args} to {info.max_args})")


def quick_run() -> None:
    if len(sys.argv) <= 1:
        print("no function name given")
        list_functions()
        exit(1)
    
    function_name: str = sys.argv[1] if len(sys.argv) > 1 else ""
    function_args: list[str] = sys.argv[2:]
    
    if run_function(function_name, *function_args):
        return
    
    print(f"cannot find function '{function_name}', available are:")
    list_functions()
    exit(1)


__all__ = ["quick_run", "cli"]
