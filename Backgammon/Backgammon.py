import random
from copy import deepcopy
from enum import Enum
from typing import NamedTuple


class Player(Enum):
	LIGHT = 0
	DARK = 1
	EMPTY = 2

	def to_unicode(self):
		if self == Player.LIGHT:
			return '○'
		if self == Player.DARK:
			return '●'
		return ' '

	def __str__(self):
		if self == Player.LIGHT:
			return 'o'
		if self == Player.DARK:
			return 'x'
		return ' '

	def direction(self):
		if self == Player.LIGHT:
			return 1
		if self == Player.DARK:
			return -1

	def opponent(self):
		if self == Player.LIGHT:
			return Player.DARK
		if self == Player.DARK:
			return Player.LIGHT
		assert False, 'impossible outcome'


class BoardSquare(NamedTuple):
	player: Player
	num: int

	def to_string(self):
		return str(self.player) * self.num

	def to_unicode(self):
		return str(self.player.to_unicode()) * self.num


class Move(NamedTuple):  # pass is encoded (None,roll,false)
	player: Player
	pos: int  # 0-23, bar=self.bar_pos
	num: int  # roll: 1-6
	hit: bool  # hit piece of opposite player

class Turn(NamedTuple):
	player: Player
	prev_player: Player
	dice: tuple
	action: int
	double_turn: bool
	first_move_hit: bool
	second_move_hit: bool

class State:
	def __init__(self, board, bar, beared, turn_num, turn_history, double_turn, dice, cur_player):
		self.board = deepcopy(board)
		self.bar = bar.copy()
		self.beared = beared.copy()
		self.turn_num = turn_num
		self.turn_history = turn_history.copy()
		self.double_turn = double_turn
		self.dice = dice
		self.cur_player = cur_player


class Backgammon:
	def __init__(self, verbose=True, max_turns = 500, deterministic = None):
		self.verbose = verbose
		'''self.board = [
			BoardSquare(Player.LIGHT, 2), BoardSquare(Player.EMPTY, 0), BoardSquare(Player.EMPTY, 0), BoardSquare(
				Player.EMPTY, 0), BoardSquare(Player.EMPTY, 0), BoardSquare(Player.DARK,  5),
			BoardSquare(Player.EMPTY, 0), BoardSquare(Player.DARK,  3), BoardSquare(Player.EMPTY, 0), BoardSquare(
				Player.EMPTY, 0), BoardSquare(Player.EMPTY, 0), BoardSquare(Player.LIGHT, 5),
			BoardSquare(Player.DARK,  5), BoardSquare(Player.EMPTY, 0), BoardSquare(Player.EMPTY, 0), BoardSquare(
				Player.EMPTY, 0), BoardSquare(Player.LIGHT, 3), BoardSquare(Player.EMPTY, 0),
			BoardSquare(Player.LIGHT, 5), BoardSquare(Player.EMPTY, 0), BoardSquare(Player.EMPTY, 0), BoardSquare(
				Player.EMPTY, 0), BoardSquare(Player.EMPTY, 0), BoardSquare(Player.DARK,  2)
		]'''
		self.board = [ 
		[2,0,0,0,0,0,
		 0,0,0,0,0,5,
		 0,0,0,0,3,0,
		 5,0,0,0,0,0],
		[0,0,0,0,0,5,
		 0,3,0,0,0,0,
		 5,0,0,0,0,0,
		 0,0,0,0,0,2]]
		self.bar = [0, 0]
		self.beared = [0,0]
		self.turn_num = 1
		self.turn_history = []
		self.double_turn = False
		# self.dice
		# self.cur_player

		self.bar_pos = 100
		self.pass_pos = 1001
		self.off_pos = -100
		self.checkers_per_side = 15
		self.board_size = len(self.board[0])
		# pieces that have moved off the board

		self.direction = [1,-1]
		self.opponent = [1,0]
		self.die_unicode = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']
		self.dark_home = [5, 4, 3, 2, 1, 0]
		self.light_home = [18, 19, 20, 21, 22, 23]
		self.moves = []
		self.moves_list = []
		
		self.max_turns = max_turns
		self.ddice = None
		if deterministic:
			player, self.ddice = deterministic
			self.dice = self.ddice[0]
			self.cur_player = self.prev_player = player
		else:
			self.init_game()

	def save_state(self):
		return State(self.board, self.bar, self.beared, self.turn_num, self.turn_history, self.double_turn, self.dice, self.cur_player)

	def restore_state(self, state):
		self.board = deepcopy(state.board)
		self.bar = state.bar.copy()
		self.beared = state.beared.copy()
		self.turn_num = state.turn_num
		self.turn_history = state.turn_history.copy()
		self.double_turn = state.double_turn
		self.dice = state.dice
		self.cur_player = state.cur_player

	def init_game(self):
		self.set_start_player()
		self.roll_dice()

	def __str__(self):
		s = "Turn %s\n" % str(self.turn_num)
		bar_light = str(self.bar[0])
		bar_dark = str(self.bar[1])
		beared_light = str(self.beared[0])
		beared_dark = str(self.beared[1])

		change = False
		if len(bar_light) < len(beared_light):
			bar_light = " " + bar_light
			s += " "
		elif len(beared_light) < len(bar_light):
			beared_light = " " + beared_light
			s += " "

		if len(bar_dark) < len(beared_dark):
			bar_dark = " " + bar_dark
		elif len(beared_dark) < len(bar_dark):
			beared_dark = " " + beared_dark
		s +=  "         LIGHT│DARK\n"
		s += "Bar:       %s  │  %s\n" % (bar_light, bar_dark)
		s += "Beared:    %s  │  %s\n\n" % (beared_light, beared_dark)
		s += self.to_unicode()
		s += 'Rolled: %s\n ' % str(self.dice_to_unicode(self.dice))
		return s

	#def board_repr(self):
	#	s = ''
	#	offset = self.board_size // 2
	#	for i in range(offset):
	#		s += self.board[i].to_unicode() + '\t' + \
	#			self.board[self.board_size-i-1].to_unicode() + '\n'
	#	return self.to_unicode()

	def to_unicode(self):
		s =  '│13 14 15 16 17 18 19 20 21 22 23 24│\n'
		s += '│┯  ┯  ┯  ┯  ┯  ┯   ┯  ┯  ┯  ┯  ┯  ┯│\n'
		mat = self.board_as_matrix()
		for i in range(len(mat)):
			if i == 5:
				s += '│' + '═' * 17 + '╬' + '═' * 17 + '│' + '\n'  # ‾
			for j in range(len(mat[0])):
				if j == 0:
					s += '│'
				player = mat[i][j]
				s += player.to_unicode()
				if j != len(mat[0]) - 1 and j != 5:
					s += "  "
				if j == 5:
					s += ' ║ '
				if j == 11:
					s += '│'
			s += '\n'
		s += '│┷  ┷  ┷  ┷  ┷  ┷   ┷  ┷  ┷  ┷  ┷  ┷│\n'
		s += '│12 11 10 9  8  7   6  5  4  3  2  1│\n'
		return s

	def board_as_matrix(self):
		matrix = [[Player.EMPTY] * 12 for i in range(10)]

		for i in range(0, 12):
			player = self.player_at(i)
			if player != Player.EMPTY:
				for k in range(min(self.at(player.value, i), 5)):
					matrix[9-k][11-i] = player

		for i in range(12, self.board_size):
			player = self.player_at(i)
			if player != Player.EMPTY:
				for k in range(min(self.at(player.value, i), 5)):
					matrix[k][i-12] = player
		return matrix

	def board_as_unicode_matrix(self):
		matrix = self.board_as_matrix()
		for i in range(len(matrix)):
			for j in range(len(matrix[0])):
				matrix[i][j] = matrix[i][j].to_unicode()
		return matrix

	def ind_as_string(self, ind):
		if self.in_board(ind):
			return str(ind + 1)
		if ind == self.bar_pos:
			return 'bar'
		if ind == self.pass_pos:
			return 'pass'
		return 'off'

	def roll_die(self):
		return random.randint(1, 6)

	def roll_dice(self):
		roll1, roll2 = self.roll_die(), self.roll_die()
		# put the higher die first for simplicity (need to use higher die if possible)
		self.dice = max(roll1, roll2), min(roll1, roll2)

	def dice_to_unicode(self, dice):
		return self.die_unicode[dice[0]-1] + " " + self.die_unicode[dice[1]-1]


	def at(self, player, point):
		#assert not (self.board[0][point] > 0 and self.board[1][point] > 0) 
		return self.board[player][point]

	def player_at(self, point) -> Player:
		if self.board[0][point] > 0:
			return Player.LIGHT
		elif self.board[1][point] > 0:
			return Player.DARK
		return Player.EMPTY

	def in_board(self, ind):
		return 0 <= ind < self.board_size

	def is_empty(self, point):
		return self.at(0, point) == 0 and self.at(1, point) == 0

	def is_enemy(self, point, player):
		return self.at(self.opponent[player], point) > 0

	def is_hit(self, point, player):
		return self.in_board(point) and self.at(self.opponent[player], point) == 1
	
	def is_legal_spot(self, point, player):
		return point == self.bar_pos or self.at(self.opponent[player], point) <= 1

	def is_score_spot(self, point, player):
		# for white this is > 23, for black this is < 0
		if point == self.bar_pos:
			return False
		if player == 0:
			return point > 23
		if player == 1:
			return point < 0
		return False

	def set_start_player(self):
		light = self.roll_die()
		dark = self.roll_die()
		if self.verbose:
			print("Player 1 (white) rolled: %s" % str(light))
			print("Player 2 (black) rolled: %s" % str(dark))
		if light > dark:
			self.cur_player = self.prev_player = 0
			if self.verbose:
				print("Player 1 (white) goes first.")
		elif dark > light:
			self.cur_player = self.prev_player = 1
			if self.verbose:
				print("Player 2 (black) goes first.")
		else:
			if self.verbose:
				print("Players rolled same numbers, rolling again...")
			self.set_start_player()

	def num_in_bar(self, player):
		return self.bar[player]

	def player_home(self, player):
		return [self.light_home, self.dark_home][player]

	def bar_start_ind(self, player):
		return [-1, self.board_size][player]

	def get_turn_num(self):
		return self.turn_num

	def get_pos(self, pos, roll, player):  # roll is a single value here
		if pos == self.bar_pos or pos == 'bar':
			pos = self.bar_start_ind(player)
		return pos + self.direction[player] * roll

	def get_next_pos(self, pos, player):
		return self.get_pos(pos, 1, player)

	def get_pos_from_bar(self, roll, player):
		return self.get_pos(self.bar_pos, roll, player)

	def get_pos_from_move(self, move):
		return self.get_pos(move.pos, move.num, move.player)

	def get_start_pos(self, player):
		return [0, self.board_size - 1][player]

	def input_to_move(self, positions, player) -> list:
		if positions == 'pass':
			moves = [Move(player, self.pass_pos, -1, False), Move(player, self.pass_pos, -1, False)]
			return self.encode_checker_move(moves)
		moves = []
		for start_pos, roll in positions:
			if start_pos == 'bar':
				start_pos = self.bar_pos
			else:
				start_pos = int(start_pos) - 1
			roll = int(roll)
			moves.append(Move(player, start_pos, roll, False))
		return self.encode_checker_move(moves)

	def moves_to_dicts(self, moves) -> list:
		# only want the first two in the case we have doubles (more than 2 rolls, otherwise we always have <=2 moves)
		rolls = [m.num for m in moves][:2]
		dicts = []
		for move in moves:
			if move.pos is not None:
				end_pos = self.get_pos_from_move(move)
				if not self.in_board(end_pos) and end_pos != self.bar_pos and end_pos != self.pass_pos:
					end_pos = self.off_pos
				dicts.append({'pos': [move.pos, end_pos],
							  'hit': [False, move.hit]})
		return dicts

	def dict_to_BAN(self, d):
		s = ''
		for pos, hit in zip(d['pos'], d['hit']):
			s += self.ind_as_string(pos)
			if hit:
				s += "*"
			s += '/'
		return s[:-1]  # remove final slash

	# Backgammon Algebraic Notation = BAN

	def dicts_to_BAN_no_doubles(self, dicts) -> str:
		rolls = ''
		shared = self.check_shared(dicts[0], dicts[1])
		if self.check_equality(dicts[0], dicts[1]):
			rolls += self.dict_to_BAN(dicts[0]) + "(2)"
		elif shared:
			rolls += self.dict_to_BAN(shared)
		else:
			rolls += self.dict_to_BAN(dicts[0]) + \
				' ' + self.dict_to_BAN(dicts[1])
		return rolls

	def dicts_to_BAN_doubles(self, dicts) -> str:
		i = 0
		j = 1
		while 1 < len(dicts) and i < len(dicts):
			while len(dicts) > 1 and j < len(dicts):
				combine = self.check_shared(dicts[i], dicts[j])  # i<j
				if combine:
					dicts = [combine] + dicts[0:i] + dicts[i+1:j] + dicts[j+1:]
					i = 0
					j = 1
				else:
					j += 1
			i += 1
			j = i+1

		for i in range(len(dicts)):
			dicts[i]['eq'] = 1

		i = 0
		j = 1
		while 1 < len(dicts) and i < len(dicts):
			while len(dicts) > 1 and j < len(dicts):
				if self.check_equality(dicts[i], dicts[j]):  # i<j:
					dicts[i]['eq'] += dicts[j]['eq']
					dicts = dicts[0:j] + dicts[j+1:]
					i = 0
					j = 1
				else:
					j += 1
			i += 1
			j = i+1

		rolls = ''
		for d in dicts:
			rolls += self.dict_to_BAN(d)
			if d['eq'] > 1:
				rolls += '(%s)' % d['eq']
			rolls += ' '
		return rolls.strip()

	def are_pass_moves(self, dicts) -> bool:
		for d in dicts:
			s = ''
			if d['pos'][0] != self.pass_pos:
				return False
		return True

	def moves_to_BAN(self, moves, dice) -> str:
		rolls = '%s-%s: ' % (dice[0], dice[1])  # (moves[0].num, moves[1].num)
		dicts = self.moves_to_dicts(moves)
		if self.are_pass_moves(dicts) or len(dicts) == 0:
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
			return {'pos': pos, 'hit': hit}
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
		return True

	def update_board_pos(self, pos, player, amnt):
		assert(amnt >= 0)
		self.board[player][pos] = amnt

	# Update Board to reflect the move, i.e. move out of bar, or bear, or move one spot to another, captures, etc...
	# update self.bar, self.cur_player, self.beared

	def apply_move(self, move) -> None:
		start_pos = move.pos
		end_pos = self.get_pos_from_move(move)
		cur_player = move.player
		opp_player = self.opponent[cur_player]
		if start_pos == self.pass_pos:
			return
		if start_pos == self.bar_pos:
			assert self.bar[cur_player] >= 1
			self.bar[cur_player] -= 1
		else:
			assert self.at(cur_player, start_pos) >= 1
			self.update_board_pos(start_pos, cur_player, self.at(cur_player, start_pos) - 1)
		if not self.in_board(end_pos):  # bear move
			assert end_pos != self.bar_pos
			self.beared[cur_player] += 1
		elif move.hit:
			# not bear move
			# update the end position to have 1 piece of this type
			assert self.at(opp_player, end_pos) == 1
			self.update_board_pos(end_pos, cur_player, 1)
			self.update_board_pos(end_pos, opp_player, 0)
			self.bar[opp_player] += 1
		else:
			assert self.at(opp_player, end_pos) == 0
			assert self.at(cur_player, end_pos) >= 0
			self.update_board_pos(end_pos, cur_player, self.at(cur_player, end_pos) + 1)
			assert self.at(cur_player, end_pos) >= 1

	def undo_move(self, move):
		start_pos = move.pos
		end_pos = self.get_pos_from_move(move)
		cur_player = move.player
		opp_player = self.opponent[cur_player]
		if start_pos == self.pass_pos:
			return
		elif start_pos == self.bar_pos:
			self.bar[cur_player] += 1
		else:
			assert self.at(cur_player, start_pos) >= 0
			self.update_board_pos(start_pos, cur_player, self.at(cur_player, start_pos) + 1)
		if not self.in_board(end_pos):
			assert self.beared[cur_player] >= 1
			self.beared[cur_player] -= 1
		elif move.hit:
			# not bear move
			assert self.at(cur_player, end_pos) == 1
			assert self.bar[opp_player] >= 1
			self.update_board_pos(end_pos, opp_player, 1)
			self.update_board_pos(end_pos, cur_player, 0)
			self.bar[opp_player] -= 1
		else:
			assert self.at(cur_player, end_pos) >= 1
			self.update_board_pos(end_pos, cur_player, self.at(cur_player, end_pos) - 1)
			assert self.at(cur_player, end_pos) >= 0 

	def check_move_hit(self, move):
		hit = False
		end_pos = self.get_pos_from_move(move)
		if self.is_hit(end_pos, move.player):
			move = Move(move.player, move.pos, move.num, True)
			hit = True
		return move, hit

	def apply_action(self, action) -> None:
		moves = self.decode_checker_move(action)
		fmh = False
		smh = False
		assert len(moves) == 2
		move, fmh = self.check_move_hit(moves[0])
		self.apply_move(move)
		move, smh = self.check_move_hit(moves[1])
		self.apply_move(move)

		self.turn_history.append(Turn(self.cur_player, self.prev_player, self.dice, action, self.double_turn, fmh, smh))

	def undo_action(self, action) -> None:
		last_turn = self.turn_history.pop()
		assert last_turn.action == action
		self.cur_player = last_turn.player
		self.prev_player = last_turn.prev_player
		self.dice = last_turn.dice
		self.double_turn = last_turn.double_turn

		#print(self.encoded_move_to_BAN(action, self.cur_player))

		moves = self.decode_checker_move(action, self.cur_player)
		moves[1] = Move(self.cur_player, moves[1].pos, moves[1].num, last_turn.second_move_hit)
		moves[0] = Move(self.cur_player, moves[0].pos, moves[0].num, last_turn.first_move_hit)
		
		self.undo_move(moves[1])
		self.undo_move(moves[0])

		if not self.double_turn:
			self.turn_num -= 1


	def remove_die(self, dice, die):
		for i in range(len(dice)):
			if die == dice[i]:
				return dice[0:i] + dice[i+1:]

	# Here we can implement logic that improves the engine, such as removing duplicate moves.
	# This function should modify self.moves_list

	def process_legal_checker_moves(self, player, max_moves):
		if max_moves == 0:
			return [[Move(player, self.pass_pos, -1, False), Move(player, self.pass_pos, -1, False)]]

		legal_actions = []
		max_roll = -1
		for move in self.moves_list:
			if max_moves == 2:
				if len(move) == 2:
					legal_actions.append(move)
			elif max_moves == 1:
				max_roll = max(max_roll, move[0].num)

		if max_moves == 1:
			for move in self.moves_list:
				if move[0].num == max_roll:
					legal_actions.append(move)

		return legal_actions

	def able_to_bear(self, player):
		if self.num_in_bar(player) > 0:
			return False
		total_pieces = self.beared[player]
		for pos in self.player_home(player):
			num = self.at(player, pos)
			total_pieces += num
		assert total_pieces <= self.checkers_per_side
		return total_pieces == self.checkers_per_side

	def furthest_checker_in_home(self, player):
		home = self.player_home(player)
		for point in home:
			if self.at(player, point) > 0:
				return point

	def get_legal_actions(self, player=None, dice=None):
		if player is None:
			player = self.cur_player
		if dice is None:
			dice = self.dice
		self.generate_legal_moves(player, dice)
		actions = []
		for move in self.moves_list:
			actions.append(self.encode_checker_move(move, dice))
		return actions

	def generate_legal_moves(self, player=None, dice=None):
		if player is None:
			player = self.cur_player
		if dice is None:
			dice = self.dice
		self.moves = []
		self.moves_list = []
		# updates self.moves_list
		max_moves = self.legal_checker_moves_outer(player, dice)
		self.moves_list = self.process_legal_checker_moves(player, max_moves)

	def legal_checker_moves_outer(self, player, dice):
		if len(self.moves) == 2:
			self.moves_list.append(self.moves)
			return len(self.moves)

		legal_moves = self.legal_checker_moves(player, dice)

		if len(legal_moves) == 0:
			self.moves_list.append(self.moves)
			return len(self.moves)

		max_moves = -1
		for move in legal_moves:
			self.moves.append(move)
			self.apply_move(move)
			new_dice = self.remove_die(dice, move.num)
			child_max = self.legal_checker_moves_outer(player, new_dice)
			self.undo_move(move)
			self.moves = self.moves.copy()
			self.moves.pop()
			max_moves = max(child_max, max_moves)
		return max_moves

	def legal_checker_moves(self, player, dice):
		moves = []
		if self.num_in_bar(player) > 0:
			# Must move checkers out of the bar
			for roll in dice:
				pos = self.get_pos_from_bar(roll, player)
				if self.is_legal_spot(pos, player):
					hit = self.is_hit(pos, player)
					moves.append(Move(player, self.bar_pos, roll, hit))
			return moves

		able_to_bear = self.able_to_bear(player)
		pos = self.player_home(player)[0] if able_to_bear else self.get_start_pos(player)
		direction = self.direction[player]
		while self.in_board(pos):
			if self.at(player, pos) > 0:
				for roll in dice:
					next_pos = self.get_pos(pos, roll, player)
					if self.is_score_spot(next_pos, player) and able_to_bear:
						if player == 0 and next_pos == 24 or \
						   player == 1 and next_pos == -1:
							moves.append(Move(player, pos, roll, False))
						else:
							if pos == self.furthest_checker_in_home(player):
								moves.append(Move(player, pos, roll, False))
					elif not self.is_score_spot(next_pos, player) and self.in_board(next_pos) and self.is_legal_spot(next_pos, player):
						hit = self.is_hit(next_pos, player)
						moves.append(Move(player, pos, roll, hit))
			pos += direction
		return moves

	def random_policy(self):
		i = random.randint(0, len(self.moves_list) - 1)
		return self.moves_list[i]

	def game_over(self):
		if self.beared[0] == 15:
			return True, 0
		elif self.beared[1] == 15:
			return True, 1
		elif self.turn_num >= self.max_turns:
			return True, Player.EMPTY
		else:
			return False, Player.EMPTY

	def get_reward_done(self, player):
		reward = 0
		done = False
		game_over, winner = self.game_over()
		if game_over:
			done = True
			if player == winner:
				reward = 1
			elif self.opponent[player] == winner or self.turn_num >= self.max_turns:
				reward = 0
		return reward, done, winner

	def step(self, action):
		self.apply_action(action)
		double_move = self.dice[0] == self.dice[1]
		if self.double_turn or not double_move:
			self.prev_player = self.cur_player
			self.cur_player = self.opponent[self.cur_player]
			if self.ddice:
				self.dice = self.ddice[self.turn_num]
			else:
				self.roll_dice()
			self.turn_num += 1

		self.double_turn = double_move and not self.double_turn

		reward, done, winner = self.get_reward_done(self.cur_player)
		obs = self.observation_tensor(self.cur_player)
		return self.cur_player, winner, obs, reward, done

	def step_back(self, action):
		self.undo_action(action)
		reward, done, winner = self.get_reward_done(self.cur_player)
		obs = self.observation_tensor(self.cur_player)
		return winner, obs, reward, done


	def play_one_turn(self, policy):
		self.roll_dice()

		double_move = self.dice[0] == self.dice[1]
		self.generate_legal_moves()

		moves = policy()
		for move in moves:
			self.apply_move(move)

		if double_move:
			self.generate_legal_moves()
			double_moves = policy()
			for move in double_moves:
				self.apply_move(move)
			moves.extend(double_moves)

		self.turn_num += 1
		self.cur_player = self.opponent[self.cur_player]
		return self.dice, moves

	def play_game(self):
		BAN_moves_logger = []
		game_over = False
		while not game_over:
			dice, moves = self.play_one_turn(self.random_policy)
			game_over, winner = self.game_over()

			if self.verbose:
				print("\nRolled: ", self.dice_to_unicode(dice))
				BAN_move = self.moves_to_BAN(moves, dice)
				BAN_moves_logger.append(BAN_move)
				print(BAN_move)
				print(self)

		score = self.beared[winner], self.beared[self.opponent[winner]]

		if self.verbose:
			print("The winner is %s!" % winner, score)
			for move in BAN_moves_logger:
				print(move)
		return winner, self.turn_num

	''' Use an encoding of the board in the following format:
		the first 4*24 points encode the first players pieces on the board
		the next  4*24 points encode the second players pieces on the board
		the final 6 points are player bar, player beared, cur_player == player, opponent bar, opponent beared, cur_player == opponent
	'''

	def observation_tensor(self, player):
		tensor = []
		opponent = self.opponent[player]

		for pos in range(self.board_size):
			num = self.at(player, pos)
			if num == 0:
				tensor.extend([0,0,0,0])
			else:
				tensor.append(int(num == 1))
				tensor.append(int(num == 2))
				tensor.append(int(num == 3))
				tensor.append((num-3) if (num > 3) else 0)
		
		for pos in range(self.board_size):
			num = self.at(opponent, pos)
			if num == 0:
				tensor.extend([0,0,0,0])
			else:
				tensor.append(int(num == 1))
				tensor.append(int(num == 2))
				tensor.append(int(num == 3))
				tensor.append((num-3) if (num > 3) else 0)

		tensor.append(self.bar[player])
		tensor.append(self.beared[player])
		tensor.append(int(self.cur_player == player))

		tensor.append(self.bar[opponent])
		tensor.append(self.beared[opponent])
		tensor.append(int(self.cur_player == opponent))

		return tensor

	def encode_checker_move(self, moves, dice=None):
		if dice is None:
			dice = self.dice
		dig0 = 25
		dig1 = 25
		high_roll_first = False
		# moves[0].num if moves[0].num > moves[1].num else moves[1].num
		high_roll = max(dice)

		if len(moves) != 0:
			pos1 = moves[0].pos
			if pos1 == self.bar_pos:
				pos1 = 24
			if pos1 != self.pass_pos:
				num1 = moves[0].num
				dig0 = pos1
				high_roll_first = num1 == high_roll

		if len(moves) > 1:
			pos2 = moves[1].pos
			if pos2 == self.bar_pos:
				pos2 = 24
			if pos2 != self.pass_pos:
				dig1 = pos2

		move = dig1 * 26 + dig0
		if not high_roll_first:
			move += 26*26
		return move

	def decode_checker_move(self, encoded_move, player=None, dice=None):
		if player is None:
			player = self.cur_player
		if dice is None:
			dice = self.dice
		high_roll_first = encoded_move < 26*26
		if not high_roll_first:
			encoded_move -= 26*26

		digits = (encoded_move % 26, encoded_move // 26)

		moves = []
		high_roll = dice[0]
		low_roll = dice[1]

		for i in range(0, 2):
			num = -1
			if i == 0:
				num = high_roll if high_roll_first else low_roll
			else:
				num = low_roll if high_roll_first else high_roll

			if digits[i] == 25:  # pass move
				moves.append(Move(player, self.pass_pos, -1, False))
			else:
				pos = self.bar_pos if digits[i] == 24 else digits[i]
				moves.append(Move(player, pos, num, False))
		return moves

	def encoded_move_to_BAN(self, encoded_move, player=None, dice=None):
		if player is None:
			player = self.cur_player
		if dice is None:
			dice = self.dice
		moves = self.decode_checker_move(encoded_move, player, dice)
		return self.moves_to_BAN(moves, dice)

	''' 
	Legal Singular Moves:
		move to an open point (open: not more than one opposing checkers on spot)
	Modifiers:
		if piece of player on bar:
			must move piece off first, check if more pieces on bar
		elif able to bear:
			bear moves are legal
		else:
			normal generation of moves

	Recursive Procedure:
		Start at furthest man from home
		Scan towards home, stopping at squares with pieces of that player
		First determine which state the board is in (what kinds of moves are legal)
		apply the current die face to the piece 
			if legal_moves:
				update the board
				call recursively for the remaining die faces, start the next scan at the furthest point from home
			else:
				continue to the next spot with a piece of correct player and try again
	'''

	'''
		Number of Distinct Actions is 1352:
		can have up to 25*26 + 25 + 26*26 moves
		Encoded from {0, 1, ..., 1350, 1351}
		base 26: {0, 1, ..., 23, bar_pos, pass_pos} => first 676 numbers
	'''