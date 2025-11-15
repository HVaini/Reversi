from reversi.board import valid_moves, get_opponent

# Painomatriisi, arvot seuraavat osin kurssisivujen linkin artikkelissa olleita, mutta skaalattuna sekä 
# sovittaen niitä paremmin omaan malliini (vaikka pystyn perustelemaan käyttämäni luvut niin kyse on kuitenkin arvioista)
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

# painokerroin jolla mobility vs matriisin painoarvot saadaan haluttuun tasapainoon, nyt painottaa matriisia 
# ajattelin tähän vielä ehkä dynaamista painotusta joka muuttuu vuorojen edetessä 
heuristic_weight = 5  

# Kulman vierusruutujen bonus, kun kulma on pelaajalla 
SAFE_CORNER_BONUS = 20

# Määritellään kulmien läheiset ruudut
SAFE_SETS = {
    (0,0): [(0,1),(1,0),(1,1)],
    (0,7): [(0,6),(1,7),(1,6)],
    (7,0): [(6,0),(7,1),(6,1)],
    (7,7): [(6,7),(7,6),(6,6)]
}

def evaluate(board, player):
    opponent = get_opponent(player)

    # 1. Mobility eli pelaajan optiot, tämän myös pitäisi mielestäni riittää  varmistamaan että vastus ei voita peliä
    # sillä että syö kaikki napit keskipelissä
    my_moves = len(valid_moves(board, player))
    opp_moves = len(valid_moves(board, opponent))
    mobility_score = my_moves - opp_moves

    # 2. matriisi
    positional_score = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                positional_score += V[r][c]
            elif board[r][c] == opponent:
                positional_score -= V[r][c]

    # 3. kun kulma on omassa hallussa niin alkuperäinen matriisi ei päde, lisätään arvoon bonus, korvaa stability-heuristiikkaa myös
    # tätä olisi mahdollista laajentaa myös eteenpäin ja muodostaa kulmista alkavia "kolmioita", en tiedä onko nyt tarpeen koska yleensä loppupelitilanne
    # ja lisäksi "kolmas" kolmio on matriisissa jo nyt arvoltaan positiivinen
    for corner, neighs in SAFE_SETS.items():
        cr, cc = corner
        if board[cr][cc] == player:
            for (r, c) in neighs:
                if board[r][c] == player:
                    positional_score += SAFE_CORNER_BONUS
                elif board[r][c] == opponent:
                    positional_score -= SAFE_CORNER_BONUS

    # yhdistetty arvio joka palauttaa siirron pisteet
    return mobility_score + positional_score * heuristic_weight
