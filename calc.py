# breaker = 0
# global breaker
from card_randomizer import randomize
from card_randomizer import print_cards


def main():
    print_cards(randomize(['card1', 'card2', 'card3', 'card4', 'card5']))
    first = get_arg('first')
    second = get_arg('second')
    action = get_action('action')
    print('the result is:', math_it(first, second, action))


def get_arg(title):
    while True:
        try:
            arg = float(input(f'the {title} parameter:'))
        except ValueError:
            print("bad input, repeat")
        else:
            return arg


def get_action(title):
    while True:
        arg = input(f'the {title}:')
        match arg:
            case '+' | '-' | '*' | '/':
                return arg
            case _:
                print("bad input, repeat")


def math_it(first, second, a):
    match a:
        case '+':
            return round(float(first + second), 2)
        case '-':
            return round(float(first - second), 2)
        case '*':
            return round(float(first * second), 2)
        case '/':
            return round(float(first / second), 2)
        case _:
            return 'bad luck'


if __name__ == "__main__":
    main()
