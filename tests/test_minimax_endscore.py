import unittest
import copy

from reversi.board import black_piece, white_piece, empty_slot
from AI.minimax_endscore import minimax_endscore


class TestMinimaxEndscore(unittest.TestCase):

    def test_full_board_black_wins(self):

        # arvo on 64 kun toisella on kaikki nappulat ja siirtoa ei palauteta

        board = [[black_piece for i in range(8)] for i in range(8)]

        val, move = minimax_endscore(board, black_piece)

        self.assertEqual(val, 64)
        self.assertIsNone(move)

    def test_full_board_white_wins(self):

        # sama tapaus kuin edellä mutta toisinpäin
        board = [[white_piece for i in range(8)] for i in range(8)]

        val, move = minimax_endscore(board, black_piece)

        self.assertEqual(val, -64)
        self.assertIsNone(move)

    def test_no_moves_passes_turn(self):

        # musta ympäröi valkoisen, valkoisella ei laillisia siirtoja
        board = [[black_piece for i in range(8)] for i in range(8)]
        board[3][3] = white_piece

        val, move = minimax_endscore(board, white_piece)

        self.assertIsInstance(val, int)

    def test_simple_mid_endgame_position(self):

        # testataan palauttaako ainoan oikean laillisen siirron
        board = [[black_piece for i in range(8)] for i in range(8)]
        board[7][7] = empty_slot   
        board[7][6] = white_piece
        val, move = minimax_endscore(board, black_piece)

        self.assertEqual(move, (7, 7))


    def test_one_empty_but_no_legal_moves(self):

        # Laudalla on yksi tyhjä ruutu, mutta siirto ei ole laillinen valkoiselle

        board = [[black_piece for i in range(8)] for i in range(8)]
        board[0][0] = empty_slot 
        board[0][1] = black_piece 
        board[1][0] = black_piece
        board[1][1] = black_piece

    
        val, move = minimax_endscore(board, white_piece)

        # pitää palauttaa None koska valkoisella ei ole siirtoa
        self.assertIsInstance(val, int)
        self.assertIsNone(move)

    def test_no_moves_branch(self):
        # musta dominoi, valkoinen ei voi pelata mutta peli ei ole loppu
        board = [
            ['X','X','X','X','X','X','X','.'],
            ['X','X','X','X','X','X','X','O'],
            ['X','X','X','X','X','X','X','O'],
            ['X','X','X','X','X','X','X','O'],
            ['X','X','X','X','X','X','X','O'],
            ['X','X','X','X','X','X','X','O'],
            ['X','X','X','X','X','O','.','O'],
            ['X','X','X','X','X','.','.','O'],
        ]

        val, move = minimax_endscore(board, 'O') 

        self.assertIsInstance(val, int)
        self.assertIsNone(move)  

    def test_best_val_branch(self):
        board = [
            ['.','X','X','X','X','X','X','X'],
            ['O','O','O','O','O','O','O','.'],
            ['O','O','O','O','O','O','O','O'],
            ['O','O','O','O','O','O','O','O'],
            ['O','O','O','O','O','O','O','O'],
            ['O','O','O','O','O','O','O','O'],
            ['O','O','O','O','O','O','O','O'],
            ['O','O','O','O','O','.','O','X'],
        ]

        # 7,5 on ratkaistu manuaalisesti parhaaksi arvoksi
        val, move = minimax_endscore(board, 'X')

        self.assertEqual(move, (7,5))

    def test_endscore_finds_correct_value_and_alpha_beta_cuts(self):
        # lauta luotu reversi-stockfish analysaattorilla
        board = [
            ['.', '.', '.', 'X', 'O', '.', '.', 'O'],
            ['.', '.', 'X', 'X', 'X', 'O', 'O', 'O'],
            ['.', 'X', 'O', 'X', 'O', 'X', 'X', 'O'],
            ['X', 'O', 'X', 'O', 'O', 'O', 'X', '.'],
            ['O', 'X', 'O', 'X', 'O', 'X', 'X', 'X'],
            ['O', 'O', 'O', 'O', 'X', 'O', 'X', 'O'],
            ['.', 'X', 'X', 'X', 'O', 'X', 'X', 'O'],
            ['.', 'X', 'X', 'X', 'X', 'X', 'X', 'O'],
        ]

        val, move = minimax_endscore(board, 'X', alpha=-999999, beta=0)

        # siirto, joka häviää vähiten
        self.assertEqual(move, (2,0))

        # val on negatiivinen 
        self.assertLess(val, 0)



