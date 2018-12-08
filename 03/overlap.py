#!/usr/bin/python

import re

import utils

class Claim:
    """
    Claim defining a rectangle of fabric
    """
    def __init__(self, idx, x, y, width, height):
        self.idx = int(idx)
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)

def convert_strings_to_claims(lines):
    """
    Convert list of strings into Claim objects

    Input:
    - lines: list of strings
    
    Returns:
    - list of Claims
    """
    pattern = r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)'
    temp = [re.findall(pattern, line)[0] for line in lines]
    return [Claim(*x) for x in temp]

def count_overlap(claims):
    """
    Count number of overlapping square inches of fabric

    Input:
    - claims: list of Claims

    Returns:
    - number of overlapping square inches described by the Claims
    """
    # Store number of claims describing each coordinate
    squares = {}

    for claim in claims:
        for i in range(claim.width):
            for j in range(claim.height):
                coord = (claim.x + i, claim.y + j)

                if coord in squares:
                    squares[coord] += 1
                else:
                    squares[coord] = 1

    # Count number of coordinates with overlapping claims
    num_overlap = 0

    for coord in squares:
        if squares[coord] > 1:
            num_overlap += 1

    return num_overlap

def find_non_overlap(claims):
    """
    Find the claim that does not overlap with any others

    Input:
    - claims: list of Claims

    Returns:
    - index of the claim that does not overlap with any others
        -1 if no claim was found
    """
    # Store last occupying claim at each coordinate
    squares = {}

    # Store overlap status of each claim
    overlap_statuses = {}

    for claim in claims:
        overlap_statuses[claim.idx] = False

        for i in range(claim.width):
            for j in range(claim.height):
                coord = (claim.x + i, claim.y + j)

                if coord in squares:
                    # Mark previously occupying claim as overlapping
                    overlap_statuses[squares[coord]] = True

                    # Mark current claim as overlapping
                    overlap_statuses[claim.idx] = True

                # Assign idx of current claim to this coordinate
                squares[coord] = claim.idx

    # Find the first claim that does not overlap with any others
    for idx in overlap_statuses:
        if not overlap_statuses[idx]:
            return idx

    return -1

if __name__ == '__main__':
    lines = utils.read_lines_from_file('input.txt')
    claims = convert_strings_to_claims(lines)
    print(count_overlap(claims))
    print(find_non_overlap(claims))
