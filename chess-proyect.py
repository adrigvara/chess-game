from math import inf

def best_move(board, depth=8):
    best_move_yet, highest_score_yet = None, -inf
    for move, board in successors(board):
        best_move_yet, highest_score_yet = max((best_move_yet, highest_score_yet), (move, min_value(board, depth-1, highest_score_yet, inf)), key=lambda x: x[1])
    return best_move_yet

def score_search_with_cut(score_search):
    def wrapper(board, depth, *args):
        return score(board) if depth == 0 or game_finished(board) else score_search(board, depth, *args)
    return wrapper;

@score_search_with_cut
def max_score(board, depth, alpha, beta):
    value = -inf
    for move, board in successors(board):
        value = max(value, min_score(board, depth-1, alpha, beta))
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value

@score_search_with_cut
def min_score(board, depth, alpha, beta):
    value = inf
    for move, board in successors(board):
        value = min(value, max_score(board, depth-1, alpha, beta))
        if value <= alpha:
            return value
        beta = min(beta, value)
    return play, value

def successors(board):
    return (move, board_after_move(move, board) for move in board.legal_moves)

def board_after_move(move, board):
    new_board = board.copy(False)
    new_board.push(move)
    return new_board

def score(board):
    return 1
