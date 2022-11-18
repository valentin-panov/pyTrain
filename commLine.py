import sys


def main ():
    print_arg()


def print_arg():
    for arg in sys.argv[1:]:
        print(arg)


if __name__ == "__main__":
    main()