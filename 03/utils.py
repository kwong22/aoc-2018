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
