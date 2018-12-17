#!/home/kwong/anaconda3/bin/python

from collections import deque

import utils

def opposite_polarity(x, y):
    '''
    Check if characters x and y are uppercase and lowercase versions of the same
    letter

    Inputs:
    - x: a character
    - y: a character
    
    Output:
    - True if x and y are uppercase and lowercase versions of the same letter
        False otherwise
    '''
    return abs(ord(x) - ord(y)) == 32

def react_polymer(sequence):
    '''
    React polymer such that adjacent units of the same type (same letter) and
    opposite polarity (one uppercase, the other lowercase) are destroyed

    Input:
    - sequence: string containing the sequence of the polymer

    Output:
    - number of units in the resulting polymer
    '''
    # Convert sequence to deque (double-ended queue) of characters
    remaining_units = deque(sequence)

    # Add 2 units to the working list
    working_units = deque(remaining_units.popleft())
    working_units.append(remaining_units.popleft())

    # Track whether or not the top 2 units react
    no_reaction = False # The top 2 units may react

    while len(remaining_units) > 0 or not no_reaction:
        if len(working_units) > 1:
            # Check the top 2 units in the working list
            y = working_units.pop()
            x = working_units.pop()

            if not opposite_polarity(x, y):
                # Add back in the units that were removed to be checked
                no_reaction = True # The top 2 units did not react
                working_units.append(x)
                working_units.append(y)

                # If possible, add another unit to the top of the working list
                if len(remaining_units) > 0:
                    working_units.append(remaining_units.popleft())
                    no_reaction = False # The top 2 units may react
        else:
            # If working list does not have enough units to compare, add
            # another one if possible
            if len(remaining_units) > 0:
                working_units.append(remaining_units.popleft())
                no_reaction = False # The top 2 units may react
            else:
                # Otherwise working list remains too small, and no more
                # reactions are possible
                no_reaction = True

    return len(working_units)

def find_problem_unit(sequence):
    '''
    Find the unit (letter) that, when removed, results in the shortest polymer

    Input:
    - sequence: string containing the sequence of the polymer

    Output:
    - number of units in the shortest polymer
    '''
    min_len = len(sequence) 

    for i in range(ord('A'), ord('Z')+1):
        # Remove instances of both uppercase and lowercase versions of letter
        new_seq = sequence.replace(chr(i), '').replace(chr(i+32), '')

        length = react_polymer(new_seq)
        if length < min_len:
            min_len = length

    return min_len

if __name__ == '__main__':
    lines = utils.read_lines_from_file('input.txt')
    print(react_polymer(lines[0]))
    print(find_problem_unit(lines[0]))

