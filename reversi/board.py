empty_slot = '.'
black_piece = 'X'
white_piece = 'O'
board_size = 8

def new_board():
    """ Luo reversi-pelin aloitusasetelman pelilaudalle. """

    nb = []
    for i in range(board_size):
        row = []
        for i in range(board_size):
            row.append('.')
        nb.append(row)

    nb[3][3] = white_piece
    nb[3][4] = black_piece
    nb[4][3] = black_piece
    nb[4][4] = white_piece
    return nb

def print_board(nb):
    """ Tulostaa pelilaudan. """
    for row in nb:
        print(" ".join(row))

def get_opponent(player):
    """ Hakee vastustajan värin. """
    if player == black_piece:
        return white_piece
    elif player == white_piece:
        return black_piece
    else:
        return None


def valid_moves(board, player):
    """ Käy läpi kaikki sääntöjen mukaiset siirrot joita vuorossa oleva
    pelaaja voi pelata.

    :param board: 8x8 pelilauta listojen listana.
    :param player: Vuorossa oleva pelaaja, joko X tai O
    :return: laillisten siirtojen lista koordinaatteina
    """

    opponent = get_opponent(player)
    #suunnat koordinaattien muutoksina jotta voidaan edetä jokaista linjaa pitkin
    directions = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
    "up_left": (-1, -1),
    "up_right": (-1, 1),
    "down_left": (1, -1),
    "down_right": (1, 1),
}
    moves = []

    for i in range(board_size):
        for j in range(board_size):
            #tyhjä ruutu eli voidaan pelata
            if board[i][j] != empty_slot:
                continue

            #nollataan vastustajan nappulan tarkistus vuoron aluksi    
            for direction, (vertical, horizontal) in directions.items():
                row = i + vertical
                col = j + horizontal
                has_opponent_between = False

                # pelilaudan rajat sekä vastustajan nappula linjalla
                while (0 <= row < board_size and 0 <= col < board_size) and board[row][col] == opponent:
                    row += vertical
                    col += horizontal
                    has_opponent_between = True

                # sama tarkistus myös loppuehdossa
                if has_opponent_between and (0 <= row < board_size and 0 <= col < board_size) and board[row][col] == player:
                    moves.append((i, j))
                    break

    return moves


def play_move(board, move, player):
    """ 
    Toteuttaa pelaajan valitseman siirron. Sijoittaa pelinappulan ja kääntää
    sääntöjen mukaan kääntyvät nappulat kaikilla linjoilla.

    :param board: 8x8 pelilauta listojen listana
    :param move: valitun siirron koordinaatit
    :param player: siirron tekevä pelaaja
    :return: ei palauta arvoa vaan päivittää parametrin board tilanteen
    """
    opponent = get_opponent(player)
    move_row, move_col = move

    directions = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
    "up_left": (-1, -1),
    "up_right": (-1, 1),
    "down_left": (1, -1),
    "down_right": (1, 1),
}
    valid = valid_moves(board, player)
    if move in valid:
        for direction, (vertical, horizontal) in directions.items():
             row = move_row + vertical
             col = move_col + horizontal
             #etsitään kuinka pitkään vastustajan nappulat jatkuvat linjalla
             while (0 <= row < board_size and 0 <= col < board_size) and board[row][col] == opponent:
                    row += vertical
                    col += horizontal


             #kävellään takaisin alkupisteeseen ja käännetään nappulat          
             if (0 <= row < board_size and 0 <= col < board_size) and board[row][col] == player:             
                        
                        
                        
                    r = row - vertical
                    c= col - horizontal
                    while (r, c) != (move_row, move_col):
                        board[r][c] = player
                        r -= vertical
                        c -= horizontal
        board[move_row][move_col] = player

def count_points(board):
    """ Palauttaa kummankin pelaajan pisteet. """

    black_points = sum(row.count(black_piece) for row in board)
    white_points = sum(row.count(white_piece) for row in board)
    return black_points, white_points

def end_game(board):
    """ sisältää tarkistusehdot kaikille eri tavoille joilla peli voi päättyä"""

    black_count = sum(row.count(black_piece) for row in board)
    white_count = sum(row.count(white_piece) for row in board)

    # peli päättyy jos ei tyhjiä ruutuja
    if black_count + white_count == 64:
        return True

    # tai jos toisella ei nappuloita jäljellä, tällöin siirtoja ei enää ole kummallakaan 
    if black_count == 0 or white_count == 0:
        return True
    # jos kummallakaan pelaajalla ei ole laillisia siirtoja
    if not valid_moves(board, black_piece) and not valid_moves(board, white_piece):
        return True


    return False

                