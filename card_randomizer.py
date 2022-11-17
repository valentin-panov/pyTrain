import random


def randomize(array):
    random.shuffle(array)
    return array


def print_cards(cards):
    for card in cards:
        print(card)