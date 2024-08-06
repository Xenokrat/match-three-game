import unittest

from src.elements import *
from src.game import *


class TestMatchThreeGame(unittest.TestCase):

    def test_piece(self):
        piece = ConcretePiece()
        self.assertEqual(piece._value, PieceEnum.EMPTY)
        piece.set_value(PieceEnum.A)
        self.assertEqual(piece._value, PieceEnum.A)
        piece.set_random_value()
        self.assertIn(piece._value, PieceEnum)
        piece.set_empty_value()
        self.assertEqual(piece._value, PieceEnum.EMPTY)

    def test_score(self):
        score = ConcreteScore()
        score.add_points(10)
        self.assertEqual(score._score.value, 10)
        score.remove_points(5)
        self.assertEqual(score._score.value, 5)
        score.remove_points(10)
        self.assertEqual(score._score.value, 0)

    def test_board(self):
        board = ConcreteBoard(3, 3)
        board.move()
        self.assertEqual(board.get_move_status(), 1)
        board.render()

    def test_bonus(self):
        board = ConcreteBoard(3, 3)
        bonus = ConcreteBonus()
        bonus._board = board
        bonus.apply_bonus()
        self.assertEqual(board.get_move_status(), 1)

    def test_bonus_list(self):
        bonus_list = ConcreteBonusList()
        bonus = ConcreteBonus()
        bonus_list.add_bonus(bonus)
        self.assertTrue(bonus_list.has_bonus(bonus))
        bonus_list.remove_bonus(bonus)
        self.assertFalse(bonus_list.has_bonus(bonus))

    def test_history(self):
        history = ConcreteHistory()
        state = (ConcreteBoard(3, 3), ConcreteScore(), ConcreteBonusList())
        history.add_state(state)
        self.assertEqual(len(history._state_list), 1)
        history.undo()
        self.assertEqual(len(history._state_list), 0)

    def test_command(self):
        command = ConcreteCommand()
        command.execute()

    def test_game(self):
        game = ConcreteGame()
        game.render_game()
        command = ConcreteCommand()
        game.accept_user_command(command)

    def test_match_handler(self):
        board = ConcreteBoard(3, 3)
        score = ConcreteScore()
        match_handler = ConcreteMatchHandler(board, score)
        self.assertTrue(match_handler.has_matches())
        match_handler.process_matches()
        self.assertEqual(match_handler.process_matches_status(), 1)


if __name__ == "__main__":
    unittest.main()
