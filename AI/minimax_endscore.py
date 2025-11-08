import random, copy
from reversi.board import valid_moves, play_move, get_opponent, end_game, count_points, empty_slot

def minimax_endscore(board, player):
    #käy kaikki jäljellä olevat siirrot pelin loppuun ja optimoi pistemäärän, ei vielä alpha-betaa
    #koska tahdon rakentaa tämän vaiheittain ja lisäten elementtejä vähän kerrallaan
    if end_game(board):
        b, w = count_points(board)
        return b - w, None

    moves = valid_moves(board, player)
    if not moves:
        opp = get_opponent(player)
        val, move = minimax_endscore(copy.deepcopy(board), opp)
        return -val, None

    best_val = -65
    best_move = None
    for m in moves:
        b2 = copy.deepcopy(board)
        play_move(b2, m, player)
        val, move = minimax_endscore(b2, get_opponent(player))
        val = -val
        if val > best_val:
            best_val, best_move = val, m


    #tehdään tähän myöhemmin vielä sellainen vaihtoehto että jos paras tulos on tappiollinen niin ei optimoida tulosta vaan
    #pyritään tekemään siirto joka pitää mahdollisimman monta voittavaa optiota avoinna jos vastus ei minimoi täydellisesti


    return best_val, best_move