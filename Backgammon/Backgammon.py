import random

from enum import Enum
from typing import NamedTuple

class Color(Enum):
	LIGHT = 0
	DARK = 1
	EMPTY = 2

class Piece(NamedTuple):
	type: PieceType
	color: Color


class BoardSquare(NamedTuple):
	color: Color
	num: int

class Direction(Enum):
	LIGHT: 1
	DARK: -1


class Move(NamedTuple): # pass is encoded (-1,-1,false)
	color: Color
	pos: int # 0-23, bar=self.bar_pos
	num: int # roll: 1-6
	hit: bool # hit piece of opposite color

def direction_from_color(color):
	if color == Color.WHITE:
		return 1
	elif color == Color.DARK:
		return -1

class Backgammon:
	def __init__(self):
		self.board = [
		BoardSquare(Color.LIGHT, 2), BoardSquare(Color.EMPTY, 0), BoardSquare(Color.EMPTY, 0), BoardSquare(Color.EMPTY, 0), BoardSquare(Color.EMPTY, 0), BoardSquare(Color.DARK,  5),
		BoardSquare(Color.EMPTY, 0), BoardSquare(Color.DARK,  3), BoardSquare(Color.EMPTY, 0), BoardSquare(Color.EMPTY, 0), BoardSquare(Color.EMPTY, 0), BoardSquare(Color.LIGHT, 5),
		BoardSquare(Color.DARK,  5), BoardSquare(Color.EMPTY, 0), BoardSquare(Color.EMPTY, 0), BoardSquare(Color.EMPTY, 0), BoardSquare(Color.LIGHT, 3), BoardSquare(Color.EMPTY, 0),
		BoardSquare(Color.LIGHT, 5), BoardSquare(Color.EMPTY, 0), BoardSquare(Color.EMPTY, 0), BoardSquare(Color.EMPTY, 0), BoardSquare(Color.EMPTY, 0), BoardSquare(Color.DARK,  2)
		]
		self.bar = {Color.LIGHT: 0, Color.DARK: 0}
		self.bar_pos = 100
		self.cur_player = self.set_start_player()
		self.checkers_per_side = 15
		self.board_size = len(self.board)
		self.beared_pieces = {Color.LIGHT: 0, Color.DARK: 0} # pieces that have moved off the board

	def ind_to_points(self, ind):
		return ind + 1

	def roll_die(self):
		return random.randint(1,6)

	def roll_turn(self):
		roll1, roll2 = self.roll_die(), self.roll_die()
		return max(roll1, roll2), min(roll1, roll2) # put the higher die first for simplicity (need to use higher die if possible)

	def at(self, point):
		return self.board[point]

	def color_at(self, point):
		return self.at(point).color

	def num_at(self, point):
		return self.at(point).num

	def in_board(self, ind):
		return 0 < ind < self.board_size

	def is_empty(self, point):
		return self.color_at(point) == Color.EMPTY

	def is_enemy(self, point, our_color):
		return not is_empty(point) and self.color_at(point) != our_color

	def is_friendly(self, point, our_color):
		return not self.is_enemy(point, our_color)

	def is_legal_spot(self, point, our_color):
		return is_empty(point) or self.color_at(point) == our_color or self.num_at(point) == 1

	def opp_color(self, our_color):
		if our_color is Color.LIGHT:
			return Color.DARK
		elif our_color is Color.DARK:
			return Color.LIGHT
		else:
			assert(False, 'impossible outcome')

	def set_start_player(self):
		light = self.roll_die()
		dark = self.roll_die()
		if light > dark:
			self.cur_player = Color.LIGHT
		elif dark > light:
			self.cur_player = Color.DARK
		else:
			print("Players Rolled Same Numbers, rolling again...")
			self.set_start_player()

	def color_in_bar(self, color):
		assert(color != Color.EMPTY)
		return bar[color] > 0

	def num_in_bar(self, color):
		assert(color != Color.EMPTY)
		return bar[color]


	def bar_start_ind(self, color):
		if color == Color.LIGHT:
			return -1
		elif color is Color.DARK:
			return self.board_size

	# class Move(NamedTuple): # pass is encoded (-1,-1,false)
	#	color: Color
	#	pos: int # 0-23, bar=24
	#	num: int # roll: 1-6
	#	hit: bool # hit piece of opposite color

	def get_pos(self, pos, roll, color): # roll is a single value here
		return pos + direction_from_color(color) * roll

	def get_pos_from_bar(self, roll, color):
		return self.get_pos(self.bar_start_ind(color), roll, color)


	# Update Board to reflect the move, i.e. move out of bar, or bear, or move one spot to another, captures, etc...
	# update self.bar, self.cur_player, self.beared_pieces
	def apply_move(self, move):
		#assert(self.is_legal_spot(self.get_pos(move.pos, move.num, self.cur_player)), self.cur_player)
		start_pos = move.pos
		roll = move.num
		hit = move.hit
		if start_pos == self.bar_pos:
			end_pos = self.get_pos_from_bar(move.num, self.cur_player)
		else:
			end_pos = self.get_pos(move.pos, move.roll, self.cur_player)
		if not self.in_board(end_pos): # bear move
			self.beared_pieces[self.cur_player] += 1
		else:
			# not bear move

		self.cur_player 


	def undo_move(self, move):
		pass

	def moves_non_double(self, color, roll):
		direction = direction_from_color(color) # 1 for light, -1 for dark
		if self.bar[color] > 0:
			# must move both out, don't consider any other pieces
			start_ind = self.bar_start_ind(color)
			if self.is_legal_spot(start_ind + roll[0], color) and self.is_legal_spot(start_ind + roll[1], color)
				return move_to_notation() 


	def moves_double(self, color, roll):


	def get_legal_moves(self, color, roll):
		direction = direction_from_color(color)

		if roll[0] == roll[1]:
			self.moves_double(color, roll)
		else:
			self.moves_non_double(color, roll)

