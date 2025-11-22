import copy
from reversi.board import valid_moves, play_move, get_opponent
from AI.reorder import reorder_moves

def minimax_midgame(board, player, depth, evaluate, alpha=-999999, beta=999999):
    #sama minimax logiikka kuin minimax_endgamessa, alpha beta lisätty
    if depth == 0:
        return evaluate(board, player), None

    moves = valid_moves(board, player)

    # Ei siirtoja, käännetään arvo
    if not moves:
        opp = get_opponent(player)
        val, _ = minimax_midgame(copy.deepcopy(board), opp, depth - 1, evaluate, -beta, -alpha)
        return -val, None

    # esijärjestetyt siirrot parhaista huonoimpiin
    moves = reorder_moves(board, player, moves)

    best_val = -999999
    best_move = None

    for m in moves:
        b2 = copy.deepcopy(board)
        play_move(b2, m, player)

        opp = get_opponent(player)

        val, _ = minimax_midgame(b2, opp, depth - 1, evaluate, -beta, -alpha)
        val = -val 

        if val > best_val:
            best_val = val
            best_move = m

        # alpha-beta karsinta, minimoiva vastustaja lukitsee haaran, loput karsitaan
        if best_val >= beta:
            return best_val, best_move

        alpha = max(alpha, best_val)

    return best_val, best_move
