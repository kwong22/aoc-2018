#!/usr/bin/python

import numpy as np

def compute_cell_power(x, y, serial_num):
    '''
    Compute the power level of a single fuel cell

    Inputs:
    - x: X-coordinate of the fuel cell in the grid (starts at 1)
    - y: Y-coordinate of the fuel cell in the grid (starts at 1)
    - serial_num: serial number of the grid containing the fuel cell

    Output:
    - power: the power level of the fuel cell

    '''
    power = ((x + 10) * y + serial_num) * (x + 10)
    power = int(power / 100) % 10
    power -= 5
    return power

def compute_grid_power(serial_num):
    '''
    Compute the power level of all fuel cells in a 300x300 grid with the
    specified serial number

    Input:
    - serial_num: serial number of the grid of fuel cells

    Output:
    - grid_power: np.array of shape (300, 300)
    '''
    width = 300
    length = 300

    grid_power = np.zeros((width, length))

    for i in range(width):
        for j in range(length):
            grid_power[i, j] = compute_cell_power(i+1, j+1, serial_num)

    return grid_power

def find_largest_power(grid_power, n):
    '''
    Find the nxn square in a grid of fuel cells that has the largest total
    power

    Input:
    - grid_power: np.array of shape (300, 300) representing the power levels of
      the fuel cells in the grid
    - n: size of the square used to calculate power

    Output:
    - tuple of:
        indices of the top-left fuel cell of the square with largest power
        the power level of that square
    '''
    width = 300 - n + 1
    length = 300 - n + 1

    square_power = np.zeros((width, length))

    for i in range(width):
        for j in range(width):
            square_power[i, j] = np.sum(grid_power[i:i+n, j:j+n])

    ind = np.unravel_index(np.argmax(square_power), square_power.shape)
    return (ind[0]+1, ind[1]+1), np.amax(square_power)

def find_largest_power_and_size(grid_power):
    '''
    Find the size and coordinates of the nxn square in a grid of fuel cells
    that has the largest total power

    Input:
    - grid_power: np.array of shape (300, 300) representing the power levels of
      the fuel cells in the grid

    Output:
    - tuple of:
        X-coordinate of top-left fuel cell of square with largest power
        Y-coordinate of top-left fuel cell of square with largest power
        size of square
    '''
    results = []

    for i in range(300):
        result = find_largest_power(grid_power, n=i+1)
        results.append(result)

    # Find result with the largest power
    max_power = results[0][1]
    idx = 0

    for i in range(1, len(results)):
        if results[i][1] > max_power:
            max_power = results[i][1]
            idx = i

    return results[idx][0][0], results[idx][0][1], idx+1

if __name__ == '__main__':
    grid_power = compute_grid_power(9424)
    print(find_largest_power(grid_power, n=3))
    print(find_largest_power_and_size(grid_power))

