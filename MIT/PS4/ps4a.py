# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence: str) -> list[str]:
    if len(sequence) == 1:
        return sequence
    else:
        perms = []
        first_char = sequence[0]
        for perm in get_permutations(sequence[1:]):
            for index in range(len(perm)+1):
                new_string = perm[:index] + first_char + perm[index:]
                perms.append(new_string)
        return perms

if __name__ == '__main__':
   example_input = 'abc'
   print('Input:', example_input)
   print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
   print('Actual Output:', get_permutations(example_input))

   example_input = 'abcd'
   print('Input:', example_input)
   print('Expected Output:', ["abcd","abdc","acbd","acdb","adbc","adcb","bacd","badc","bcad","bcda","bdac","bdca","cabd","cadb","cbad","cbda","cdab","cdba","dabc","dacb","dbac","dbca","dcab","dcba"])
   print('Actual Output:', get_permutations(example_input))

