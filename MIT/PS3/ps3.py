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
	new_hand = dict()
	for x in hand.keys():
		new_hand[x] = hand[x]
	for x in word.lower():
		new_hand[x] -= 1
		if new_hand[x] == 0:
			new_hand.pop(x)
	return new_hand


def is_valid_word(word: str, hand: dict[str, int], word_list: list) -> boolean:
	"""
	Returns True if word is in the word_list and is entirely
    composed of letters in the hand. 
	"""
	word_check = False
	if "*" in word:
		for char in VOWELS:
			new_word = word.replace("*", char) # str.replace returns a new string
			if new_word.lower() in word_list: # check the new word against the word list
				word_check = True
				break
	else: word_check = word.lower() in word_list

	word_to_dict = get_frequency_dict(word.lower())
	keys_in_hand = all([x in hand.keys() and word_to_dict[x] <= hand[x] for x in word.lower()])
	
	if word_check and keys_in_hand:	return True
	else: return False

def calculate_handlen(hand):
	""" 
	Returns the length (number of letters) in the current hand.

	hand: dictionary (string-> int)
	returns: integer
	"""
	count = sum([hand.get(x, 0) for x in hand.keys()])
	return count


def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.

    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand

    """

    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score

    # As long as there are still letters left in the hand:

    # Display the hand

    # Ask user for input

    # If the input is two exclamation points:

    # End the game (break out of the loop)

    # Otherwise (the input is not two exclamation points):

    # If the word is valid:

    # Tell the user how many points the word earned,
    # and the updated total score

    # Otherwise (the word is not valid):
    # Reject invalid word (print a message)

    # update the user's hand by removing the letters of their inputted word

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function


#
# Problem #6: Playing a game
#


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.

    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

    pass  # TO DO... Remove this line when you implement this function


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series

    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.

    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """

    # TO DO... Remove this line when you implement this function
    print("play_game not implemented.")


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
