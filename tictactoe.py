"""
Play tic tac toe.

Players are represented by values True (o) and False (x). Spaces are
represented by None.
"""

from copy import deepcopy

O = True
X = False
SPACE = None
CHAR_TO_PLAYER = {'o': O, 'x': X, ' ': SPACE}
PLAYER_TO_CHAR = {O: 'o', X: 'x', SPACE: " "}


def did_player_win(board, player):
    """Has 'player' won on this board?"""
    return (did_player_win_horizontal(board, player) or
            did_player_win_vertical(board, player) or
            did_player_win_diagonal(board, player))


def did_player_win_horizontal(board, player):
    """Did 'player' win horizontally on this board?"""
    for row in board:
        if all(spot == player for spot in row):
            return True
    return False


def did_player_win_vertical(board, player):
    """Did 'player' win vertically on this board?"""
    for col_index in range(3):
        if all(board[row_index][col_index] == player
               for row_index in range(3)):
            return True
    return False


def did_player_win_diagonal(board, player):
    """Did 'player' win diagonally on this board?"""
    return (all(board[i][i] == player for i in range(3)) or
            all(board[i][2 - i] == player for i in range(3)))


def is_full(board):
    """Is the game over?"""
    return all(all(s is not None for s in row) for row in board)


def minmax(board, player, depth=0):
    """Get best next move for player and its score

    Specifically, return row and col of a players best move, and and integer
    representing score: -1 if the best possible outcome for the player is a
    loss, 0 for a tie, 1 for a win.

    Use the minmax algorithm- For all open spaces, recurse to find the other
    players next move, and choose this players move to minimize the next
    players score.
    """
    best_row = None
    best_col = None
    least_next_score = float("inf")
    for row_index in range(3):
        for col_index in range(3):
            if board[row_index][col_index] == SPACE:
                # Set this space. After evaluating it we will need to unset it
                board[row_index][col_index] = player

                # If we just won, go here!
                if did_player_win(board, player):
                    board[row_index][col_index] = SPACE
                    return (row_index, col_index), 9 - depth

                # Did we draw?
                if is_full(board):
                    # This was the only option so we can just return it
                    board[row_index][col_index] = SPACE
                    return (row_index, col_index), 0

                # Otherwise recurse to get the next player's move
                _, next_score = minmax(board, not(player), depth + 1)

                if next_score < least_next_score:
                    least_next_score = next_score
                    best_row = row_index
                    best_col = col_index

                board[row_index][col_index] = SPACE

    score = -least_next_score  # because the game is zero-sum
    return (best_row, best_col), score


def naive_take_turn(board):
    """Take the first open spot"""
    new_board = deepcopy(board)
    for row in range(3):
        for col in range(3):
            if board[row][col] == SPACE:
                new_board[row][col] = X
                return new_board


def take_turn(board, player=X):
    """Return the board after o's next turn."""
    (row, col), _ = minmax(board, player)
    board = deepcopy(board)
    board[row][col] = player
    return board


def string_to_board(board_string):
    """Convert a string into 3x3 nested lists."""
    # Do some sanity checks
    if len(board_string) != 9:
        raise ValueError("Board doesn't have 9 spaces!")

    for char in board_string:
        if char not in "ox +":
            raise ValueError(
                "'{}' is not a valid character- board must be made up of x's,"
                "o's, and spaces.".format(char))

    # Is it possible x's turn?
    # If x's == o's + 1, x started, o's turn
    # If x's == o's, o started, o's turn
    # Otherwise, this is not a reasonable board
    num_xs = board_string.count('x')
    num_os = board_string.count('o')

    return [[CHAR_TO_PLAYER[board_string[row * 3 + col]] for col in range(3)]
            for row in range(3)]


def board_to_string(board):
    """Convert board to string"""
    return "".join(
        "".join(PLAYER_TO_CHAR[spot] for spot in row) for row in board)
