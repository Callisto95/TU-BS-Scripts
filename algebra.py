from dataclasses import dataclass, field
from itertools import batched
from math import ceil, floor, log10, sqrt

from colorama import Fore, Style
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
        data.append((a, b))
    
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
    data: list[tuple[int, int]] = []
    
    x: int = ceil(sqrt(n))
    r: int = x ** 2 - n
    
    data.append((x, r))
    
    while not sqrt(r).is_integer():
        r = r + 2 * x + 1
        x = x + 1
        
        data.append((x, r))
    
    print(tabulate(data, headers=("x", "r"), tablefmt=TABLE_FORMAT, showindex=True))
    
    y: int = int(sqrt(r))
    
    print("y =", y)
    
    a: int = x + y
    b: int = x - y
    
    print(f"verifying: {a} * {b} = {a * b}")
    
    return a, b


@cli("sieve")
def sieve_of_eratosthenes(n: int) -> list[int]:
    numbers: list[int] = list(range(2, n + 1))
    primes: list[int] = []
    
    while len(numbers) > 0:
        prime: int = numbers[0]
        primes.append(prime)
        
        multiplicatives: list[int] = list(range(prime, n + 1, prime))
        numbers = [number for number in numbers if number not in multiplicatives]
        
        print(
            tabulate(
                [
                    (f"current sieve: {prime}", multiplicatives),
                    ("remaining numbers", numbers),
                    ("primes", primes),
                ],
                tablefmt="plain",
            ),
        )
        print()
    
    return primes


@cli("sieve-colour")
def sieve_of_eratosthenes(n: int) -> list[int]:
    max_length: int = floor(log10(n)) + 1
    
    @dataclass
    class FilteredNumber:
        number: int
        filtered: bool = field(default=False)
    
    numbers: list[FilteredNumber] = [FilteredNumber(n) for n in range(2, n + 1)]
    primes: list[int] = []
    
    while len((current_numbers := list(filter(lambda x: not x.filtered, numbers)))) > 0:
        prime: int = current_numbers[0].number
        primes.append(prime)
        
        multiplicatives: list[int] = list(range(prime, n + 1, prime))
        
        print("current prime", prime)
        
        for line in batched([FilteredNumber(1, True)] + numbers, 10):
            for number in line:
                # 1 is always ignored
                if number.number == 1:
                    print(" " * (max_length + 1), end="")
                    continue
                
                if number.number == prime:
                    colour = Fore.YELLOW
                elif number.number in primes:
                    colour = Fore.BLUE
                elif number.filtered and number.number in multiplicatives:
                    colour = Fore.MAGENTA
                elif number.number in multiplicatives:
                    colour = Fore.RED
                elif number.filtered:
                    colour = Fore.MAGENTA
                else:
                    colour = ""
                print(f"{colour}{number.number:{max_length}d}{Style.RESET_ALL}", end=" ")
                
                if number.number in multiplicatives:
                    number.filtered = True
            print()  # after each line
        print()  # free line after each block
    
    return primes


if __name__ == "__main__":
    quick_run()
