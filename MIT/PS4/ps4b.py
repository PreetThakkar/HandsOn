# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

### HELPER CODE ###


def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    # print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    # print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###


WORDLIST_FILENAME = 'words.txt'


class Message(object):
    def __init__(self, text: str) -> None:
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self) -> str:
        return self.message_text

    def get_valid_words(self) -> list[str]:
        # Return a COPY of valid_words
        return [word for word in self.valid_words]

    def build_shift_dict(self, shift: int) -> dict[str, str]:
        shift_dict = {}
        for i in range(26):
            shift_dict[string.ascii_lowercase[i]
                       ] = string.ascii_lowercase[(i+shift) % 26]
            shift_dict[string.ascii_uppercase[i]
                       ] = string.ascii_uppercase[(i+shift) % 26]
        return shift_dict

    def apply_shift(self, shift: int) -> str:
        shifted_string = ""
        shift_dict = self.build_shift_dict(shift)
        for i in self.get_message_text():
            shifted_string += shift_dict.get(i, i)
        return shifted_string


class PlaintextMessage(Message):
    def __init__(self, text: str, shift: int) -> None:
        super().__init__(text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)
        self.message_text_encrypted = self.apply_shift(self.shift)

    def get_shift(self) -> int:
        return self.shift

    def get_encryption_dict(self) -> dict[str, str]:
        copy = {}
        for key, value in self.encryption_dict.items():
            copy[key] = value
        return copy

    def get_message_text_encrypted(self) -> str:
        return self.message_text_encrypted

    def change_shift(self, shift: int) -> None:
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)
        self.message_text_encrypted = self.apply_shift(self.shift)


class CiphertextMessage(Message):
    def __init__(self, text: str) -> None:
        super().__init__(text)

    def decrypt_message(self) -> tuple[int, str]:
        best_decode = ""
        best_shift = 0
        max_real_words = 0
        for shift in range(26):
            decoded_string = self.apply_shift(shift) # shift only to the right
            real_words = 0
            for word in decoded_string.split(" "):
                if is_word(self.valid_words, word): real_words += 1
            if real_words > max_real_words:
                best_shift = shift
                best_decode = decoded_string
                max_real_words = real_words
        return (best_shift, best_decode)


if __name__ == '__main__':

    # Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('hello', 2)
    print('\nExpected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    # Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('\nExpected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())
    
    # Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('Do you see why?', 5)
    print('\nExpected Output: It dtz xjj bmd?')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    # Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('It dtz xjj bmd?')
    print('\nExpected Output:', (21, 'Do you see why?'))
    print('Actual Output:', ciphertext.decrypt_message())
    
    # Story String
    ciphertext = CiphertextMessage(get_story_string())
    print('\nExpected Shift:', 12)
    print('Actual Output:', ciphertext.decrypt_message())