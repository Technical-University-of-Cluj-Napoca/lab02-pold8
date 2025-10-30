import sys


def multiply_all(*args: int) -> int:
    if len(sys.argv) == 0:
        return 0
    else:
        res = 1;
        for arg in args:
            res *= arg
        return res

if __name__ == '__main__':
    arguments_list_str = sys.argv[1:]
    try:
        arguments_list_int = [int(arg) for arg in arguments_list_str]
    except ValueError:
        print("Eroare: Toate argumentele trebuie să fie numere întregi valide.")
        sys.exit(1)

    result = multiply_all(*arguments_list_int)
    print(result)