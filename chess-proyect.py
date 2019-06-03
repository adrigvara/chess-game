from argparse import ArgumentParser
from math import inf
from chess import *
from time import time

ai_color = None


def best_move(board, depth):
    global ai_color
    ai_color = board.turn
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
    return (result == "1-0" and ai_color == WHITE) or \
        (result == "0-1" and ai_color == BLACK)


def heuristic_score(board):
    HEURISTIC_TABLE = {
        material_heuristic: 0.75,
        space_heuristic: 0.25,
    }
    return sum(heuristic_weight*heuristic_value(board) for heuristic_value, heuristic_weight
               in HEURISTIC_TABLE.items())


def heuristic(heuristic_func):
    def wrapper(board):
        return heuristic_value(heuristic_func(board, ai_color), heuristic_func(board, not ai_color))

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


def play_chess(player_color, depth):
    turn = 1
    board = Board()
    while not board.is_game_over():
        view_board(board)
        time1 = time()
        move = next_move(board, player_color, depth)
        time2 = time()
        print("Turn:", turn, "White:" if ai_color else "Black:", move, "Time:", time2-time1)
        board.push(move)
        turn += 1
    view_board(board)
    if board.is_checkmate():
        print("checkmate")
    if board.is_stalemate():
        print("stalemate")
    if board.is_insufficient_material():
        print("insufficient material")
    if board.is_seventyfive_moves():
        print("seventyfive moves")
    if board.is_fivefold_repetition():
        print("fivefold repetition")
    if board.is_variant_end():
        print("variant end")


def view_board(board):
    print(board.unicode(invert_color=True, borders=True))


def next_move(board, player_color, depth):
    return player_move(board) if player_color == board.turn else best_move(board, depth)


def player_move(board):
    while True:
        try:
            str = input("player move: ")
            move = Move.from_uci(str)
        except ValueError:
            print(str, "is not a move")
            continue
        if move not in board.legal_moves:
            print(move, "is not a legal move")
        else:
            break
    return move


def str_to_color(str):
    if str.lower() in ('white', 'w'):
        return WHITE
    elif str.lower() in ('black', 'b'):
        return BLACK


parser = ArgumentParser(description="Chess game in terminal environment")
parser.add_argument('-c', '--color', '--player-color', dest='color', type=str_to_color, required=False, default=None,
                    help='color for the player (default=None)')
parser.add_argument('-d', '--depth', '--search-depth', dest='depth', type=int, required=False, default=4,
                    help='depth of search for the best movement for artificial intelligence (default=4)')
args = parser.parse_args()
play_chess(args.color, args.depth)
