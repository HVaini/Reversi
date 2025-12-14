from AI.minimax_midgame import minimax_midgame
from AI.evaluate import evaluate
from AI.minimax_endscore import minimax_endscore
from AI.iterative_deepening_midgame import iterative_deepening_midgame
from reversi.board import valid_moves, empty_slot
import random, copy

def evaluate_normal(board, player):
    """
    Oletusheuristiikka keskipeliin.
    Painottaa enemmän positioarvoa.
    """
    return evaluate(board, player, weight=5)

def evaluate_longshot(board, player):
    """
    Tappiollisessa loppupeli-tilanteeessa kutsuttava heuristiikka.
    Pyrkii tekemään pelistä monimutkaisempaa ja lisäämään omien
    vaihtoehtojen määrää jotta jatkossa löytyy voitollinen linja.
    """
    return evaluate(board, player, weight=1)


def ai_move(board, player):
    """
    AI:n logiikkaa kontrolloiva funktio, joka valitsee pelitilanteen mukaan
    käytettävän heuristiikan.
    
    :param board: Pelilaudan tilanne
    :param player: Vuorossa oleva pelaaja
    :return: siirto
    """
    empty_count = sum(row.count(empty_slot) for row in board)
    moves = valid_moves(board, player)
    if not moves:
        return None

    # 10 siirron kohdalla koko loppupeli pystytään ratkaisemaan täydellisesti ilman viivettä
    if empty_count <= 10:
        val, best = minimax_endscore(copy.deepcopy(board), player)
        print(f"[Endgame]Tekoälyn arvio: {val}")
        print(f"[Endgame]Tekoälyn siirto: {best}")


        # jos minimax_endgame antaa negatiivisen arvon niin sen sijaan että hävittäisiin mahdollisimman pienin lukemin, käytetään heuristiikkaa
        # painotuksilla joka lisää monimutkaisuutta ja vaihtoehtoja ja toivotaan vastustajan virhettä.
        if val < 0:
            print("[Risk mode] Endgame-minimax ennustaa tappion, kokeillaan heuristista hakua.")
            val_longshot, best_longshot = minimax_midgame(
                copy.deepcopy(board),
                player,
                depth=4,
                evaluate=evaluate_longshot,
            )
            if best_longshot is not None:
                print(f"[Risk mode] Heuristinen arvio: {val_longshot}")
                print(f"[Risk mode] Valittu riskisiirto: {best_longshot}")
                return best_longshot


        return best

    # kutsutaan iteratiivisen syventämisen kautta midgame-heuristiikkaa käyttävä minimax jos peli ei ole loppuvaiheessa
    elif empty_count <= 60:
        val, best, reached = iterative_deepening_midgame(copy.deepcopy(board), player, evaluate=evaluate_normal, time_limit = 2, max_depth = 60)
        print(f"[Midgame] Tekoälyn arvio: {val}")
        print(f"[Midgame] Tekoälyn siirto: {best}")
        return best

    # varmuuden vuoksi mukana jotta missään ennakoimattomassa tapauksessakaan
    # siirto ei jää jumiin
    else:
        move = random.choice(moves)
        print(f"[Random] Tekoälyn siirto: {move}")
        return move