from minimax import minimax as _minimax

"""
The game starts with 13 objects. Players take turns removing 1, 2, or 3 objects
from the pile. The player that takes the last object loses.

'state' will be an integer indicating how many items are on the pile.
players will be represented by the integers 1 and -1.
"""

def get_next_moves(state, player):
    return dict((n, state - n) for n in range(1, min(3, state) + 1))


def get_final_score(state, player):
    if state == 0:
        return -1
    else:
        return None


def minimax(state, player):
    return _minimax(state, get_next_moves, get_final_score, player)
