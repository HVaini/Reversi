from AI.minimax_midgame import minimax_midgame
from AI.evaluate import evaluate
from AI.minimax_endscore import minimax_endscore
from reversi.board import (
    new_board, print_board, play_move, valid_moves,
    get_opponent, black_piece, white_piece,
    count_points, end_game, empty_slot
)
import random, copy

def ai_move(board, player):
    empty_count = sum(row.count(empty_slot) for row in board)
    moves = valid_moves(board, player)
    if not moves:
        return None

    # kutsutaan loppupelin pisteratkaisin, mielestäni tämä on perusteltu osa koska ihminenkin pystyy laskemaan tässä vaiheessa pisteitä ja
    # tämä antaa absoluuttisesti parhaan tuloksen
    if empty_count <= 7:
        val, best = minimax_endscore(copy.deepcopy(board), player)
        print(f"[Endgame]Tekoälyn arvio: {val}")
        print(f"[Endgame]Tekoälyn siirto: {best}")
        return best

    # kutsutaan midgame-heuristiikkaa käyttävä minimax jos peli ei ole loppuvaiheessa
    elif empty_count <= 60:
        val, best = minimax_midgame(copy.deepcopy(board), player, depth=5, evaluate=evaluate, alpha=-999999, beta=999999)
        print(f"[Midgame] Tekoälyn arvio: {val}")
        print(f"[Midgame] Tekoälyn siirto: {best}")
        return best

    # vaikkakin tämä on ilmeisen tarpeeton niin se on varmuuden vuoksi mukana jotta missään ennakoimattomassa tapauksessakaan
    # siirto ei jää jumiin
    else:
        move = random.choice(moves)
        print(f"[Random] Tekoälyn siirto: {move}")
        return move