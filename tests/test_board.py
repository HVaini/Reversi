import unittest

from reversi.board import (
    new_board,
    valid_moves,
    play_move,
    black_piece,
    white_piece,
    empty_slot,
    count_points,
    end_game,
)


class TestBoard(unittest.TestCase):

    def test_new_board_initial_setup(self):
        # asetaanko lauta oikein
        board = new_board()
        b, w = count_points(board)

        self.assertEqual(b, 2)
        self.assertEqual(w, 2)

        self.assertEqual(board[3][3], white_piece)
        self.assertEqual(board[3][4], black_piece)
        self.assertEqual(board[4][3], black_piece)
        self.assertEqual(board[4][4], white_piece)

    def test_valid_moves_initial_black(self):

        # ovatko validit siirrot oikein alussa
        board = new_board()
        moves = set(valid_moves(board, black_piece))

        expected = {(2, 3), (3, 2), (4, 5), (5, 4)}
        self.assertEqual(moves, expected)

    def test_play_move_flips_correct_pieces(self):

        # kääntyvätkö oikeat nappulat
        board = new_board()
        play_move(board, (2, 3), black_piece)

        
        self.assertEqual(board[2][3], black_piece)
        self.assertEqual(board[3][3], black_piece)

        # Tarkista pisteet
        b, w = count_points(board)
        self.assertEqual(b, 4) 
        self.assertEqual(w, 1)

    def test_end_game_on_full_board(self):
        
        # end game testi täydelle laudalle
        board = [[black_piece for i in range(8)] for i in range(8)]
        self.assertTrue(end_game(board))

    def test_end_game_initial_is_false(self):
        
        # end game ei toteudu alussa
        board = new_board()
        self.assertFalse(end_game(board))
    
    def test_end_game_no_moves_for_both_players(self):

        # testataan että peli päättyy vaikka laudalla on tilaa mutta kummallakaan ei ole laillista siirtoa
        board = [[black_piece for _ in range(8)] for _ in range(8)]
        board[2][3] = white_piece
        board[3][6] = white_piece

        # nyt kumpikaan ei voi siirtää, mutta lauta ei ole täynnä
        board[0][0] = empty_slot

        self.assertTrue(end_game(board))

