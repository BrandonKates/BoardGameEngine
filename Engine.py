# Board representation:
# the board is a list of pieces (objects)
#
#   b b b b b b b b
#   b b b b b b b b
#   x x x x x x x x
#   x x x x x x x x
#   x x x x x x x x
#   x x x x x x x x
#   w w w w w w w w
#   w w w w w w w w
#

# Helper Functions

from enum import Enum
from typing import NamedTuple

position_to_coordinates = {
	'a8': (0, 0), 'b8': (0, 1), 'c8': (0, 2), 'd8': (0, 3), 'e8': (0, 4), 'f8': (0, 5), 'g8': (0, 6), 'h8': (0, 7),
	'a7': (1, 0), 'b7': (1, 1), 'c7': (1, 2), 'd7': (1, 3), 'e7': (1, 4), 'f7': (1, 5), 'g7': (1, 6), 'h7': (1, 7),
	'a6': (2, 0), 'b6': (2, 1), 'c6': (2, 2), 'd6': (2, 3), 'e6': (2, 4), 'f6': (2, 5), 'g6': (2, 6), 'h6': (2, 7),
	'a5': (3, 0), 'b5': (3, 1), 'c5': (3, 2), 'd5': (3, 3), 'e5': (3, 4), 'f5': (3, 5), 'g5': (3, 6), 'h5': (3, 7),
	'a4': (4, 0), 'b4': (4, 1), 'c4': (4, 2), 'd4': (4, 3), 'e4': (4, 4), 'f4': (4, 5), 'g4': (4, 6), 'h4': (4, 7),
	'a3': (5, 0), 'b3': (5, 1), 'c3': (5, 2), 'd3': (5, 3), 'e3': (5, 4), 'f3': (5, 5), 'g3': (5, 6), 'h3': (5, 7),
	'a2': (6, 0), 'b2': (6, 1), 'c2': (6, 2), 'd2': (6, 3), 'e2': (6, 4), 'f2': (6, 5), 'g2': (6, 6), 'h2': (6, 7),
	'a1': (7, 0), 'b1': (7, 1), 'c1': (7, 2), 'd1': (7, 3), 'e1': (7, 4), 'f1': (7, 5), 'g1': (7, 6), 'h1': (7, 7)
}

coordinates_to_position = [
	['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'],
	['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'],
	['a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6'],
	['a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5'],
	['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4'],
	['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3'],
	['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'],
	['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
]



class PieceType(Enum):
	EMPTY = 0
	ROOK = 1
	KNIGHT = 2
	BISHOP = 3
	QUEEN = 4
	KING = 5
	PAWN = 6


class Color(Enum):
	WHITE = 0
	BLACK = 1
	EMPTY = 2

class Piece(NamedTuple):
	type: PieceType
	color: Color
	
	def toUnicode(self):
		white_unicode = '♖♘♗♕♔♙'
		black_unicode = '♜♞♝♛♚♟'
		if self.color == Color.EMPTY:
			return '.'
		elif self.color == Color.WHITE:
			return white_unicode[self.type.value - 1]
		else:
			return black_unicode[self.type.value - 1]
	
	def toString(self):
		white_string = 'RNBQKP'
		black_string = 'rnbqkp'
		if self.type == PieceType.EMPTY:
			return ' '
		if self.color == Color.WHITE:
			return white_string[self.type.value - 1]
		else:
			return black_string[self.type.value - 1]


class Moves(Enum):
	UP = (1, 0)
	DOWN = (-1, 0)
	LEFT = (0, 1)
	RIGHT = (0, -1)
	UP_LEFT = (1, 1)
	UP_RIGHT = (1, -1)
	DOWN_LEFT = (-1, 1)
	DOWN_RIGHT = (-1, -1)

class Square(Enum):
	EMPTY = 0  # proposed square is empty
	FRIENDLY = 1  # proposed square contains a piece of the same color
	ENEMY = 2  # proposed square contains a piece of different color

#KnightOffsets = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]


class Engine:
	def __init__(self):
		self.turn = 0
		self.player = 'white'
		self.board = ChessBoard()

	def update_player(self, turn):
		return 'white' if turn % 2 == 0 else 'black'

	def start_new_game(self):
		pass


class ChessBoard:
	def __init__(self):
		self.board = \
	[
		[Piece(PieceType.ROOK,  Color.BLACK), Piece(PieceType.KNIGHT, Color.BLACK), Piece(PieceType.BISHOP, Color.BLACK), Piece(PieceType.QUEEN, Color.BLACK), 
	 	 Piece(PieceType.KING,  Color.BLACK), Piece(PieceType.BISHOP, Color.BLACK), Piece(PieceType.KNIGHT, Color.BLACK), Piece(PieceType.ROOK,  Color.BLACK)],
	 	[Piece(PieceType.PAWN,  Color.BLACK), Piece(PieceType.PAWN,   Color.BLACK), Piece(PieceType.PAWN,   Color.BLACK), Piece(PieceType.PAWN,  Color.BLACK), 
	 	 Piece(PieceType.PAWN,  Color.BLACK), Piece(PieceType.PAWN,   Color.BLACK), Piece(PieceType.PAWN,   Color.BLACK), Piece(PieceType.PAWN,  Color.BLACK)],
	 	[Piece(PieceType.EMPTY, Color.EMPTY), Piece(PieceType.EMPTY,  Color.EMPTY), Piece(PieceType.EMPTY,  Color.EMPTY), Piece(PieceType.EMPTY, Color.EMPTY), 
	 	 Piece(PieceType.EMPTY, Color.EMPTY), Piece(PieceType.EMPTY,  Color.EMPTY), Piece(PieceType.EMPTY,  Color.EMPTY), Piece(PieceType.EMPTY, Color.EMPTY)],
		[Piece(PieceType.EMPTY, Color.EMPTY), Piece(PieceType.EMPTY,  Color.EMPTY), Piece(PieceType.EMPTY,  Color.EMPTY), Piece(PieceType.EMPTY, Color.EMPTY), 
		 Piece(PieceType.EMPTY, Color.EMPTY), Piece(PieceType.EMPTY,  Color.EMPTY), Piece(PieceType.EMPTY,  Color.EMPTY), Piece(PieceType.EMPTY, Color.EMPTY)],
		[Piece(PieceType.EMPTY, Color.EMPTY), Piece(PieceType.EMPTY,  Color.EMPTY), Piece(PieceType.EMPTY,  Color.EMPTY), Piece(PieceType.EMPTY, Color.EMPTY), 
		 Piece(PieceType.EMPTY, Color.EMPTY), Piece(PieceType.EMPTY,  Color.EMPTY), Piece(PieceType.EMPTY,  Color.EMPTY), Piece(PieceType.EMPTY, Color.EMPTY)],
		[Piece(PieceType.EMPTY, Color.EMPTY), Piece(PieceType.EMPTY,  Color.EMPTY), Piece(PieceType.EMPTY,  Color.EMPTY), Piece(PieceType.EMPTY, Color.EMPTY), 
		 Piece(PieceType.EMPTY, Color.EMPTY), Piece(PieceType.EMPTY,  Color.EMPTY), Piece(PieceType.EMPTY,  Color.EMPTY), Piece(PieceType.EMPTY, Color.EMPTY)],
		[Piece(PieceType.PAWN,  Color.WHITE), Piece(PieceType.PAWN,   Color.WHITE), Piece(PieceType.PAWN,   Color.WHITE), Piece(PieceType.PAWN,  Color.WHITE), 
	 	 Piece(PieceType.PAWN,  Color.WHITE), Piece(PieceType.PAWN,   Color.WHITE), Piece(PieceType.PAWN,   Color.WHITE), Piece(PieceType.PAWN,  Color.WHITE)],
	 	[Piece(PieceType.ROOK,  Color.WHITE), Piece(PieceType.KNIGHT, Color.WHITE), Piece(PieceType.BISHOP, Color.WHITE), Piece(PieceType.QUEEN, Color.WHITE), 
	 	 Piece(PieceType.KING,  Color.WHITE), Piece(PieceType.BISHOP, Color.WHITE), Piece(PieceType.KNIGHT, Color.WHITE), Piece(PieceType.ROOK,  Color.WHITE)]
	]
	self.prevBoard = self.board.copy()
	self.enPassant = None # en-passant can only be performed immediately after the opponent makes the move with their pawn
	self.castling_rights = {'white_left': True, 'white_right': True, 'black_left' : True, 'black_right' : True}
	def __str__(self):
		return self.toUnicode()

	def toString(self):
		board = ''
		for i in range(0, 8):
			row = ''
			for j in range(0, 8):
				row += self.board[i][j].toString()
			board += row + "\n"
		return board

	def toUnicode(self):
		board = ''
		for i in range(0, 8):
			row = ''
			for j in range(0, 8):
				row += self.board[i][j].toUnicode()
			board += row + "\n"
		return board

	def pos_as_tuple(self, pos):
		if type(pos) == tuple:
			return pos
		if type(pos) == str:
			return position_to_coordinates[pos]
	
	def at(self, pos):
		x,y = self.pos_as_tuple(pos)
		return self.board[x][y]

	def piece_at(self, pos):
		return self.at(pos) != None

	def color_at(self, pos):
		p = self.at(pos)
		return p.color if p is not None else None

	def update_position(self, position : tuple, pieceType : PieceType, color : Color) -> None:
		self.prevBoard = self.board.copy()
		x,y = position
		self.board[x][y] = Piece(pieceType, color)

	def update_position_with(self, position : tuple, piece : Piece) -> None:
		t = piece.type
		color = piece.color
		self.update_position(self, position, t, color)


	def update_en_passant(self, from_pos, to_pos):
		self.enPassant = None
		from_x, from_y = self.pos_as_tuple(from_pos)
		to_x, to_y = self.pos_as_tuple(to_pos)
		assert from_x != to_x
		if from_y == to_y and abs(from_x - to_x) == 2:
			self.enPassant = to_pos


	# TODO: self.castling_rights = {'white_left': True, 'white_right': True, 'black_left' : True, 'black_right' : True}
	# must also check if any squares the king passes through are under attack by enemy team, and the king must not be in check
	def update_castling_rights(self, piece, from_pos):
		if piece.color == Color.WHITE:
			if piece.type == PieceType.KING:
				self.castling_rights['white_left'] = False
				self.castling_rights['white_right'] = False
			elif piece.type == PieceType.ROOK:
				if from_pos == 'a1':
					self.castling_rights['white_left'] = False
				elif from_pos == 'h1':
					self.castling_rights['white_right'] = False
		elif piece.color == Color.BLACK:
			if piece.type == PieceType.KING:
				self.castling_rights['black_left'] = False
				self.castling_rights['black_right'] = False
			elif piece.type == PieceType.ROOK:
				if from_pos == 'a8':
					self.castling_rights['black_right'] = False
				elif from_pos == 'h8':
					self.castling_rights['black_left'] = False


	# move needs to take a from_pos and to_pos and update the board accordingly, additionally, it should update other features like en_passant, castling, and promotion
	def move(self, from_pos, to_pos):
		piece = self.at(from_pos)
		self.update_position_with(to_pos, piece)
		if piece.type is PieceType.PAWN:
			self.update_en_passant(from_pos, to_pos)
		self.update_castling_rights(piece, from_pos)

	def is_empty(self, pos):
		piece = self.at(pos)
		return piece.type == PieceType.EMPTY

	def is_enemy(self, pos, color):
		piece = self.at(pos)
		return not self.is_empty(pos) and piece.color != color
		
	def is_friendly(self, pos, color):
		return not self.is_enemy(pos, color)

	# Can move this function outside to helper -> doesn't require chessboard class properties (unless the chessboard size can change)
	def in_board(self, pos):
		x,y = self.pos_as_tuple(pos)
		if x < 0 or x > 7 or y < 0 or y > 7:
			return False
		return True

	# Can move this function outside to helper -> doesn't require chessboard class properties
	def calculate_position(self, pos, offset, color, spaces=1):
		pos_x, pos_y = self.pos_as_tuple(pos)
		x_offset, y_offset = offset.value if type(offset) is Moves else offset
		if color is Color.WHITE:
			pos_x -= x_offset * spaces # -x is up for white   | +x is down for white
			pos_y -= y_offset * spaces # -y is left for white | +y is right for white
		elif color is Color.BLACK:
			pos_x += x_offset * spaces # +x is up for black   | -x is down for black
			pos_y += y_offset * spaces # +y is left for black | -y is right for white
		return pos_x, pos_y

	# check the position x,y for allied or enemy pieces
	def check_position_for_pieces(self, pos, color):
		proposed_color = self.color_at(pos)
		if proposed_color is Color.EMPTY:
			return Square.EMPTY
		elif proposed_color == color:
			return Square.FRIENDLY
		else:
			return Square.ENEMY

	# this works for every piece except pawn, which cannot capture by moving forward
	def check_multiple_positions(self, pos, offset, color):
		legal_moves = []
		spaces = 1
		while True:
			next_pos = self.calculate_position(pos, offset, color, spaces)
			if self.in_board(next_pos):
				check = self.check_position_for_pieces(next_pos, color)
				if check == Square.FRIENDLY:
					break
				legal_moves.append(next_pos)
				if check == Square.ENEMY:
					break
				spaces += 1
			else:
				break
		return legal_moves

	def convert_moves_to_positions(self, moves):
		return [coordinates_to_position[move[0]][move[1]] for move in moves]


	def is_pawn_starting_rank(self, pos, color):
		x,y = self.pos_as_tuple(pos)
		pos = coordinates_to_position[x][y]
		if color == Color.WHITE:
			return pos[1] == '2' # pawn needs to be in second row for white
		elif color == Color.BLACK:
			return pos[1] == '7' # pawn needs to be in seventh row for black
		else:
			return False

	def is_pawn_promotion_rank(self, pos, color)
		x,y = self.pos_as_tuple(pos)
		pos = coordinates_to_position[x][y]
		return pos[1] == '1' or pos[1] == '8'

	# returns a tuple, represent if color can castle to the (left, right) sides O-O-O or O-O
	def can_castle(self, color):
		left, right = False, False
		if color == Color.WHITE:
			# check left first
			if is_empty('b1') and is_empty('c1') and is_empty('d1'):
				left = True
			if is_empty('f1') and is_empty('g1'):
				right = True
		else:
			if is_empty('b8') and is_empty('c8') and is_empty('d8'):
				right = True
			if is_empty('f8') and is_empty('g8'):
				left = True
		return left, right


	def opponent_color(self, color):
		if color is Color.WHITE:
			return Color.BLACK
		elif color is Color.BLACK:
			return Color.WHITE
		else:
			return Color.EMPTY

	def under_attack(self, pos, our_color):
		opp_color = self.opponent_color(our_color)

		king_dests = self.generate_king_moves(pos, our_color)
		for dest in king_dests:
			if self.at(dest) is Piece(PieceType.KING,  opp_color):
				return True

		bishop_dests = self.generate_bishop_moves(pos, our_color)
		for dest in bishop_dests:
			if self.at(dest) is Piece(PieceType.BISHOP, opp_color) or
			   self.at(dest) is Piece(PieceType.QUEEN, opp_color):
			   return True

		rook_dests = self.generate_rook_moves(pos, our_color)
		for dest in rook_dests:
			if self.at(dest) is Piece(PieceType.ROOK, opp_color) or
			   self.at(dest) is Piece(PieceType.QUEEN, opp_color):
			   return True

		knight_dests = self.generate_knight_moves(pos, our_color)
		for dest in knight_dests:
			if self.at(dest) is Piece(PieceType.KNIGHT,  opp_color):
				return True

		# TODO: NO En Passant here
		pawn_capture_dests = self.generate_pawn_capture_moves(pos, our_color, en_passant=False)
		for dest in pawn_capture_dests:
			if self.at(dest) is Piece(PieceType.PAWN, opp_color):
				return True
		return False

	#TODO:
	def generate_pawn_moves(self, pos, color):
		legal_moves = []
		p1 = self.calculate_position(pos, Moves.UP, color)  # up 1
		if self.in_board(p1) and self.check_position_for_pieces(p1, color) is Square.EMPTY:
			legal_moves.append(p1)

		if self.is_pawn_starting_rank(pos, color): # if pawn is in its starting position --> need to redo this, check the file it's in for white/black
			p2 = self.calculate_position(pos, Moves.UP, color, spaces=2)
			if self.in_board(p2) and self.check_position_for_pieces(p2, color) is Square.EMPTY:
				legal_moves.append(p2)

		# TODO: Add a check for Pawn Promotion (needs to happen the same turn as the piece moves)
		return self.convert_moves_to_positions(legal_moves)

	def generate_pawn_capture_moves(self, pos, color, en_passant = True):
		p3 = self.calculate_position(pos, Moves.UP_RIGHT, color)
		if self.in_board(p3) and self.check_position_for_pieces(p3, color) is Square.ENEMY:
			legal_moves.append(p3)

		p4 = self.calculate_position(pos, Moves.UP_LEFT, color)
		if self.in_board(p4) and self.check_position_for_pieces(p4, color) is Square.ENEMY:
			legal_moves.append(p4)
		return self.convert_moves_to_positions(legal_moves)
		# TODO: Add a case for En Passant (need access to the previous board state as well)

	def generate_rook_moves(self, pos, color):
		rook_offsets = [Moves.UP, Moves.DOWN, Moves.LEFT, Moves.RIGHT]
		legal_moves = []
		for offset in rook_offsets:
			legal_moves.extend(self.check_multiple_positions(pos, offset, color))
		return self.convert_moves_to_positions(legal_moves)


	def generate_knight_moves(self, pos, color):
		legal_moves = []
		knight_offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
		for offset in knight_offsets:
			new_pos = self.calculate_position(pos, offset, color)
			if self.in_board(new_pos) and self.check_position_for_pieces(new_pos, color) in (Square.ENEMY, Square.EMPTY):
				legal_moves.append(new_pos)
		return self.convert_moves_to_positions(legal_moves)

	def generate_bishop_moves(self, pos, color):
		bishop_offsets = [Moves.UP_RIGHT, Moves.UP_LEFT, Moves.DOWN_RIGHT, Moves.DOWN_LEFT]
		legal_moves = []
		for offset in bishop_offsets:
			legal_moves.extend(self.check_multiple_positions(pos, offset, color))
		return self.convert_moves_to_positions(legal_moves)

	def generate_queen_moves(self, pos, color):
		queen_offsets = [Moves.UP, Moves.DOWN, Moves.RIGHT, Moves.LEFT, Moves.UP_RIGHT, Moves.UP_LEFT, Moves.DOWN_RIGHT, Moves.DOWN_LEFT]
		legal_moves = []
		for offset in queen_offsets:
			legal_moves.extend(self.check_multiple_positions(pos, offset, color))
		return self.convert_moves_to_positions(legal_moves)

	def generate_king_moves(self, pos, color):
		legal_moves = []
		offsets = [Moves.UP, Moves.DOWN, Moves.RIGHT, Moves.LEFT, Moves.UP_RIGHT, Moves.UP_LEFT, Moves.DOWN_RIGHT, Moves.DOWN_LEFT]
		for offset in offsets:
			new_pos = self.calculate_position(pos, offset, color)
			if self.in_board(new_pos) and self.check_position_for_pieces(new_pos, color) in (Square.ENEMY, Square.EMPTY):
				legal_moves.append(new_pos)
		return self.convert_moves_to_positions(legal_moves)