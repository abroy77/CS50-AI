"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    num_empty = 0
    for row in board:
        num_empty += row.count(EMPTY)

    if num_empty % 2 == 0:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row in board:
        for column in row:
            if board[row][column] is EMPTY:
                actions.add((row, column))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    assert action in actions(board)
    new_board = deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    def win_sequence(sequence):
        if sequence.count(X) == 3:
            return X
        elif sequence.count(O) == 3:
            return O
        else:
            return None

    def get_row(board, index):
        return board[index]

    def get_col(board, index):
        return [row[index] for row in board]

    # at least 5 turns need to be played in total for a win state
    num_empty = 0
    for row in board:
        num_empty += row.count(EMPTY)
    if num_empty > 4:
        return None

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
