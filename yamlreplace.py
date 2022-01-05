from functools import reduce, partial
from sys import argv, stderr, stdin
from stat import S_ISREG, S_ISFIFO
from itertools import starmap
from os import fstat

from yaml import safe_load, dump
from yaml.scanner import ScannerError

RED = "\u001b[31m"
GREEN = "\u001b[32m"
RESET = "\u001b[0m"


def try_value_as_number(value):
    try:
        return int(value)
    except Exception:
        pass
    try:
        return float(value)
    except Exception:
        return value


def path_arg_split(patharg):
    try:
        path, arg = patharg.split(":")
        return path.split("."), try_value_as_number(arg)
    except Exception:
        return f"Unable to parse argument {RED}{patharg}{RESET}"


def set_path_to_value(yaml, path, value):
    try:
        nested_dictionary = reduce(lambda x, y: x[y], path[:-1], yaml)
        nested_dictionary[path[-1]] = value
    except KeyError as e:
        missing_key = str(e.args[0])
        missing_index = path.index(missing_key)
        key_to_path = ".".join(path[:missing_index]) + "." if missing_index != 0 else ""
        return f"Missing path {GREEN}{key_to_path}{RED}{missing_key}{RESET} from {'.'.join(path)}"
    except TypeError as e:
        return f"Path {RED}{'.'.join(path)}{RESET} tries to set a non-map field"


def get_file_input():
    file_name = argv[1]
    with open(file_name) as yaml_file:
        return safe_load(yaml_file)


def get_directed_input():
    return safe_load(stdin)


def main():
    # check input
    mode = fstat(0).st_mode
    try:
        first_arg, yaml_dict = (
            (1, get_directed_input())
            if S_ISREG(mode) or S_ISFIFO(mode)
            else (2, get_file_input())
        )
    except ScannerError:
        print("Unable to parse input yaml", file=stderr)
        exit(1)
    except IndexError:
        print("No yaml recieved", file=stderr)
        exit(1)

    prepared_arguments = list(map(path_arg_split, argv[first_arg:]))
    argument_errors = list(filter(lambda x: isinstance(x, str), prepared_arguments))
    if argument_errors:
        print(*argument_errors, file=stderr, sep="\n")
        exit(1)

    set_path_in_yaml = partial(set_path_to_value, yaml_dict)
    errors = list(filter(None, starmap(set_path_in_yaml, prepared_arguments)))
    if errors:
        print(*errors, file=stderr, sep="\n")
        exit(1)

    print(dump(yaml_dict), end="")


if __name__ == "__main__":
    main()
