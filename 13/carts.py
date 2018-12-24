#!/usr/bin/python

import numpy as np

import utils

class Cart:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.turn_opt = 0

    def move(self):
        # 0 = right
        # 1 = up
        # 2 = left
        # 3 = down
        if self.direction == 1:
            self.y -= 1
        elif self.direction == 3:
            self.y += 1
        elif self.direction == 2:
            self.x -= 1
        elif self.direction == 0:
            self.x += 1

        return self.x, self.y

def read_map(lines):
    width = len(lines[0])
    height = len(lines)

    tracks = np.zeros((width, height), dtype=str)

    carts = []

    for j in range(height):
        line = list(lines[j])

        for i in range(width):
            if line[i] == '^':
                carts.append(Cart(i, j, 1))
                tracks[i, j] = '|'
            elif line[i] == 'v':
                carts.append(Cart(i, j, 3))
                tracks[i, j] = '|'
            elif line[i] == '<':
                carts.append(Cart(i, j, 2))
                tracks[i, j] = '-'
            elif line[i] == '>':
                carts.append(Cart(i, j, 0))
                tracks[i, j] = '-'
            else:
                tracks[i, j] = line[i]

    return tracks, carts

def move_until_crash(tracks, carts):
    '''
    Move carts along tracks until any two carts collide

    Inputs:
    - tracks: np.array representing the tracks
    - carts: list of Carts

    Output:
    - location of the first crash
    '''
    while True:
        # Sort carts by location
        carts = sorted(carts, key=lambda cart: tracks.shape[0] * cart.y + cart.x)

        for i in range(len(carts)):
            # Move cart
            nx, ny = carts[i].move()

            # Check for collision with other carts
            for j in range(len(carts)):
                if j != i:
                    if carts[j].x == nx and carts[j].y == ny:
                        return nx, ny

            # Modify cart direction
            direc = carts[i].direction

            if tracks[nx, ny] == '/':
                if direc == 1 or direc == 3:
                    carts[i].direction = (direc - 1) % 4
                elif direc == 0 or direc == 2:
                    carts[i].direction = (direc + 1) % 4

            elif tracks[nx, ny] == '\\':
                if direc == 1 or direc == 3:
                    carts[i].direction = (direc + 1) % 4
                elif direc == 0 or direc == 2:
                    carts[i].direction = (direc - 1) % 4

            elif tracks[nx, ny] == '+':
                turn_opt = carts[i].turn_opt

                if turn_opt == 0:
                    # Turn left (counter-clockwise)
                    carts[i].direction = (direc + 1) % 4
                elif turn_opt == 2:
                    # Turn right (clockwise)
                    carts[i].direction = (direc - 1) % 4

                carts[i].turn_opt = (turn_opt + 1) % 3

def move_and_remove_until_one_left(tracks, carts):
    '''
    Move carts along tracks, removing any colliding carts until there is one
    cart remaining

    Inputs:
    - tracks: np.array representing the tracks
    - carts: list of Carts

    Output:
    - location of the last cart
    '''
    removed = set()

    while True:
        # Sort carts by location
        # For some reason, I only get the correct answer when I don't sort
        #carts = sorted(carts, key=lambda cart: tracks.shape[0] * cart.y + cart.x)

        for i in range(len(carts)):
            if i in removed:
                continue

            # Move cart
            nx, ny = carts[i].move()

            # Check for collision with other carts
            for j in range(len(carts)):
                if j in removed:
                    continue

                if j != i:
                    if carts[j].x == nx and carts[j].y == ny:
                        removed.add(i)
                        removed.add(j)
                        break

            # Modify cart direction
            direc = carts[i].direction

            if tracks[nx, ny] == '/':
                if direc == 1 or direc == 3:
                    carts[i].direction = (direc - 1) % 4
                elif direc == 0 or direc == 2:
                    carts[i].direction = (direc + 1) % 4

            elif tracks[nx, ny] == '\\':
                if direc == 1 or direc == 3:
                    carts[i].direction = (direc + 1) % 4
                elif direc == 0 or direc == 2:
                    carts[i].direction = (direc - 1) % 4

            elif tracks[nx, ny] == '+':
                turn_opt = carts[i].turn_opt

                if turn_opt == 0:
                    # Turn left (counter-clockwise)
                    carts[i].direction = (direc + 1) % 4
                elif turn_opt == 2:
                    # Turn right (clockwise)
                    carts[i].direction = (direc - 1) % 4

                carts[i].turn_opt = (turn_opt + 1) % 3

        if len(removed) == len(carts) - 1:
            # Find and return the last remaining cart
            for k in range(len(carts)):
                if k not in removed:
                    return carts[k].x, carts[k].y

def draw_window(tracks, cart, window=3):
    for j in range(max(0, cart.y - window), min(tracks.shape[1], cart.y + window)):
        line = []

        for i in range(max(0, cart.x - window), min(tracks.shape[0], cart.x + window)):
            if i == cart.x and j == cart.y:
                if cart.direction == 0:
                    line.append('>')
                elif cart.direction == 1:
                    line.append('^')
                elif cart.direction == 2:
                    line.append('<')
                elif cart.direction == 3:
                    line.append('v')
            else:
                line.append(tracks[i, j])

        print(''.join(line))

    print('*')

if __name__ == '__main__':
    lines = utils.read_lines_from_file('input.txt')
    tracks, carts = read_map(lines)
    print(move_until_crash(tracks, carts))

    # Reset the carts
    _, carts = read_map(lines)
    print(move_and_remove_until_one_left(tracks, carts))

