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

	def toString(self):
		piece = ' '
		if self.color == Color.LIGHT:
			piece = 'o'
		elif self.color == Color.DARK:
			piece = 'x'
		return piece * self.num

	def toUnicode(self):
		piece = ' '
		if self.color == Color.LIGHT:
			piece = '○'
		elif self.color == Color.DARK:
			piece = '●'
		return piece * self.num

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
		self.die_unicode = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']

	def __str__(self):
		s = ''
		offset = self.board_size // 2
		for i in range(offset):
			s += self.board[i].toUnicode() + '\t' + self.board[self.board_size-i-1].toUnicode() + '\n'
		return s


	def ind_as_string(self, ind):
		if self.in_board(ind):
			return str(ind + 1)
		if ind == self.bar_pos:
			return 'bar'
		else:
			return 'off'

	def roll_die(self):
		return random.randint(1,6)

	def roll_turn(self):
		roll1, roll2 = self.roll_die(), self.roll_die()
		return max(roll1, roll2), min(roll1, roll2) # put the higher die first for simplicity (need to use higher die if possible)

	def roll_to_die_unicode(self, roll):
		return self.die_unicode[roll-1]

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
			assert False, 'impossible outcome'

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


	def get_pos(self, pos, roll, color): # roll is a single value here
		if pos == self.bar_pos:
			pos = self.bar_start_ind(color)
		return pos + direction_from_color(color) * roll

	def get_pos_from_move(self, move):
		return self.get_pos(move.pos, move.num, move.color)


	def moves_to_dicts(self, moves) -> list:
		rolls = [m.num for m in moves][:2] # only want the first two in the case we have doubles (more than 2 rolls, otherwise we always have <=2 moves)
		dicts = []
		for move in moves:
			if move.pos:
				dicts.append( {'pos' : [move.pos, self.get_pos_from_move(move)], \
						   	   'hit' : [False, move.hit]})
		return dicts

	def dict_to_BAN(self, d):
		s = ''
		for pos, hit in zip(d['pos'], d['hit']):
			s += self.ind_as_string(pos)
			if hit:
				s += "*"
			s += '/'
		return s[:-1] # remove final slash
		

	# Backgammon Algebraic Notation = BAN
	def dicts_to_BAN_no_doubles(self, dicts) -> str:
		rolls = ''
		shared = self.check_shared(dicts[0], dicts[1])
		if shared:
			rolls += self.dict_to_BAN(shared)
		else:
			rolls += self.dict_to_BAN(dicts[0]) + ' ' + self.dict_to_BAN(dicts[1])
		return rolls

	def dicts_to_BAN_doubles(self, dicts) -> str:
		i = 0
		j = 1
		while 1 < len(dicts) and i < len(dicts):
			while len(dicts) > 1 and j < len(dicts):
				combine = self.check_shared(dicts[i], dicts[j]) # i<j
				if combine:
					dicts = [combine] + dicts[0:i] + dicts[i+1:j] + dicts[j+1:]
					i = 0
					j = 1
				else:
					j+=1
			i+=1
			j=i+1

		for i in range(len(dicts)):
			dicts[i]['eq'] = 1

		i = 0
		j = 1
		while 1 < len(dicts) and i < len(dicts):
			while len(dicts) > 1 and j < len(dicts):
				combine = self.check_equality(dicts[i], dicts[j]) # i<j
				if combine:
					dicts = [combine] + dicts[0:i] + dicts[i+1:j] + dicts[j+1:]
					i = 0
					j = 1
				else:
					j+=1
			i+=1
			j=i+1

		rolls = ''
		for d in dicts:
			rolls += self.dict_to_BAN(d)
			if d['eq'] > 1:
				rolls += '(%s)' % d['eq']
			rolls += ' '
		return rolls.strip()



	def moves_to_BAN(self, moves) -> str:
		rolls = '%s-%s: ' % (moves[0].num, moves[1].num)
		dicts = self.moves_to_dicts(moves)
		if len(dicts) == 0:
			return rolls + '(no play)'
		if len(dicts) == 1:
			return rolls + self.dict_to_BAN(dicts[0])
		if len(moves) <= 2:
			return rolls + self.dicts_to_BAN_no_doubles(dicts)
		else:
			return rolls + self.dicts_to_BAN_doubles(dicts)

	def check_shared(self, t1, t2):
		def check_shared_helper(t, bef, bef_hit):
			pos = bef
			hit = bef_hit
			for i in range(1, len(t['pos'])):
				if t['hit'][i]:
					pos.append(t['pos'][i])
					hit.append(True)
			return pos, hit
		def helper(t1, t2):
			hit = [False]
			pos, hit = check_shared_helper(t1, [t1['pos'][0]], [False])
			pos, hit = check_shared_helper(t2, pos, hit)
			if not t2['hit'][-1]:
				pos.append(t2['pos'][-1])
				hit.append(t2['hit'][-1])
			return {'pos' : pos, 'hit' : hit}
		# t1_final == t2_start
		if t1['pos'][-1] == t2['pos'][0]:
			return helper(t1, t2)
		# t2_start == t1_final
		elif t2['pos'][-1] == t1['pos'][0]:
			return helper(t2, t1)
		return False

	def check_equality(self, t1, t2):
		if len(t1['pos']) != len(t2['pos']):
			return False
		for t1_pos, t1_hit, t2_pos, t2_hit in zip(t1['pos'], t1['hit'], t2['pos'], t2['hit']):
			if t1_pos != t2_pos or t1_hit != t2_hit:
				return False
		t1['eq'] += t2['eq']
		return t1


	def update_board_pos(self, pos, color, amnt):
		assert amnt >= 0
		if amnt == 0:
			color = Color.EMPTY
		self.board[pos] = BoardSquare(color, amnt)

	# Update Board to reflect the move, i.e. move out of bar, or bear, or move one spot to another, captures, etc...
	# update self.bar, self.cur_player, self.beared_pieces
	def apply_move(self, move) -> None:
		start_pos = move.pos
		end_pos = self.get_pos_from_move(move)
		cur_player = move.color
		opp_player = self.opp_color(cur_player)
		if start_pos == self.bar_pos:
			self.bar[cur_player] -= 1
		else:
			self.update_board_pos(start_pos, cur_player, self.board[start_pos].num - 1)
		if not self.in_board(end_pos): # bear move
			self.beared_pieces[cur_player] += 1
		elif move.hit:
			# not bear move
			self.update_board_pos(end_pos, cur_player, 1) # update the end position to have 1 piece of this type
			self.bar[opp_player] += 1
		else:
			self.update_board_pos(end_pos, cur_player, self.board[end_pos].num + 1)
		
		
	def undo_move(self, move):
		start_pos = move.pos
		end_pos = self.get_pos_from_move(move)
		cur_player = move.color
		opp_player = self.opp_color(cur_player)
		if start_pos == self.bar_pos:
			self.bar[cur_player] += 1
		else:
			self.update_board_pos(start_pos, cur_player, self.board[start_pos].num + 1)
		if not self.in_board(end_pos):
			self.beared_pieces[cur_player] -= 1
		elif move.hit:
			# not bear move
			self.update_board_pos(end_pos, opp_player, 1)
			self.bar[opp_player] -= 1
		else:
			self.update_board_pos(end_pos, cur_player, self.board[end_pos].num - 1)



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



''' 
	Legal Singular Moves:
		move to an open point (open: not more than one opposing checkers on spot)
	Modifiers:
		if piece of color on bar:
			must move piece off first, check if more pieces on bar
		elif able to bear:
			bear moves are legal
		else:
			normal generation of moves

	Recursive Procedure:
		Start at furthest man from home
		Scan towards home, stopping at squares with pieces of that color
		First determine which state the board is in (what kinds of moves are legal)
		apply the current die face to the piece 
			if legal_moves:
				update the board
				call recursively for the remaining die faces, start the next scan at the furthest point from home
			else:
				continue to the next spot with a piece of correct color and try again




'''
