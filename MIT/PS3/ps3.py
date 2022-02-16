# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
from typing import Union
import string
from xmlrpc.client import boolean

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}


WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """

    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence: Union[str, list]) -> dict[str, int]:
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.
    """

    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


def get_word_score(word: str, n: int) -> int:
    """ 
        Returns the score for a word. Assumes the word is a
    valid word.
        """

    word_score = 0
    first_comp = sum([SCRABBLE_LETTER_VALUES.get(x, 0) for x in word.lower()])
    second_comp = 7 * len(word) - 3*(n-len(word))
    # Implementation of ternary operator
    word_score = first_comp * (second_comp if second_comp > 1 else 1)
    return word_score


def display_hand(hand: dict[str, int]):
    """ 
        Displays the letters currently in the hand. 
        """

    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')
    print()


def deal_hand(n: int) -> dict:
    """
    Returns a random hand containing n lowercase letters.
    """

    hand = {}
    num_vowels = int(math.ceil(n / 3)) - 1
    hand["*"] = 1
    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand


def update_hand(hand: dict[str, int], word: str) -> dict[str, int]:
    """
    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.
    """
    new_hand = copy_hand(hand)
    for x in word.lower():
        new_hand[x] -= 1
        if new_hand[x] == 0:
            new_hand.pop(x)
    return new_hand


def copy_hand(hand: dict[str, int]) -> dict[str, int]:
    new_hand = dict()
    for x in hand.keys():
        new_hand[x] = hand[x]
    return new_hand


def is_valid_word(word: str, hand: dict[str, int], word_list: list) -> boolean:
    """
    Returns True if word is in the word_list and is entirely
composed of letters in the hand. 
    """
    word_check = False
    if "*" in word:
        for char in VOWELS:
            # str.replace returns a new string
            new_word = word.replace("*", char)
            if new_word.lower() in word_list:  # check the new word against the word list
                word_check = True
                break
    else:
        word_check = word.lower() in word_list

    word_to_dict = get_frequency_dict(word.lower())
    keys_in_hand = all([x in hand.keys() and word_to_dict[x]
                       <= hand[x] for x in word.lower()])

    if word_check and keys_in_hand:
        return True
    else:
        return False


def calculate_handlen(hand: dict[str, int]):
    """ 
    Returns the length (number of letters) in the current hand.

    hand: dictionary (string-> int)
    returns: integer
    """
    count = sum([hand.get(x, 0) for x in hand.keys()])
    return count


def play_hand(hand: dict[str, int], word_list: list) -> int:
    """
    Allows the user to play the given hand.
    """
    total_score = 0
    hand_temp = copy_hand(hand=hand)
    while hand_temp != {}:
        display_hand(hand_temp)
        word = input('Enter word, or "!!" to indicate that you are finished: ')
        
        if word == "!!": break
        
        if not is_valid_word(word=word, hand=hand_temp, word_list=word_list):
            print("That is not a valid word. Please choose another word. ")
        else:
            score = get_word_score(word=word, n=calculate_handlen(hand=hand_temp))
            total_score += score
            print(f"{word} earned {score} points. Total: {total_score} points")
            hand_temp = update_hand(hand=hand_temp, word=word)
    if hand_temp == {}: print("Ran out of letters")
    return total_score


def substitute_hand(hand: dict[str, int], letter: str) -> dict[str, int]:
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.
    """
    new_letter = letter
    while new_letter in hand.keys():
        new_letter = random.choice(VOWELS+CONSONANTS)
    
    count = hand.pop(letter, -1)
    
    if count:   hand[new_letter] = count
    return hand # return hand as it is


def play_game(word_list: list):
    """
    Allow the user to play a series of hands
    """

    hand_count = int(input("Enter total number of hands: "))
    total_score = 0
    replay_hand = False
    while hand_count != 0:
        # hand = deal_hand(7)
        hand = deal_hand(7)
        display_hand(hand=hand)
        
        if replay_hand == False:
            choice = True if input("Would you like to substitute a letter? (yes/no) ") == "yes" else False
        if choice:
            letter = input("Which letter would you like to replace: ")
            hand = substitute_hand(hand=hand, letter=letter)

        # display_hand(hand)
        score = play_hand(hand=hand, word_list=word_list)
        print(f"Total score for this hand: {score}\n----------")
        replay_hand = True if input("Would you like to replay the hand? (yes/no) ") == "yes" else False
        if choice:  continue
        else:
            total_score += score
            hand_count -= 1
    print(f" Total score over all hands: {total_score}")


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
    # Test for substitute_hand 
    # hand = {'n': 1, 'h': 1, '*': 1, 'y': 1, 'd':1, 'w':1, 'e': 2}
    # print(substitute_hand(hand, 'n'))