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
    for row in range(3):
        for column in range(3):
            if board[row][column] is EMPTY:
                actions.add((row, column))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action not in actions(board):
        raise Exception("Invalid action")
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

    def get_diagonal(board, index):
        if index == 0:
            return [board[0][0], board[1][1], board[2][2]]
        else:
            return [board[0][2], board[1][1], board[2][0]]

    # at least 5 turns need to be played in total for a win state
    num_empty = 0
    for row in board:
        num_empty += row.count(EMPTY)
    if num_empty > 4:
        return None

    # check rows
    for i in range(3):
        win = win_sequence(get_row(board, i))
        if win:
            return win
    # check columns
    for i in range(3):
        win = win_sequence(get_col(board, i))
        if win:
            return win
    # check diagonals
    for i in range(2):
        win = win_sequence(get_diagonal(board, i))
        if win:
            return win

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    elif not actions(board):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    def max_value(board, ab_thresh=None):
        if terminal(board):
            return utility(board)
        v = -math.inf
        for action in actions(board):
            v = max(v, min_value(result(board, action), ab_thresh=None))
            if (ab_thresh is not None) and (v > ab_thresh):
                return v
                
        return v

    def min_value(board, ab_thresh=None):
        if terminal(board):
            return utility(board)
        v = math.inf
        for action in actions(board):
            v = min(v, max_value(result(board, action), ab_thresh=None))
            if (ab_thresh is not None) and (v < ab_thresh):
                return v
        return v
    action_rewards={}
    if player(board) == X:
        for action in actions(board):

            reward = min_value(result(board, action))
            action_rewards[action] = reward
            best_action = max(action_rewards.items(), key=lambda x: x[1])
            best_action = best_action[0]
    else:
        for action in actions(board):
            reward = max_value(result(board, action))
            action_rewards[action] = reward
            best_action = min(action_rewards.items(), key=lambda x: x[1])
            best_action = best_action[0]

    return best_action

