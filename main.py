from src.pyval import *


def main():
    @type_check.type_check_args([int, int])
    def mul(x, y):
        return x * y

    print(mul(3, 7))


if __name__ == "__main__":
    main()
