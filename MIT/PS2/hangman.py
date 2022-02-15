# Hangman Game

import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    return random.choice(wordlist)


def is_word_guessed(secret_word, letters_guessed):
    if all(letter in letters_guessed for letter in list(secret_word)):
        return True
    else:
        return False


def get_guessed_word(secret_word, letters_guessed):
    guessed = ""
    for letter in list(secret_word):
        if letter in letters_guessed:
            guessed += letter
        else:
            guessed += "_ "
    return guessed


def get_available_letters(letters_guessed):
    return "".join([x for x in string.ascii_lowercase if x not in letters_guessed])


def hangman(secret_word):
    remaining_guesses = 6
    warnings_remaining = 3
    letters_guessed = []
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print("-------------")

    while remaining_guesses > 0:
        print(f"You have {remaining_guesses} guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}")
        guess = input("Please guess a letter: ")

        if guess not in get_available_letters(letters_guessed):
            warnings_remaining -= 1
            if guess in string.ascii_letters:
                print(
                    f"Oops! You've already guessed that letter. You now have {warnings_remaining} warnings: ", end="")
            else:
                print(
                    f"Oops! You've guessed an invalid symbol. You now have {warnings_remaining} warnings: ", end="")
        elif guess in secret_word:
            letters_guessed.append(guess)
            print(f"Good guess: ", end="")
        elif guess not in secret_word:
            letters_guessed.append(guess)
            remaining_guesses -= 1
            print("Oops! That letter is not in my word: ", end="")

        print(get_guessed_word(secret_word, letters_guessed))
        print("------------")

        if is_word_guessed(secret_word, letters_guessed):
            print("Congratulations, you won!")
            score = remaining_guesses * \
                len([x for x in letters_guessed if x in secret_word])
            print("Your total score for this game is: ", score)
            break

    if remaining_guesses == 0:
        print(f"Sorry, you ran out of guesses. The word was {secret_word}.")


# -----------------------------------


def match_with_gaps(my_word, other_word):
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    if len(other_word) != len(my_word.replace(" ", "")):
        return False
    else:
        for i in range(len(other_word)):
            my_word = my_word.replace(" ", "")
            if my_word[i] != "_" and my_word[i] != other_word[i]:
                return False
            elif my_word[i] == "_":
                continue
        return True


def show_possible_matches(my_word):
    words = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            words.append(word)
    return " ".join(words)


def hangman_with_hints(secret_word):
    remaining_guesses = 6
    warnings_remaining = 3
    letters_guessed = []
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print("-------------")

    while remaining_guesses > 0:
        print(f"You have {remaining_guesses} guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}")
        guess = input("Please guess a letter: ")

        if guess not in get_available_letters(letters_guessed):
            warnings_remaining -= 1
            if guess.isalpha():
                print(
                    f"Oops! You've already guessed that letter. You now have {warnings_remaining} warnings: ", end="")
            else:
                if guess == "*":
                    print(show_possible_matches(
                        get_guessed_word(secret_word, letters_guessed)))
                else:
                    print(
                        f"Oops! You've guessed an invalid symbol. You now have {warnings_remaining} warnings: ", end="")
        elif guess in secret_word:
            letters_guessed.append(guess)
            print(f"Good guess: ", end="")
        elif guess not in secret_word:
            letters_guessed.append(guess)
            remaining_guesses -= 1
            print("Oops! That letter is not in my word: ", end="")

        print(get_guessed_word(secret_word, letters_guessed))
        print("------------")

        if is_word_guessed(secret_word, letters_guessed):
            print("Congratulations, you won!")
            score = remaining_guesses * \
                len([x for x in letters_guessed if x in secret_word])
            print("Your total score for this game is: ", score)
            break

    if remaining_guesses == 0:
        print(f"Sorry, you ran out of guesses. The word was {secret_word}.")


if __name__ == "__main__":
    wordlist = load_words()
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)
	######################
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
    # print(match_with_gaps("a_ _ le", "apple"))
    # print(show_possible_matches("a_ _ l_"))
