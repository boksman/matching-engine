import sys


def print_stderr(*args, **kwargs):
    # print to standard error
    print(*args, file=sys.stderr, **kwargs)


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False