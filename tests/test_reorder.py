import unittest

from AI.reorder import reorder_moves


class TestReorder(unittest.TestCase):

    def test_reorder_prioritizes_corners(self):

        # asetetaanko kulmat oikein ensimmäiseksi listalla
        board = [["." for _ in range(8)] for _ in range(8)]
        player = "X"

        moves = [
            (1, 1),  # worst
            (0, 1),  # bad
            (3, 3),  # neutral
            (0, 0),  # corner
        ]

        ordered = reorder_moves(board, player, moves)

        self.assertEqual(ordered[0], (0, 0))

        self.assertIn((3, 3), ordered[1:3])
        self.assertIn((0, 1), ordered)
        self.assertIn((1, 1), ordered)

    def test_reorder_preserves_all_moves(self):

        # kaikki siirrot säilyvät
        board = [["." for i in range(8)] for i in range(8)]
        player = "X"
        moves = [(0,0), (1,1), (3,3), (0,1), (5,5)]

        ordered = reorder_moves(board, player, moves)

        self.assertEqual(set(ordered), set(moves))
        self.assertEqual(len(ordered), len(moves))

    def test_reorder_two_corners_first(self):

        # testaa että kulmat lisätään lukujärjestyksessä listan alkuun, viimeeksi luettu ensin
        board = [["." for i in range(8)] for i in range(8)]
        player = "X"
        moves = [(7,7), (0,0), (4,4)]

        ordered = reorder_moves(board, player, moves)

        self.assertEqual(ordered[0], (0,0))
        self.assertEqual(ordered[1], (7,7))

    def test_reorder_empty_list(self):

        # jos ei siirtoja niin lista on tyhjä
        board = [["." for i in range(8)] for i in range(8)]
        player = "X"
        moves = []

        ordered = reorder_moves(board, player, moves)

        self.assertEqual(ordered, [])
