from math import ceil, log10, sqrt

from tabulate import tabulate

from tu_bs_scripts.quick_cli import cli, quick_run

TABLE_FORMAT: str = "presto"


@cli
def euklid_old(a: int, b: int) -> int:
    data: list[tuple[int, int]] = []
    
    if a == 0:
        return b
    while b != 0:
        if a > b:
            a = a - b
        else:
            b = b - a
        data.append((a,b))
    
    print(tabulate(data, headers=("a", "b"), tablefmt=TABLE_FORMAT))
    return a


@cli
def euklid_modern(a: int, b: int) -> int:
    data: list[tuple[int, int, int]] = []
    
    while b != 0:
        h: int = a % b
        a = b
        b = h
        data.append((a, b, h))
    
    print(tabulate(data, headers=("a", "b", "mod"), tablefmt=TABLE_FORMAT))
    return a


@cli
def base_change(number: str | int, source_base: int, target_base: int) -> str:
    data: list[tuple[int, int, int, int]] = []
    values: list[int] = []
    
    rest: int = int(str(number), source_base)
    if source_base != 10:
        print(f"necessary conversion: ({number}){source_base} to ({rest})10")
        print()
    
    while rest != 0:
        rest_save: int = rest
        rest, mod = divmod(rest, target_base)
        data.append((rest_save, target_base, rest, mod))
        values.append(mod)
    
    print(tabulate(data, headers=("current", "/ base", "= div", "% mod"), tablefmt="plain"))
    
    values.reverse()
    if target_base <= 10:
        # a number can be created nicely
        return "".join([str(value) for value in values])
    elif target_base == 16:
        # hex returns '0x...', so it must be stripped
        return "0x" + "".join([hex(value)[2:].upper() for value in values])
    else:
        # fallback: just dump the array
        return repr(values)


@cli("fermat-factor")
def fermat_factorization(n: int) -> tuple[int, int]:
    x: int = ceil(sqrt(n))
    r: int = x**2 - n

    while not sqrt(r).is_integer():
        r = r + 2 * x + 1
        x = x + 1

    y: int = int(sqrt(r))
    a: int = x + y
    b: int = x - y

    return a, b


if __name__ == "__main__":
    quick_run()
