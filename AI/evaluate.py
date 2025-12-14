from reversi.board import valid_moves, get_opponent

# painoarvo-matriisi, perustuu yleisiin Reversi-heuristiikkoihin,
# mutta skaalattuna ja muokattuna juuri tähän heuristiikkakehykseen sopivaksi
V = [
    [ 25, -9,  12,  7,  7,  12, -9, 25 ],
    [ -9, -12, 1,   1,  1,  1, -12, -9 ],
    [ 12,  1,  2,   2,  2,  2,  1,  12 ],
    [ 7,   1,  2,   1,  1,  2,  1,   7 ],
    [ 7,   1,  2,   1,  1,  2,  1,   7 ],
    [ 12,  1,  2,   2,  2,  2,  1,  12 ],
    [ -9, -12, 1,   1,  1,  1, -12, -9 ],
    [ 25, -9,  12,  7,  7,  12, -9, 25 ]
]


# Kulman vierusruutujen bonus, kun kulma on pelaajalla 
SAFE_CORNER_BONUS = 20

# Määritellään kulmien läheiset ruudut
SAFE_SETS = {
    (0,0): [(0,1),(1,0),(1,1)],
    (0,7): [(0,6),(1,7),(1,6)],
    (7,0): [(6,0),(7,1),(6,1)],
    (7,7): [(6,7),(7,6),(6,6)]
}

def evaluate(board, player, weight):
    """
    Kolmiosainen arviointiheuristiikka jonka avulla määritellään pelitilanteen arvo.
    (Mobility, Positio ja kulmabonus)
    
    :param board: Pelilaudan tilanne
    :param player: Vuorossa oleva pelaaja jonka näkökulmasta tilanne arvioidaan
    :param weight: Painokerroin mobilityn ja arvomatriisin tasapainotukseen
    :return: pelitilanteen arvo numerollisesti esitettynä
    """
    opponent = get_opponent(player)

    # 1. Mobility arvioi pelaajan omien siirtovaihtoehtojen määrää
    my_moves = len(valid_moves(board, player))
    opp_moves = len(valid_moves(board, opponent))
    mobility_score = my_moves - opp_moves

    # 2. painomatriisi, perustuen strategisiin arvioihin eri ruutujen merkityksestä
    positional_score = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                positional_score += V[r][c]
            elif board[r][c] == opponent:
                positional_score -= V[r][c]

    # 3. kun kulma on omassa hallussa niin alkuperäinen matriisi ei ole sopiva, lisätään vierusruutuihin bonus
    # korvaa yleistä Reversin stability-heuristiikkaa
    # koska kyseinen tilanne on lähes poikkeuksetta aivan loppupelissä niin bonusta ei ole tarpeen 
    # laajentaa leveämmälle alueelle koska tilanne käsitellään minimax_endscoressa 
    for corner, neighs in SAFE_SETS.items():
        cr, cc = corner
        if board[cr][cc] == player:
            for (r, c) in neighs:
                if board[r][c] == player:
                    positional_score += SAFE_CORNER_BONUS
                elif board[r][c] == opponent:
                    positional_score -= SAFE_CORNER_BONUS

    # yhdistetty arvio joka palauttaa siirron pisteet painotettuna
    return mobility_score + positional_score * weight
