"""
Tic Tac Toe Player
"""

import math
import copy
from random import randrange

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    numberX = 0
    numberO = 0
    for i in range(len(board)):
        for j in range(3):
            # print(board[i][j])
            if board[i][j] == "X":
                numberX += 1
            elif board[i][j] == "O":
                numberO += 1
    # print("numberx")
    # print(numberX)
    # print("numbero")
    # print(numberO)
    if numberX <= numberO:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    ans = set()
    for i in range(len(board)):
        for j in range(3):
            if board[i][j] == EMPTY:
                thistupl = (i, j)
                ans.add(thistupl)
    # print(ans)
    return ans


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newBoard = copy.deepcopy(board)
    if board[action[0]][action[1]] == None:
        if player(board) == X:
            # print("player X moved")
            newBoard[action[0]][action[1]] = "X"
        elif player(board) == O:
            # print("player O moved")
            newBoard[action[0]][action[1]] = "O"
    else:
        # print('ACTION')
        # print(action)
        raise Exception("Invalid Action!!")
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    ans = None
    for i in range(len(board)):
        if board[i][0] != None and board[i][0] == board[i][1] and board[i][0] == board[i][2]:
            if board[i][0] == "X":
                ans = X
            elif board[i][0] == "O":
                ans = O
        elif board[0][i] != None and board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            if board[0][i] == "X":
                ans = X
            elif board[0][i] == "O":
                ans = O
        elif board[0][0] != None and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
            if board[0][0] == "X":
                ans = X
            elif board[0][0] == "O":
                ans = O
        elif board[2][0] != None and board[2][0] == board[1][1] and board[1][1] == board[0][2]:
            if board[2][0] == "X":
                ans = X
            elif board[2][0] == "O":
                ans = O
    return ans


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    ans = True
    if board[0][0] != None and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[0][0] == "X":
            return True
        elif board[0][0] == "O":
            return True
    elif board[2][0] != None and board[2][0] == board[1][1] and board[1][1] == board[0][2]:
        if board[2][0] == "X":
            return True
        elif board[2][0] == "O":
            return True
    for i in range(len(board)):
        if board[i][0] != None and board[i][0] == board[i][1] and board[i][0] == board[i][2]:
            return True
        elif board[0][i] != None and board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            return True
    for i in range(len(board)):
        for j in range(3):
            if board[i][j] == None:
                ans = False
    return ans


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
    if terminal(board):
        return None

    else:
        if player(board) == X:
            bestScore = -math.inf
            bestAction = None

            for action in actions(board):
                newValue = minValue(result(board, action))

                if newValue > bestScore:
                    bestScore = newValue
                    bestAction = action

            return bestAction
        elif player(board) == O:
            bestScore = math.inf
            bestAction = None

            for action in actions(board):
                newValue = maxValue(result(board, action))

                if newValue < bestScore:
                    bestScore = newValue
                    bestAction = action

            return bestAction


def maxValue(board):
    score = -math.inf

    if terminal(board):
        # print(utility(board))
        return utility(board)

    for action in actions(board):
        score = max(score, minValue(result(board, action)))

    return score


def minValue(board):
    score = math.inf

    if terminal(board):
        # print(utility(board))
        return utility(board)

    for action in actions(board):
        score = min(score, maxValue(result(board, action)))

    return score
