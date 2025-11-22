import unittest

from reversi.board import new_board, play_move, black_piece, white_piece, empty_slot
from AI.ai_move import evaluate_normal, evaluate_longshot, evaluate


class TestEvaluate(unittest.TestCase):

    def test_initial_position_is_symmetric(self):
        # arvojen pitäisi olla samat molemmilla pelaajilla koska tilanne on symmetrinen
        board = new_board()

        val_black = evaluate_normal(board, black_piece)
        val_white = evaluate_normal(board, white_piece)

        self.assertEqual(val_black, 0)
        self.assertEqual(val_white, 0)

    def test_evaluate_changes_after_move(self):

        # arvojen pitäisi muuttua
        board = new_board()
        play_move(board, (2, 3), black_piece)

        val_black = evaluate_normal(board, black_piece)
        val_white = evaluate_normal(board, white_piece)

        # arvojen pitää olla kokonaislukuja
        self.assertIsInstance(val_black, int)
        self.assertIsInstance(val_white, int)

        # tilanteen pitäisi muuttua
        self.assertFalse(val_black == 0 and val_white == 0)

    def test_longshot_weight_affects_evaluation(self):

        #Testaa että longshot (weight=1) ja normal (weight=5)
        #antavat eri arvoja ainakin jossain tilanteessa.

        board = new_board()
        play_move(board, (2, 3), black_piece)

        normal_val = evaluate_normal(board, black_piece)
        longshot_val = evaluate_longshot(board, black_piece)

        # arvojen pitäisi olla usein erilaisia weightin takia
        self.assertNotEqual(normal_val, longshot_val)


    def test_evaluate_simple_asymmetry(self):

        # arvojen ei pitäisi olla samat
        board = new_board()
        play_move(board, (2, 3), black_piece)

        val_black = evaluate_normal(board, black_piece)
        val_white = evaluate_normal(board, white_piece)


        self.assertTrue(val_black != val_white)

    def test_corner_owned_but_adjacent_empty(self):

        #testaa toimiiko heuristiikan kulmanvierus-bonus
        board = [[white_piece for i in range(8)] for i in range(8)]
        board[0][0] = black_piece      
        board[0][1] = empty_slot       
        board[1][1] = white_piece      

        val = evaluate(board, black_piece, weight=5)

        
        self.assertIsInstance(val, int)

