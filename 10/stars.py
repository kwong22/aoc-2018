#!/usr/bin/python

import re

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

import utils

def retrieve_values(info):
    '''
    Retrieve values from a specifically-formatted string

    Input:
    - info: a string with a specific format

    Output:
    - list of integers contained in the string
    '''
    pattern = r'position=<([\s\-\d]+), ([\s\-\d]+)> velocity=<([\s\-\d]+), ([\s\-\d]+)>'
    return [int(x) for x in re.findall(pattern, info)[0]]

def align_stars(data, threshold=50):
    '''
    Find the alignment of stars that results in a visible message

    Input:
    - data: list of strings specifying position and velocity of the stars
    - threshold: an estimate of the height of letters, determines when to start
      plotting the stars. Default value is 50

    Outputs:
    - plots of the stars, labeled with the number of seconds that have elapsed
    - time_elapsed: number of seconds that have elapsed
    '''
    x_pos, y_pos, x_vel, y_vel = [], [], [], []

    # Read positions and velocities
    for d in data:
        values = retrieve_values(d)

        x_pos.append(values[0])
        y_pos.append(values[1])
        x_vel.append(values[2])
        y_vel.append(values[3])

    found = False # Found an arrangement of stars within the threshold

    time_elapsed = 0

    while True:
        # Update positions
        for i in range(len(x_pos)):
            x_pos[i] += x_vel[i]
            y_pos[i] += y_vel[i]

        time_elapsed += 1

        y_diff = max(y_pos) - min(y_pos)

        if y_diff < threshold:
            found = True

            plot_positions(x_pos,
                    [-y for y in y_pos],
                    'plot%d.png' % time_elapsed)

        # Stop looking when threshold has been met and is now being exceeded
        if found and y_diff > threshold:
            break

    return time_elapsed

def plot_positions(x_pos, y_pos, name):
    plt.figure(1)
    plt.scatter(x_pos, y_pos)
    plt.savefig(name)

if __name__ == '__main__':
    lines = utils.read_lines_from_file('input.txt')
    align_stars(lines)

