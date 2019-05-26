from statistics import mean
from math import inf
from chess import *

player_color = None


def best_move(board, depth=5):
    global player_color
    player_color = board.turn
    best_move_yet, highest_score_yet = None, -inf
    for move, board in successors(board):
        best_move_yet, highest_score_yet = max(
            (best_move_yet, highest_score_yet),
            (move, min_score(board, depth-1, highest_score_yet, inf)),
            key=lambda x: x[1])
    return best_move_yet


def score_search_with_cut(score_search):
    def wrapper(board, depth, *args):
        return score(board) if depth == 0 or board.is_game_over() \
            else score_search(board, depth, *args)
    return wrapper


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
    return result_value(board) if board.is_game_over() else heuristic_score(board)


def result_value(board):
    return 0 if draw(board.result()) else 1 if win(board.result()) else -1


def draw(result):
    return result == "1/2-1/2"


def win(result):
    return (result == "1-0" and player_color == WHITE) or \
        (result == "0-1" and player_color == BLACK)


def heuristic_score(board):
    return mean((material_heuristic(board), space_heuristic(board)))


def heuristic(heuristic_func):
    def wrapper(board):
        return heuristic_value(heuristic_func(board, player_color), heuristic_func(board, not player_color))

    def heuristic_value(player_value, opponent_value):
        return (player_value - opponent_value) / (player_value + opponent_value)
    return wrapper


@heuristic
def material_heuristic(board, color):
    PIECE_TYPE_VALUES = {
        KING:   20000,
        QUEEN:  900,
        ROOK:   500,
        BISHOP: 330,
        KNIGHT: 320,
        PAWN:   100,
    }
    return sum(PIECE_TYPE_VALUES[piece.piece_type] for piece in board.piece_map().values()
               if piece.color == color)


@heuristic
def space_heuristic(board, color):
    return sum(len(board.attacks(square)) for square, piece
               in board.piece_map().items() if piece.color == color)


game = Board()
turn = 1
while not game.is_game_over():
    print(game.unicode(invert_color=True))
    move = best_move(game, 4)
    print("Turn:", turn, "White:" if player_color else "Black:", move)
    game.push(move)
    turn += 1
if game.is_checkmate():
    print("checkmate")
if game.is_stalemate():
    print("stalemate")
if game.is_insufficient_material():
    print("insufficient material")
if game.is_seventyfive_moves():
    print("is seventyfive moves")
if game.is_fivefold_repetition():
    print("fivefold repetition")
if game.is_variant_end():
    print("variant end")
