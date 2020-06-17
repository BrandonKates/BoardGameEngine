import random

from enum import Enum
from typing import NamedTuple

class Color(Enum):
	LIGHT = 0
	DARK = 1
	EMPTY = 2

class BoardSquare(NamedTuple):
	color: Color
	num: int

class Direction(Enum):
	LIGHT: 1
	DARK: -1


class Move(NamedTuple): # pass is encoded (None,roll,false)
	color: Color
	pos: int # 0-23, bar=self.bar_pos
	num: int # roll: 1-6
	hit: bool # hit piece of opposite color

def direction_from_color(color):
	if color == Color.LIGHT:
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
		return str(ind + 1)

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
		return 0 <= ind < self.board_size

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
		if pos == self.bar_pos:
			pos = self.bar_start_ind(color)
		return pos + direction_from_color(color) * roll

	def get_pos_from_move(self, move):
		return self.get_pos(move.pos, move.num, move.color)

	# Backgammon Algebraic Notation = BAN
	def move_to_BAN(self, move : Move) -> str:
		initial_pos = 'bar' if move.pos == self.bar_pos else self.ind_to_points(move.pos)

		fp = self.get_pos_from_move(move)
		final_pos = self.ind_to_points(fp) if self.in_board(fp) else 'off'
		#BAN_notation = '%s/%s' % (initial_pos, final_pos)
		#if move.hit:
		#BAN_notation += '*'
		#return BAN_notation
		return initial_pos, final_pos, move.hit

	def moves_to_BAN_no_doubles(self, moves) -> str:
		rolls = []
		for move in moves:
			rolls.append(move.roll)
			if move.pos is None:

	def moves_to_BAN(self, moves) -> str:
		n = len(moves)
		if len(moves) <= 2:
			self.moves_to_BAN_no_doubles(moves)
		else:
			self.moves_to_BAN_doubles(moves)

	def combine_multimoves(self, moves: List) -> List:
		 # given two moves:
		 # either combine them as 6-2:9/3 3/1 -> 6-2:9/1
		 # or if a hit then: 6-2:9/3* 3/1 -> 6-2:9/3*/1
		 # else: 2-2: 9/5 9/5 -> 2-2:9/5(2)

	def move_equality(self, m1, m2):
		return m1.pos == m2.pos and m1.num == m2.num:

	def check_shared(self, m1, m2):
		m1_final = self.get_pos_from_move(m1)
		m2_final = self.get_pos_from_move(m2)
		hit = m1.hit or m2.hit

		if m1_final == m2.pos:
			if m1.hit:
				# new move is m1.pos/m1_final*/m2_final
				(m1.pos, m1_final, m2_final), (False, True, False)
			elif m2.hit:
				(m1.pos, m1_final, m2_final), (False, False, True)
				# m1.pos/m2_final*
			else:
				(m1.pos, m1_final, m2_final), (False, False, False)
				# m1.pos/m2_final
		elif m2_final == m1.pos:
			if m2.hit:
				(m2.pos, m2_final, m1_final), (False, True, False)
				# new move is m2.pos/m2_final*/m1_final
			elif m1.hit:
				(m2.pos, m2_final, m1_final), (False, False, True)
				# new move is m2.pos/m1_final*
			else:
				(m2.pos, m2_final, m1_final), (False, False, False)
				# new move is m2.pos/m1_final

	def combine_two(self, move1, move2):
		max_die = max(move1.num, move2.num)
		min_die = min(move1.num, move2.num)

		if self.get_pos_from_move(move1)
		# check same (last):
		elif self.move_equality(move1, move2):
			s = '%s-%s: %s/%s(2)'
			#return Move(move1.pos, move1.num, move1.hit or move2.hit) # same move


	# Update Board to reflect the move, i.e. move out of bar, or bear, or move one spot to another, captures, etc...
	# update self.bar, self.cur_player, self.beared_pieces
	def apply_move(self, move):
		#assert(self.is_legal_spot(self.get_pos(move.pos, move.num, self.cur_player)), self.cur_player)
		start_pos = move.pos
		roll = move.num
		hit = move.hit
		end_pos = self.get_pos(move.pos, move.num, self.cur_player)
		if not self.in_board(end_pos): # bear move
			self.beared_pieces[self.cur_player] += 1
		else:
			# not bear move
			return
		self.cur_player 


	def undo_move(self, move):
		pass

	def moves_non_double(self, color, roll):
		direction = direction_from_color(color) # 1 for light, -1 for dark
		if self.bar[color] > 0:
			# must move both out, don't consider any other pieces
			start_ind = self.bar_start_ind(color)
			if self.is_legal_spot(start_ind + roll[0], color) and self.is_legal_spot(start_ind + roll[1], color):
				return move_to_notation() 


	def moves_double(self, color, roll):
		pass

	def get_legal_moves(self, color, roll):
		direction = direction_from_color(color)

		if roll[0] == roll[1]:
			self.moves_double(color, roll)
		else:
			self.moves_non_double(color, roll)

