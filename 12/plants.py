#!/usr/bin/python

import utils

def read_initial_state(line):
    '''
    Create initial state from a string

    Input:
    - line: string containing '#' and '.'

    Output:
    - state: set of indices representing location of each '#'
    '''
    state = set() # unordered collection of unique elements

    for i in range(len(line)):
        if line[i] == '#':
            state.add(i)

    return state

def create_rules(notes):
    '''
    Create rules from a list of notes

    Input:
    - notes: list of strings

    Output:
    - rules: set of patterns that result in '#'
    '''
    rules = set()

    for note in notes:
        parsed = note.split(' ')

        if parsed[2] == '#':
            rules.add(parsed[0])

    return rules

def run_generations(state, rules, num_generations=1):
    '''
    Run generations on the state based on the rules

    Inputs:
    - state: set of indices representing location of each '#'
    - rules: set of patterns that result in '#'
    - num_generations: number of generations to run. Default is 1

    Output:
    - set of indices representing location of each '#' in the last generation
    '''
    for _ in range(num_generations):
        next_state = set()

        for i in range(min(state) - 2, max(state) + 3):
            # Build around current index
            window = []
            for j in range(i - 2, i + 3):
                if j in state:
                    window.append('#')
                else:
                    window.append('.')
            window = ''.join(window)

            # Check if window results in '#'
            if window in rules:
                next_state.add(i)

        state = next_state

    return state

def part_one(lines):
    '''
    Solve part one
    '''
    state = read_initial_state(lines[0].split(' ')[2])
    rules = create_rules(lines[2:])
    out = run_generations(state, rules, num_generations=20)

    return sum(out)

def part_two(lines):
    '''
    Solve part two
    '''
    state = read_initial_state(lines[0].split(' ')[2])
    rules = create_rules(lines[2:])
    out = run_generations(state, rules, num_generations=1000)

    return sum(out) + 91 * (50000000000 - 1000)

if __name__ == '__main__':
    lines = utils.read_lines_from_file('input.txt')
    print(part_one(lines))
    print(part_two(lines))

