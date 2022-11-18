from card_randomizer import randomize, print_cards
from calc import calc
from commLine import print_arg
from getReq import itunes_tracks


def main():
    print_cards(randomize(['card1', 'card2', 'card3', 'card4', 'card5']))
    calc()
    print_arg()
    itunes_tracks()


if __name__ == "__main__":
    main()
