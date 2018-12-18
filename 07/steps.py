#!/usr/bin/python

import re

import utils

def parse_instruction(inst):
    '''
    Parse instruction into a requirement and step

    Input:
    - inst: string containing requirement and step

    Output:
    - a tuple of requirement and step
    '''
    pattern = r'Step ([A-Z]) must be finished before step ([A-Z])'
    return re.findall(pattern, inst)[0]

def build_dictionaries(instructions):
    '''
    Build dictionaries for requirements and next steps from instructions

    Input:
    - instructions: list of strings containing instructions

    Outputs:
    - reqs: dictionary of requirements
        key: name of step
        value: list of steps that must be completed before taking this one
    - next_steps: dictionary of next steps
        key: name of step
        value: list of steps that can be taken from this one
    - all_steps: list of all steps
    '''
    reqs, next_steps = {}, {}
    all_steps = []

    for inst in instructions:
        req, step = parse_instruction(inst)

        # Add step and requirement to all steps
        if req not in all_steps:
            all_steps.append(req)
        if step not in all_steps:
            all_steps.append(step)

        # Add step to requirements
        if step in reqs:
            if req not in reqs[step]:
                reqs[step].append(req)
        else:
            reqs[step] = [req]

        # Add step to next steps
        if req in next_steps:
            if step not in next_steps[req]:
                next_steps[req].append(step)
        else:
            next_steps[req] = [step]

    return reqs, next_steps, all_steps

def meets_requirements(next_step, reqs, completed):
    '''
    Return whether or not the next step can be taken based on previous steps

    Inputs:
    - next_step: the potential next step
    - reqs: dictionary of requirements for taking each step
    - completed: list of completed steps

    Output:
    - True if the next step can be taken (all requirements met)
        False otherwise
    '''
    meets_reqs = True

    if next_step in reqs:
        for req in reqs[next_step]:
            if req not in completed:
                meets_reqs = False

    return meets_reqs

def determine_order(instructions):
    '''
    Determine the order in which steps are completed if available steps are
    always taken in alphabetical order

    Input:
    - instructions: list of strings containing instructions

    Output:
    - closed: string containing the order in which steps were taken
    '''
    reqs, next_steps, all_steps = build_dictionaries(lines)
    open_list, closed_list = [], []

    # Find possible starting steps
    for step in all_steps:
        if step not in reqs:
            open_list.append(step)
    open_list.sort()

    while len(open_list) > 0:
        for i in range(len(open_list)):
            step = open_list[i]

            if meets_requirements(step, reqs, closed_list):
                closed_list.append(step)
                open_list.pop(i)

                # Add next steps to open list 
                if step in next_steps:
                    for next_step in next_steps[step]:
                        if next_step not in open_list:
                            open_list.append(next_step)
                    open_list.sort()
                break

    return ''.join(closed_list)

def calculate_completion_time(instructions, num_workers=1):
    '''
    Calculate time to complete if each step takes 60 seconds + number of seconds
    corresponding to the letter: A=1, B=2, etc.
    With multiple workers, multiple steps can be performed simultaneously

    Input:
    - instructions: list of strings containing instructions
    - num_workers: number of workers

    Output:
    - time to complete all steps
    '''
    reqs, next_steps, all_steps = build_dictionaries(lines)
    open_list, closed_list, working_list = [], [], []

    total_num_steps = len(all_steps)

    time_elapsed = 0

    # Find possible starting steps
    for step in all_steps:
        if step not in reqs:
            open_list.append(step)
    open_list.sort()

    while len(closed_list) < total_num_steps:
        # Give available workers steps to complete
        while len(working_list) < num_workers:
            # To determine whether for loop ends because of break or because
            # end of loop has been reached
            i = 0

            for _ in range(len(open_list)):
                step = open_list[i]

                if meets_requirements(step, reqs, closed_list):
                    # Assign step to a worker
                    working_list.append((step, ord(step) - ord('A') + 61))
                    open_list.pop(i)
                    break # Move on to next worker

                i += 1

            if i == len(open_list):
                # No steps in open list can be worked on. Stop searching
                break

        # Update times in working list
        for i in reversed(range(len(working_list))):
            if working_list[i][1] > 1:
                # Tuples are immutable. Create a new one to modify it
                working_list[i] = (working_list[i][0], working_list[i][1]-1)
            else:
                # Step is complete
                step = working_list[i][0]
                closed_list.append(step)
                working_list.pop(i)

                # Add next steps to open list 
                if step in next_steps:
                    for next_step in next_steps[step]:
                        if next_step not in open_list:
                            open_list.append(next_step)
                    open_list.sort()

        time_elapsed += 1

    return time_elapsed

if __name__ == '__main__':
    lines = utils.read_lines_from_file('input.txt')
    print(determine_order(lines))
    print(calculate_completion_time(lines, num_workers=5))

