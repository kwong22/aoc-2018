#!/usr/bin/python

import re

import utils

def sort_records(records):
    '''
    Sort records in chronological order

    Input:
    - records: list of records

    Output:
    - list of records in chronological order
    '''
    pattern = r'\[(.*)\]'
    return sorted(records, key=lambda record: re.findall(pattern, record)[0])

def count_sleep(records):
    '''
    Count the minutes that each guard spends asleep

    Input:
    - records: list of records of guard activity

    Output:
    - tuple of:
        - dictionary of total number of minutes spent asleep for each guard
            key: guard ID
            value: total number of minutes spent asleep
        - dictionary of specific minutes spent asleep for each guard
            key: guard ID
            value: dictionary containing number of times spent asleep for each
            minute of the hour
    '''
    total_minutes = {} # total number of minutes spent asleep for each guard
    
    minutes_asleep = {} # specific minutes spent asleep for each guard

    sorted_records = sort_records(records)

    curr_guard = -1
    start_sleep = -1
    is_asleep = False

    for record in sorted_records:
        if 'Guard' in record:
            curr_guard = int(re.findall(r'#(\d+)', record)[0])
            is_asleep = False
        elif 'falls' in record:
            if curr_guard != -1:
                # Always midnight hour (00), so only the minutes matter
                start_sleep = int(re.findall(r':(\d\d)', record)[0])
                is_asleep = True
            else:
                raise ValueError('No guard is at the post.')
        elif 'wakes' in record:
            if is_asleep:
                # Always midnight hour (00), so only the minutes matter
                end_sleep = int(re.findall(r':(\d\d)', record)[0])

                # Add to total number of minutes spent asleep
                duration = end_sleep - start_sleep
                if curr_guard in total_minutes:
                    total_minutes[curr_guard] += duration
                else:
                    total_minutes[curr_guard] = duration

                # Keep track of specific minutes spent asleep
                if curr_guard not in minutes_asleep:
                    # Create new dictionary to store specific minutes
                    minutes_asleep[curr_guard] = {}

                for i in range(start_sleep, end_sleep):
                    if i in minutes_asleep[curr_guard]:
                        minutes_asleep[curr_guard][i] += 1
                    else:
                        minutes_asleep[curr_guard][i] = 1
            else:
                raise ValueError('Guard is already awake.')

    return (total_minutes, minutes_asleep)

def find_greatest_quantity_slept(total_minutes, minutes_asleep):
    '''
    Solve part one
    '''
    # Find ID of guard with the most minutes spent asleep
    max_id = max(total_minutes, key=total_minutes.get)

    # Find the specific minute in which the guard spent the most time asleep
    max_minute = max(minutes_asleep[max_id], key=minutes_asleep[max_id].get)

    return max_id * max_minute

def find_greatest_frequency_slept(minutes_asleep):
    '''
    Solve part two
    '''
    max_guard = -1
    max_minute = -1
    max_freq = -1

    for guard in minutes_asleep:
        for minute in minutes_asleep[guard]:
            if minutes_asleep[guard][minute] > max_freq:
                max_guard = guard
                max_minute = minute
                max_freq = minutes_asleep[guard][minute]

    return max_guard * max_minute

if __name__ == '__main__':
    lines = utils.read_lines_from_file('input.txt')
    count_out = count_sleep(lines)
    print(find_greatest_quantity_slept(*count_out))
    print(find_greatest_frequency_slept(count_out[1]))
    
