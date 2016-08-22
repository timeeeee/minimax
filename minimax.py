#!/usr/bin/python
# -*- coding: utf-8 -*-

from operator import not_

import tictactoe


def tic_tac_toe_minimax(board, player):
    return minimax(board, tictactoe.get_next_moves, tictactoe.get_final_score,
                   player, get_next_player=not_)


def minimax(state, get_next_moves, get_final_score, player=1,
            get_next_player=lambda x: -x, depth=0):
    """
    State is a representation of the current state of the game.
    get_next_moves is a function that takes a state and a player, and returns a
      dictionary of that players possible next moves and the resulting states.
      If the game is over, the dictionary will be empty.
    get_final_score is a function that takes a state and player and returns
      the score for that player if that's a final state, or None if the game
      isn't over.
    player is the player making this move. This defaults to 1.
    get_next_player is a function that takes the current player, and returns the
      player whose turn it is next. This defaults to a function returning the
      negative of the current player, so that the players will alternate -1, 1.

    Returns the players best next move, the resulting state, and the resulting
    score.
    """
    if depth == 0:
        print "{}checking moves for player {}, state {}:".format(
            "  " * depth, player, state
        )
    next_moves = get_next_moves(state, player)
    best_next_score = float("-inf")
    next_player = get_next_player(player)
    best_move = None
    best_next_state = None
    for move in next_moves:
        if depth == 0:
            print "{}checking move {}...".format("  " * depth, move)
        next_state = next_moves[move]

        # Get score for this next state
        final_score = get_final_score(next_state, player)
        if final_score is None:  # The game wasn't over- recurse
            next_player = get_next_player(player)
            _, _, next_score = minimax(next_state, get_next_moves,
                                       get_final_score, player=next_player,
                                       get_next_player=get_next_player,
                                       depth=depth + 1)
            final_score = -next_score

        if depth == 0:
            print "{}worst score for move {} is {}".format("  " * depth, move, final_score)
        if final_score > best_next_score:
            best_next_score = final_score
            best_next_state = next_state
            best_move = move

    if depth == 0:
        print "{}... best move is {} with score {}".format("  " * depth, best_move, best_next_score)

    assert best_next_score != float("-inf")
    assert best_move is not None
    assert best_next_state is not None
    return best_move, best_next_state, best_next_score
