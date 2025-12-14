import random, copy
from reversi.board import valid_moves, play_move, get_opponent, end_game, count_points

def minimax_endscore(board, player, alpha=-999999, beta=999999):
    """
    Minimax-haku joka käy läpi kaikki jäljellä olevat siirrot ja etsii parhaan mahdollisen
    pistemäärän. Kutsutaan pelin loppupuolella kun jäljellä oleva syvyys mahdollistaa
    sen käytön.
    
    :param board: Pelilaudan tilanne
    :param player: Vuorossa oleva pelaaja
    :param alpha: Pelaajan parhaan löydetyn siirron arvo
    :param beta: Vastustajan parhaan löydetyn siirron arvo
    """
    # jos peli loppuu lasketaan pisteet
    if end_game(board):
        b, w = count_points(board)
        return b - w, None

    moves = valid_moves(board, player)
    # jos ei siirtoja, vuoro vastustajalle
    if not moves:
        opp = get_opponent(player)
        # vastustajalle alpha ja beta käänteisestä näkökulmasta
        val, _ = minimax_endscore(copy.deepcopy(board), opp, -beta, -alpha)
        return -val, None

    best_val = -65 # alustettu paras arvo, -64 on teoreettisesti huonoin mahdollinen tulos
    best_move = None
    for m in moves:
        # kopioidaan täydellinen laudan tilanne siirtoa varten
        b2 = copy.deepcopy(board)
        play_move(b2, m, player)
        opp = get_opponent(player)

        # kutsu vaihdettuna takaisin vastustajalle beta/alpha
        val, _ = minimax_endscore(b2, opp, -beta, -alpha)
        val = -val

        if val > best_val:
            best_val = val
            best_move = m

        # alpha–beta karsinta, vastustaja ei hyväksyisi haaraa, eli karsitaan
        if best_val >= beta:
            return best_val, best_move

        # päivitetään alpha
        alpha = max(alpha, best_val)


    return best_val, best_move