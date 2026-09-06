import contextlib
import io
import random
import unittest
from unittest.mock import patch

import bingo


class BingoTests(unittest.TestCase):
    def setUp(self):
        state = random.getstate()
        self.addCleanup(random.setstate, state)
        random.seed(17)

    def card(self):
        return [[str(row * 5 + column) for column in range(5)] for row in range(5)]

    def test_cards_have_25_unique_items_even_if_source_has_duplicates(self):
        items = [str(index) for index in range(30)] * 2
        with patch('builtins.input', side_effect=['2', 'Sam', 'Alex']):
            players = bingo.initialtePlayers(items)
        for card in players.values():
            self.assertEqual([len(row) for row in card], [5] * 5)
            flattened = [item for row in card for item in row]
            self.assertEqual(len(set(flattened)), 25)
            self.assertTrue(set(flattened) <= set(items))
        self.assertEqual(len(items), 60)

    def test_insufficient_unique_items_fail_before_prompting(self):
        with patch('builtins.input') as prompt:
            with self.assertRaisesRegex(ValueError, '25 distinct'):
                bingo.initialtePlayers(['one'] * 30)
            prompt.assert_not_called()

    def test_every_complete_row_column_and_diagonal_wins(self):
        lines = [[(row, column) for column in range(5)] for row in range(5)]
        lines += [[(row, column) for row in range(5)] for column in range(5)]
        lines += [[(i, i) for i in range(5)], [(i, 4 - i) for i in range(5)]]
        for line in lines:
            with self.subTest(line=line):
                card = self.card()
                for row, column in line:
                    card[row][column] = 'FOUND'
                self.assertTrue(bingo.isSingleLineWinner({'Sam': card}, 'Sam'))
                row, column = line[2]
                card[row][column] = 'missing'
                self.assertFalse(bingo.isSingleLineWinner({'Sam': card}, 'Sam'))

    def test_four_corners_requires_only_the_corners(self):
        card = self.card()
        corners = ((0, 0), (0, 4), (4, 0), (4, 4))
        for row, column in corners:
            card[row][column] = 'FOUND'
        self.assertTrue(bingo.isFourCornersWinner({'Sam': card}, 'Sam'))
        for row, column in corners:
            card[row][column] = 'missing'
            self.assertFalse(bingo.isFourCornersWinner({'Sam': card}, 'Sam'))
            card[row][column] = 'FOUND'

    def test_caller_draws_each_distinct_item_once_then_reports_exhaustion(self):
        calls = []
        for _ in range(3):
            self.assertIs(bingo.getNewItemForCaller(['a', 'b', 'c', 'a'], calls), calls)
        self.assertEqual(set(calls), {'a', 'b', 'c'})
        self.assertEqual(len(calls), 3)
        with self.assertRaisesRegex(ValueError, 'already been called'):
            bingo.getNewItemForCaller(['a', 'b', 'c'], calls)
        self.assertEqual(len(calls), 3)

    def test_full_card_mode_completes_offline_in_25_draws(self):
        transcript = io.StringIO()
        inputs = ['1', 'Sam', '1'] + ['p'] * 25
        with patch('builtins.input', side_effect=inputs), contextlib.redirect_stdout(transcript):
            bingo.Game([str(i) for i in range(25)])
        self.assertIn('Game End', transcript.getvalue())
        self.assertIn('Winners are\nSam', transcript.getvalue())

    def test_invalid_mode_is_false(self):
        self.assertIs(bingo.checkWinner(99, {'Sam': self.card()}, 'Sam'), False)


if __name__ == '__main__':
    unittest.main()
