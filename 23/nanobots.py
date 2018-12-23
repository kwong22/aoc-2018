#!/usr/bin/python

import re

import utils

def retrieve_values(info):
    '''
    Retrieve values from a specifically-formatted string

    Input:
    - info: a string with a specific format

    Output:
    - list of integers contained in the string
    '''
    pattern = r'pos=<([\-\d]+),([\-\d]+),([\-\d]+)>, r=([\d]+)'
    return [int(x) for x in re.findall(pattern, info)[0]]

def build_dictionary(data):
    '''
    Build dictionary of nanobots with positions and ranges

    Input:
    - data: list of strings specifying position and range of each nanobot

    Output:
    - bots: dictionary of nanobot positions and ranges
        key - position (tuple of x, y, z coordinates)
        value - range
    '''
    parsed = [retrieve_values(d) for d in data]

    bots = {}

    for p in parsed:
        bots[(p[0], p[1], p[2])] = p[3]

    return bots

def find_max_range(bots):
    '''
    Find nanobot with the greatest range

    Input:
    - bots: dictionary of nanobot positions and ranges

    Output:
    - tuple of
        position (tuple of x, y, z coordinates) of nanobot with greatest range
        range of nanobot with greatest range
    '''
    max_pos = None
    max_range = -1

    for key in bots:
        if bots[key] > max_range:
            max_pos = key
            max_range = bots[key]

    return max_pos, max_range

def manhattan_dist(pos1, pos2):
    '''
    Calculate Manhattan distance between 2 positions

    Inputs:
    - pos1: first position, tuple of x, y, z
    - pos2: second position, tuple of x, y, z

    Output:
    - Manhattan distance between the 2 positions
    '''
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) + abs(pos1[2] - pos2[2]) 

def count_bots_within_max_range(data):
    '''
    Count number of nanobots within range (via Manhattan distance) of the
    nanobot with the greatest range

    Input:
    - data: list of strings specifying nanobot positions and ranges

    Output:
    - number of nanobots within range of the nanobot with the greatest range
    '''
    bots = build_dictionary(data)

    max_pos, max_range = find_max_range(bots)

    num_in_range = 0

    for key in bots:
        if manhattan_dist(key, max_pos) <= max_range:
            num_in_range += 1

    return num_in_range

if __name__ == '__main__':
    lines = utils.read_lines_from_file('input.txt')
    print(count_bots_within_max_range(lines))

