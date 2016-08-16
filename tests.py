from itertools import product, permutations

from tictactoe import (
    did_player_win, did_player_win_horizontal, did_player_win_vertical,
    did_player_win_diagonal, take_turn)


def rotations(seq):
    seq = list(seq)
    for start in range(len(seq)):
        yield seq[start:] + seq[:start]


def test_rotations():
    count = 0
    l = range(20)
    for r in rotations(l):
        count += 1
        assert sorted(r) == l
    assert count == 20


def make_list_product():
    """Get list of all possible rows"""
    return product(*[[True, False, None] for _ in range(3)])


def same(seq):
    """Are all items of sequence equal?"""
    first = seq[0]
    return all(i == first for i in seq[1:])


def test_did_player_win_horizontal():
    """Test tictactoe.did_player_win_horizontal"""
    # Player "True" won top row
    for player in (True, False):
        row1 = [player, player, player]
        for row2 in make_list_product():
            for row3 in make_list_product():
                board = [row1, row2, row3]
                assert(did_player_win_horizontal(board, player))
                assert(did_player_win(board, player))
                board = [row2, row1, row3]
                assert(did_player_win_horizontal(board, player))
                assert(did_player_win(board, player))
                board = [row2, row3, row1]
                assert(did_player_win_horizontal(board, player))
                assert(did_player_win(board, player))

    # Check for false positives
    for row1 in make_list_product():
        if not same(row1):
            for row2 in make_list_product():
                if not same(row2):
                    for row3 in make_list_product():
                        if not same(row3):
                            board = [row1, row2, row3]
                            assert not did_player_win_horizontal(board, player)


def test_did_player_win_vertical():
    """Test tictactoe.did_player_win_vertical"""
    for player in [True, False]:
        for board in product(
                *[product([player],
                          [True, False, None],
                          [True, False, None])
                  for _ in range(3)]):
            assert did_player_win_vertical(board, player) is True
            assert did_player_win(board, player) is True

        for board in product(
                *[product([True, False, None],
                          [player],
                          [True, False, None])
                  for _ in range(3)]):
            assert did_player_win_vertical(board, player) is True
            assert did_player_win(board, player) is True

        for board in product(
                *[product([True, False, None],
                          [True, False, None],
                          [player])
                  for _ in range(3)]):
            assert did_player_win_vertical(board, player) is True
            assert did_player_win(board, player) is True


def test_take_turn_blocks_3():
    """Make sure minmax blocks a win immediately"""
    for player in [True, False]:
        other_player = not(player)

        # Check horizontal
        for row in rotations([player, player, None]):
            for board in rotations(
                    [row, [None, None, None], [None, None, None]]):
                block = take_turn(board, other_player)
                next_turn = take_turn(block, player)
                assert not did_player_win_horizontal(next_turn, player)
                assert not did_player_win(next_turn, player)
