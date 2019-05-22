from math import inf

def best_possible_move(board, depth):
    return (move for move in board.legal_moves if score(board_after_move(move, board)) == max_play(board, -inf, inf, 0))[0]

def board_after_move(move, board):
    new_board = board.copy(false)
    new_board.push(move)
    return new_board

def max_play(play, alpha, beta, depth):
    if depth == 0 or game_finished(play.board):
        return play, score(play.board)
    value = -inf
    for successor in successors(play.board):
        play, value = max((play, value), min_play(successor, alpha, beta, depth-1), key=lambda x: x[1])
        if value >= beta:
            return play, value
        alpha = max(alpha, value)
    return play, value

def min_play(play, alpha, beta, depth):
    if depth == 0 or game_finished(play.board):
        return play, score(play.board)
    v = inf
    for successor in successors(play.board):
        play, value = min((play, value), max_play(successor, alpha, beta, depth-1), key=lambda x: x[1])
        if value <= alpha:
            return play, value
        beta = min(beta, value)
    return play, value

def successors(board):
    return (move, board_after_move(move, board) for move in board.legal_moves)

def score(board):
    return 1
