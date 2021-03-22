from Othello import Color, Square, Othello, Board

import pytest

class TestOthello:
	def setup_othello(self):
		othello = Othello()
		return othello, othello.board

	def test_board_setup_correct(self):
		_, board = self.setup_othello()


class TestBoard:
	def setup_board(self):
		board = Board()
		moves = Board.get_move_directions()
		return board, moves

	def test_is_spot_in_board(self):
		board, _ = self.setup_board()
		assert board.is_spot_in_board(0, 0)
		assert board.is_spot_in_board(0, 7)
		assert board.is_spot_in_board(7, 0)
		assert board.is_spot_in_board(7, 7)
		assert not board.is_spot_in_board(0, 8)
		assert not board.is_spot_in_board(8, 8)
		assert not board.is_spot_in_board(-1, 2)

	def test_move(self):
		board, moves = self.setup_board()


	def test_board_setup(self):
		board, _ = self.setup_board()
		assert board.get_square(3, 4) == Color.BLACK
		assert board.get_square(3, 3) == Color.WHITE
		assert board.get_square(4, 4) == Color.WHITE
		assert board.get_square(4, 3) == Color.BLACK
