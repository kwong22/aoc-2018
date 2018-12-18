#!/usr/bin/python

from collections import deque

def calculate_high_score_naive(num_players, last_marble):
    '''
    Calculate the high score obtained in a game of marbles with a specified
    number of players and the value of the last marble played
    This first version uses a list to store the marbles, but insertions and
    deletions are very inefficient.

    Inputs:
    - num_players: number of players
    - last_marble: value of the last marble played in the game

    Output:
    - highest score obtained in the game by any player
    '''
    marbles = [0]
    scores = [0] * num_players

    curr_idx = 0
    curr_player = 0

    marble_value = 1

    while marble_value < last_marble:
        # Current player scores points if marble value is multiple of 23
        if marble_value % 23 == 0:
            scores[curr_player] += marble_value

            idx = (curr_idx - 7) % len(marbles)
            scores[curr_player] += marbles.pop(idx)

            curr_idx = idx % len(marbles)
        else:
            idx = (curr_idx + 2) % len(marbles)

            marbles.insert(idx, marble_value)

            curr_idx = idx

        curr_player = (curr_player + 1) % num_players
        marble_value += 1

    return max(scores)

def calculate_high_score(num_players, last_marble):
    '''
    Calculate the high score obtained in a game of marbles with a specified
    number of players and the value of the last marble played
    This modified version uses a deque to store the marbles, taking advantage of
    the rotate function to do constant-time insertions and deletions at the end
    of the deque.

    Inputs:
    - num_players: number of players
    - last_marble: value of the last marble played in the game

    Output:
    - highest score obtained in the game by any player
    '''
    marbles = deque([0]) # Current marble will always be last in the deque
    scores = [0] * num_players

    curr_player = 0

    marble_value = 1

    while marble_value < last_marble:
        # Current player scores points if marble value is multiple of 23
        if marble_value % 23 == 0:
            scores[curr_player] += marble_value

            marbles.rotate(7)
            scores[curr_player] += marbles.pop()

            marbles.rotate(-1)
        else:
            marbles.rotate(-1)
            marbles.append(marble_value)

        curr_player = (curr_player + 1) % num_players
        marble_value += 1

    return max(scores)

if __name__ == '__main__':
    print(calculate_high_score(479, 71035))
    print(calculate_high_score(479, 7103500))

