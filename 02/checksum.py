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

def count_doubles_and_triples(ids):
    """
    Count number of IDs that have doubles or triples of letters

    Input:
    - ids: list of IDs

    Returns:
    - number of IDs with doubles of letters * those with triples of letters
    """
    num_doubles = 0
    num_triples = 0

    for curr_id in ids:
        letters = dict()

        for x in curr_id:
            if x in letters:
                letters[x] += 1
            else:
                letters[x] = 1

        found_double = False
        found_triple = False

        for letter in letters:
            if not found_double and letters[letter] == 2:
                found_double = True
                num_doubles += 1
            if not found_triple and letters[letter] == 3:
                found_triple = True
                num_triples += 1

    return num_doubles * num_triples

def find_close_pair(ids):
    """
    Find pair of IDs that differ by one letter

    Input:
    - ids: list of IDs

    Returns:
    - tuple containing pair of IDs that differ by one letter
        or None if no such pair exists
    """
    for str1 in ids:
        for str2 in ids:
            if str1 == str2:
                continue

            num_diffs = 0
            for i in range(len(str1)):
                if str1[i] != str2[i]:
                    num_diffs += 1

            if num_diffs == 1:
                return (str1, str2)

    return None

if __name__ == '__main__':
    lines = read_lines_from_file('input.txt')
    print(count_doubles_and_triples(lines))
    print(find_close_pair(lines))
