from tu_bs_scripts.quick_cli import quick_run, cli


@cli
def euklid_old(a: int, b: int) -> int:
    if a == 0:
        return b
    while b != 0:
        if a > b:
            a = a - b
        else:
            b = b - a
        print(f"a: {a}, b: {b}")
    return a


@cli
def euklid_modern(a: int, b: int) -> int:
    while b != 0:
        h: int = a % b
        a = b
        b = h
        print(f"a: {a}, b: {b}, mod {h}")
    return a


if __name__ == '__main__':
    quick_run()
