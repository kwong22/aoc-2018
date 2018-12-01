#!/usr/bin/python

def read_lines_from_file(filename):
    """
    Build a list of strings line-by-line from a file.

    Input:
    - filename: name of the file to read from

    Returns:
    - output: list of strings from the file
    """
    output = []
    with open(filename, 'r') as lines:
        for line in lines:
            line = line.replace('\n', '')
            output.append(line)

    return output

def find_repeated_frequency(ints):
    """
    Find the first frequency repeated when adding list of frequencies,
    looping through the list as needed.

    Input:
    - ints: list of integers

    Returns:
    - first frequency that is repeated
    """
    # Current frequency
    curr = 0

    # Frequencies that have been encountered
    freqs = dict()

    # Current index in list
    i = 0

    while True:
        i = i % len(ints)
        curr += ints[i]

        if curr in freqs:
            return curr
        else:
            freqs[curr] = True
            i += 1

if __name__ == '__main__':
    lines = read_lines_from_file('input.txt')
    ints = [int(line) for line in lines]
    print(find_repeated_frequency(ints))
