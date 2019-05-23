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
    return result_value(board.result()) if board.is_game_over() else material_heuristic(board)

def result_value(result):
    return 1 if result == "1-0" else -1 if result == "0-1" else 0

PIECE_TYPE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 2.5,
    chess.BISHOP: 3,
    chess.ROOK: 4.7,
    chess.QUEEN: 7.7
}

def material_heuristic(board):
    white_material = material_value(board, chess.WHITE)
    black_material = material_value(board, chess.BLACK)
    return (white_material - black_material) / (white_material + black_material)

def material_value(board, color):
    return sum(PIECE_TYPE_VALUES[piece.piece_type] for piece in board.piece_map().values() if piece.color == color)
