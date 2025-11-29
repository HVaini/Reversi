import copy
from reversi.board import valid_moves, play_move, get_opponent
from AI.reorder import reorder_moves

def minimax_midgame(board, player, depth, evaluate, alpha=-999999, beta=999999, hash_moves=None):

    #sama minimax logiikka kuin minimax_endgamessa, alpha beta lisätty

    if hash_moves is None:
        hash_moves = {}

    key = hash(str(board) + player)

    if depth == 0:
        return evaluate(board, player), None

    moves = valid_moves(board, player)

    # Ei siirtoja, käännetään arvo
    if not moves:
        opp = get_opponent(player)
        val, _ = minimax_midgame(copy.deepcopy(board), opp, depth - 1, evaluate, -beta, -alpha, hash_moves)
        return -val, None

    # esijärjestetyt siirrot parhaista huonoimpiin
    moves = reorder_moves(board, player, moves)

    #haetaan onko siirto aiemmin arvioitu parhaaksi ja jos niin aloitetaan sillä
    stored = hash_moves.get(key)
    if stored in moves:
        moves.remove(stored)
        moves.insert(0, stored)
        #print(stored)

    best_val = -999999
    best_move = None

    for m in moves:
        b2 = copy.deepcopy(board)
        play_move(b2, m, player)

        opp = get_opponent(player)

        val, _ = minimax_midgame(b2, opp, depth - 1, evaluate, -beta, -alpha, hash_moves)
        val = -val 

        if val > best_val:
            best_val = val
            best_move = m

        # alpha-beta karsinta, minimoiva vastustaja lukitsee haaran, loput karsitaan
        if best_val >= beta:
            hash_moves[key] = best_move
            return best_val, best_move

        alpha = max(alpha, best_val)
    
    if best_move is not None:
        hash_moves[key] = best_move

    return best_val, best_move
