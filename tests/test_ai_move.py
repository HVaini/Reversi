import unittest
import copy

from AI.ai_move import ai_move
from reversi.board import new_board, valid_moves, black_piece, white_piece, empty_slot, play_move


class TestAIMove(unittest.TestCase):

    def test_ai_move_returns_valid_move(self):

        #AI palauttaa jonkin laillisen siirron alkutilanteessa 
        board = new_board()
        move = ai_move(copy.deepcopy(board), black_piece)
        self.assertIn(move, valid_moves(board, black_piece))

    def test_ai_move_returns_none_if_no_moves(self):
        # testataan että jos valkoisella ei ole laillisia siirtoja (kaikki mustia) niin niitä ei palauteta
        board = [[black_piece for i in range(8)] for i in range(8)]
        move = ai_move(board, white_piece)
        self.assertIsNone(move)

    def test_endgame_mode_does_not_crash(self):

        # minimax_endscore aktivoituu ja palauttaa siirron
        board = [[black_piece for i in range(8)] for i in range(8)]
        board[7][7] = empty_slot
        board[7][6] = white_piece
        move = ai_move(copy.deepcopy(board), black_piece)

        self.assertIsNotNone(move)

    def test_risk_mode_does_not_crash(self):

        # jos valuaatio antaa negatiivisen arvon niin testataan käynnistyykö ja toimiiko longshot-funktio
        board = [[white_piece for i in range(8)] for i in range(8)]
        board[7][7] = empty_slot
        board[7][6] = black_piece
        move = ai_move(copy.deepcopy(board), white_piece)

        self.assertIsNotNone(move)
