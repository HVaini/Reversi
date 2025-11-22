import random, copy
from reversi.board import valid_moves, play_move, get_opponent, end_game, count_points, empty_slot

def minimax_endscore(board, player, alpha=-999999, beta=999999):
    #käy kaikki jäljellä olevat siirrot pelin loppuun ja optimoi pistemäärän
    if end_game(board):
        b, w = count_points(board)
        return b - w, None

    moves = valid_moves(board, player)
    if not moves:
        opp = get_opponent(player)
        val, _ = minimax_endscore(copy.deepcopy(board), opp, -beta, -alpha)
        return -val, None

    best_val = -65
    best_move = None
    for m in moves:
        b2 = copy.deepcopy(board)
        play_move(b2, m, player)
        opp = get_opponent(player)

        # kutsu vaihdettuna alpha/beta
        val, _ = minimax_endscore(b2, opp, -beta, -alpha)
        val = -val

        if val > best_val:
            best_val = val
            best_move = m

        # alpha–beta karsinta
        if best_val >= beta:
            return best_val, best_move

        # päivitetään alpha
        alpha = max(alpha, best_val)


    return best_val, best_move