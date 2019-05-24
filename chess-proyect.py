from math import inf
import chess

def best_move(board, depth=6):
    best_move_yet, highest_score_yet = None, -inf
    for move, board in successors(board):
        best_move_yet, highest_score_yet = max((best_move_yet, highest_score_yet), (move, min_score(board, depth-1, highest_score_yet, inf)), key=lambda x: x[1])
    return best_move_yet

def score_search_with_cut(score_search):
    def wrapper(board, depth, *args):
        return score(board) if depth == 0 or board.is_game_over() else score_search(board, depth, *args)
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
    return value

def successors(board):
    return ((move, board_after_move(move, board)) for move in board.legal_moves)

def board_after_move(move, board):
    new_board = board.copy()
    new_board.push(move)
    return new_board

def score(board):
    return result_value(board) if board.is_game_over() else material_heuristic(board)

def result_value(board):
    return 0 if draw(board.result()) else 1 if win(board.result(), board.turn) else -1

def draw(result):
    return result=="1/2-1/2"

def win(result, color):
    return (result=="1-0" and color==chess.WHITE) or (result=="0-1" and color==chess.BLACK)

def material_heuristic(board):
    white_material = material_value(board, chess.WHITE)
    black_material = material_value(board, chess.BLACK)
    return (white_material - black_material) if board.turn else (black_material - white_material)/(white_material + black_material)

def material_value(board, color):
    PIECE_TYPE_VALUES = {
        chess.PAWN: 1,
        chess.KING: 1.7,
        chess.KNIGHT: 2.5,
        chess.BISHOP: 3,
        chess.ROOK: 4.7,
        chess.QUEEN: 7.7,
    }
    return sum(PIECE_TYPE_VALUES[piece.piece_type] for piece in board.piece_map().values() if piece.color == color)

def unicode(board):
    UNICODE_PIECE_SYMBOLS = {
        "r": u"|♖", "R": u"|♜",
        "n": u"|♘", "N": u"|♞",
        "b": u"|♗", "B": u"|♝",
        "q": u"|♕", "Q": u"|♛",
        "k": u"|♔", "K": u"|♚",
        "p": u"|♙", "P": u"|♟",
        "1": "| ",
        "2": "| | ",
        "3": "| | | ",
        "4": "| | | | ",
        "5": "| | | | | ",
        "6": "| | | | | | ",
        "7": "| | | | | | | ",
        "8": "| | | | | | | | ",
        "/": "|\n",
    }
    return my_strtr(board.fen(), UNICODE_PIECE_SYMBOLS)

def my_strtr(cadena, reemplazo):
    import re
    regex = re.compile("(%s)" % "|".join(map(re.escape, reemplazo.keys())))
    return regex.sub(lambda x: str(reemplazo[x.string[x.start() :x.end()]]), cadena)

board = chess.Board()
turn = 1
while not board.is_game_over():
    print("turn", turn, "white" if board.turn else "black", "material:", material_heuristic(board))
    move = best_move(board, 5)
    board.push(move)
    print(move)
    print(board_to_unicode(board))
    turn+=1
    print(board.attacks(9))
if board.is_checkmate():
    print("checkmate")
if board.is_stalemate():
    print("stalemate")
if board.is_insufficient_material():
    print("insufficient material")
if board.is_seventyfive_moves():
    print("is seventyfive moves")
if board.is_fivefold_repetition():
    print("fivefold repetition")
if board.is_variant_end():
    print("variant end")
