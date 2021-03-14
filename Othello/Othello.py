from enum import Enum
from typing import NamedTuple, Tuple, List

class Color(Enum):
	WHITE = 0
	BLACK = 1
	EMPTY = 2


class Square(Enum):
	FRIENDLY = 0  # proposed square contains a piece of the same color
	ENEMY = 1  # proposed square contains a piece of different color
	EMPTY = 2  # proposed square is empty


class Othello:
	def __init__(self):
		self.board = Board() # instantiate an empty board
		self.curr_color = Color.BLACK
		self.opp_color = Color.WHITE
		self.total_pieces = [32, 32]
		self.legal_moves = self.get_legal_moves()


	def turn(self, spot):
		assert board.is_spot_in_board(*spot)

		# Set the chosen square to the current player's color
		self.board.set_square(spot, self.curr_color)

		# Retrieve tiles to be flipped
		flips = self.get_flips(spot) # TODO: get this from self.legal_moves instead for speedup?
		
		# Flip tiles
		for flip in flips:
			self.board.set_square(flip, self.curr_color)

		num_flips = len(flips)
		self.total_pieces[self.curr_color.value] += num_flips + 1 # + 1 for {spot}
		self.total_pieces[self.opp_color.value]  -= num_flips

		# Swap current and opposite player
		self.curr_color, self.opp_color = self.opp_color, self.curr_color

		# Compute the legal moves for the next turn
		# self.legal_moves = self.get_legal_moves()

	def __str__(self):
		return '\n'.join(str(s) for s in self.legal_moves.items()) + "\n\n\n" + str(self.board)

	def get_square_status(self, spot):
		assert self.board.is_spot_in_board(*spot)
		square = self.board.get_square(*spot) # one of Color.WHITE, Color.BLACK, Color.EMPTY
		if square == Color.EMPTY:
			return Square.EMPTY
		if square == self.curr_color:
			return Square.FRIENDLY
		return Square.ENEMY

	def get_flips_in_direction(self, spot, move):
		if not self.board.is_spot_in_board(*spot):
			return []
		spot = Board.move(spot, move)
		seen_enemy = False
		flips = []

		while self.board.is_spot_in_board(*spot):
			status = self.get_square_status(spot)
			if status == Square.EMPTY:
				return []
			if status == Square.ENEMY:
				seen_enemy = True
				flips.append(spot)
			elif status == Square.FRIENDLY and seen_enemy:
				return flips
			spot = Board.move(spot, move)
		return []

	def get_flips(self, spot):
		if self.get_square_status(spot) != Square.EMPTY:
			return []

		flips = []
		for move in Board.get_move_directions():
			flips.extend(self.get_flips_in_direction(spot, move))
		return flips

	def get_legal_moves(self):
		spots = {}
		for spot in self.board.get_empty_positions():
			flips = self.get_flips(spot)
			if len(flips) > 0:
				spots[spot] = flips
				#spots.append({
				#	'spot': spot,
				#	'flips': flips,
				#	'num_flips': len(flips)
				# })
		return spots


class Board:
	def __init__(self, rows=8, cols=8):
		self.board = [
			Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY,
			Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY,
			Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY,
			Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.BLACK, Color.WHITE, Color.EMPTY, Color.EMPTY, Color.EMPTY,
			Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.WHITE, Color.BLACK, Color.EMPTY, Color.EMPTY, Color.EMPTY,
			Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY,
			Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY,
			Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY
		]
		self.rows = rows
		self.cols = cols

	def __str__(self):
		board = ''
		for x in range(self.rows):
			row = ''
			for y in range(self.cols):
				row += ' ' + self.square_to_unicode((x, y))
			board += row.strip() + '\n'
		return board

	def is_spot_in_board(self, x, y):
		return 0 <= x < self.rows and 0 <= y < self.cols

	def move(spot, move):
		return spot[0] + move[0], spot[1] + move[1]

	def get_move_directions():
		# UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT
		return [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

	def get_square(self, x: int, y: int) -> Color:
		assert self.is_spot_in_board(x, y)
		return self.board[x * self.rows + y]

	def set_square(self, x: int, y: int, color: Color) -> None:
		self.board[x * self.rows + y] = color

	def flip_square(self, spot: Tuple[int, int])-> None:
		current_color = Board.get_square(*spot)
		assert current_color is not Color.EMPTY
		color = None
		if current_color is Color.BLACK:
			color = Color.WHITE
		if current_color is Color.WHITE:
			color = Color.BLACK
		self.set_square(*spot, color)


	def get_all_positions(self) -> List[Tuple[int, int]]:
		return [(i, j) for j in range(self.cols) for i in range(self.rows)]

	def get_positions_of_color(self, color):
		positions = []
		for pos in self.get_all_positions():
			if self.get_square(*pos) == color:
				positions.append(pos)
		return positions

	def get_empty_positions(self):
		return self.get_positions_of_color(Color.EMPTY)

	def get_white_positions(self):
		return self.get_positions_of_color(Color.WHITE)

	def get_black_positions(self):
		return self.get_positions_of_color(Color.BLACK)
 
	def square_to_unicode(self, spot):
		color = self.get_square(*spot)
		if color == Color.WHITE:
			return '⚪'
		elif color == Color.BLACK:
			return '⚫'
		else:
			return '-'

if __name__ == '__main__':
	game = Othello()
	print(game)
	print(game.board.get_empty_positions())
	print(game.board.get_white_positions())
	print(game.board.get_black_positions())