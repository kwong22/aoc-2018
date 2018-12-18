#!/usr/bin/python

import utils

def convert_to_ints(line):
    '''
    Convert a long string into a list of integers

    Input:
    - line: string containing space-delimited integers

    Output:
    - list of integers
    '''
    return [int(x) for x in line.split(' ')]

def add_metadata(data, idx=0):
    '''
    Add up all metadata entries from the specified index in the data

    Inputs:
    - data: list of integers representing the input data
    - idx: current index in the data. Default value is 0

    Output:
    - sum of metadata entries from the specified index
    '''
    mdata_sum = 0

    # Read header
    num_children = data[idx] # number of child nodes
    idx += 1

    num_mdata = data[idx] # number of metadata entries
    idx += 1

    # Read child nodes
    for _ in range(num_children):
        mdata_temp, idx = add_metadata(data, idx)
        mdata_sum += mdata_temp

    # Read metadata entries
    for _ in range(num_mdata):
        mdata_sum += data[idx]
        idx += 1

    return mdata_sum, idx

def calculate_value(data, idx=0):
    '''
    Calculate value of the node at the specified index based on the following
    rules:
        If a node has no children, then its value is the sum of its metadata
        entries.
        Otherwise, its value is the sum of the values of its children referred
        to by its metadata entries (metadata entry 1 refers to 1st child, etc.)

    Inputs:
    - data: list of integers representing the input data
    - idx: current index in the data. Default value is 0

    Output:
    - value of the node at the specified index
    '''
    value_sum = 0

    # Read header
    num_children = data[idx] # number of child nodes
    idx += 1

    num_mdata = data[idx] # number of metadata entries
    idx += 1

    child_values = []

    # Read child nodes
    for _ in range(num_children):
        value_temp, idx = calculate_value(data, idx)
        child_values.append(value_temp)

    # Read metadata entries
    for _ in range(num_mdata):
        if num_children == 0:
            value_sum += data[idx]
        else:
            if data[idx] < num_children + 1:
                value_sum += child_values[data[idx]-1]
        idx += 1

    return value_sum, idx

if __name__ == '__main__':
    lines = utils.read_lines_from_file('input.txt')
    ints = convert_to_ints(lines[0])

    print(add_metadata(ints)[0])
    print(calculate_value(ints)[0])

