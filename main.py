from card_randomizer import randomize, print_cards
from calc import calc


def main():
    print_cards(randomize(['card1', 'card2', 'card3', 'card4', 'card5']))
    calc()


if __name__ == "__main__":
    main()
