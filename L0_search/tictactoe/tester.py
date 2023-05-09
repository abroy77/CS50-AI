from tictactoe import *

def main():
    board = [['O', None, 'X'], [None, 'O', 'O'], ['X', None, 'X']]
    print(player(board))
    for action in actions(board):
        print(action)
        print(utility(result(board, action)))
    print('best move is: ', minimax(board))
    return
if __name__=="__main__":
    main()