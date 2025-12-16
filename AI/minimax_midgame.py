import copy
from reversi.board import valid_moves, play_move, get_opponent, end_game, count_points, black_piece
from AI.reorder import reorder_moves

def minimax_midgame(board, player, depth, evaluate, alpha=-999999, beta=999999, hash_moves=None):
    """
    Pelin alku- ja keskivaiheen minimax alpha-beta-karsinnalla.
    Kutsuu heuristiikkafunktiota joka palauttaa arvon syvyydeltä.

    
    :param board: Pelilaudan tilanne
    :param player: Vuorossa oleva pelaaja
    :param depth: hakusyvyyden maksimi
    :param evaluate: Heuristiikkafunktio joka laskee pelitilanteen arvon
    :param alpha: Pelaajan parhaan löydetyn siirron arvo
    :param beta: Vastustajan parhaan löydetyn siirron arvo
    :param hash_moves: Transpositiokirjasto, tallennetaan eri asemien parhaita löydettyjä siirtoja 
    :return: palauttaa evaluate-funktion arvon parhaalle siirrolle sekä itse siirron
    """

    # Luodaan transpositiokirjasto
    if hash_moves is None:
        hash_moves = {}

    key = hash(str(board) + player)

    # jos peli päättyy millä tahansa syvyydellä niin palautettu arvo on niin suuri että se kumoaa heuristiikan
    if end_game(board):
        b, w = count_points(board)
        if player == black_piece:
            diff = b - w
        else:
            diff = w - b

        if diff == 0:
            return 0, None

        return diff * 100000, None

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

    best_val = -999999
    best_move = None

    for m in moves:
        b2 = copy.deepcopy(board)
        play_move(b2, m, player)

        opp = get_opponent(player)

        # kutsu vaihdettuna takaisin vastustajalle beta/alpha
        val, _ = minimax_midgame(b2, opp, depth - 1, evaluate, -beta, -alpha, hash_moves)
        val = -val

        if val > best_val:
            best_val = val
            best_move = m

        # alpha-beta karsinta, vastustaja ei hyväksyisi haaraa
        if best_val >= beta:
            hash_moves[key] = best_move
            return best_val, best_move

        alpha = max(alpha, best_val)
    
    # tallennetaan löydetty paras siirto tähän asemaan transpositiokirjastoon
    if best_move is not None:
        hash_moves[key] = best_move

    return best_val, best_move
