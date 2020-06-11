# Board representation:
# the board is a list of pieces (objects)
#
#	b b b b b b b b
#   b b b b b b b b
#   x x x x x x x x
#   x x x x x x x x
#   x x x x x x x x
#   x x x x x x x x
#   w w w w w w w w
#   w w w w w w w w
#

# Helper Functions

posToCoords = {
	'a8': (0,0),'b8': (0,1),'c8': (0,2),'d8': (0,3),'e8': (0,4),'f8': (0,5),'g8': (0,6),'h8': (0,7),
	'a7': (1,0),'b7': (1,1),'c7': (1,2),'d7': (1,3),'e7': (1,4),'f7': (1,5),'g7': (1,6),'h7': (1,7),
	'a6': (2,0),'b6': (2,1),'c6': (2,2),'d6': (2,3),'e6': (2,4),'f6': (2,5),'g6': (2,6),'h6': (2,7),
	'a5': (3,0),'b5': (3,1),'c5': (3,2),'d5': (3,3),'e5': (3,4),'f5': (3,5),'g5': (3,6),'h5': (3,7),
	'a4': (4,0),'b4': (4,1),'c4': (4,2),'d4': (4,3),'e4': (4,4),'f4': (4,5),'g4': (4,6),'h4': (4,7),
	'a3': (5,0),'b3': (5,1),'c3': (5,2),'d3': (5,3),'e3': (5,4),'f3': (5,5),'g3': (5,6),'h3': (5,7),
	'a2': (6,0),'b2': (6,1),'c2': (6,2),'d2': (6,3),'e2': (6,4),'f2': (6,5),'g2': (6,6),'h2': (6,7),
	'a1': (7,0),'b1': (7,1),'c1': (7,2),'d1': (7,3),'e1': (7,4),'f1': (7,5),'g1': (7,6),'h1': (7,7)
}

coordsToPos = [
	['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'],
	['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'],
	['a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6'],
	['a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5'],
	['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4'],
	['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3'],
	['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'],
	['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
]


class Engine:
	def __init__(self):
		self.turn = 0
		self.player = 'white'
		self.board = ChessBoard()
	
	def update_player(self, turn):
		return 'white' if turn % 2 == 0 else 'black'

class ChessBoard:
	def __init__(self):
		self.board = \
		[
			[Rook('a8', 'black'), Knight('b8', 'black'), Bishop('c8', 'black'), Queen('d8', 'black'), King('e8','black'), Bishop('f8', 'black'), Knight('g8', 'black'), Rook('h8', 'black')], 
			[Pawn('a7', 'black'), Pawn('b7', 'black'), Pawn('c7','black'), Pawn('d7', 'black'), Pawn('e7','black'), Pawn('f7', 'black'), Pawn('g7','black'), Pawn('h7', 'black')],
			[None, None, None, None, None, None, None, None],
			[None, None, None, None, None, None, None, None],
			[None, None, None, None, None, None, None, None],
			[None, None, None, None, None, None, None, None],
			[Pawn('a2', 'white'), Pawn('b2', 'white'), Pawn('c2','white'), Pawn('d2', 'white'), Pawn('e2','white'), Pawn('f2', 'white'), Pawn('g2','white'), Pawn('h2', 'white')],
			[Rook('a1', 'white'), Knight('b1', 'white'), Bishop('c1', 'white'), Queen('d1', 'white'), King('e1','white'), Bishop('f1', 'white'), Knight('g1', 'white'), Rook('h1', 'white')]
		]

	def __str__(self):
		board = ''
		for i in range(0,8):
			row = ''
			for j in range(0,8):
				piece = self.board[i][j]
				if piece is None:
					row += 'x'
					if j <7:
						row += ' '
				else:
					row += piece.unicode
			board += row + "\n"
		return board


	def at(self, pos):
		if type(pos) == dict:
			return self.board[pos['x']][pox['y']]
		if type(pos) == tuple:
			return self.board[pos[0]][pos[1]]

	def piece_at(self, pos):
		return self.at(pos) != None

	def color_at(self, pos):
		p = self.at(pos)
		return p.color if p is not None else None

class Piece():
	def __init__(self, pos, color):
		self.pos = self.set_initial_pos(pos)# {'x' : start_pos , 'y': start_pos}
		self.color = color # 'white' or 'black'
		self.letter = None # example: 'B' for Bishop
		self.unicode = None # unicode representation for each type of chess piece
	

	def set_initial_pos(self, pos):
		x,y = None, None
		if type(pos) == str:
			x,y = posToCoords[pos]
		if type(pos) == tuple:
			x,y = pos
		return {'x': x, 'y': y}


	def get_legal_moves(self, state):
		self.board = state.board


	def check_pos(self, pos_fn):
		legal_moves = []
		spaces = 1
		while True:
			next_pos = pos_fn(spaces)
			if next_pos:
				check = self.checkPosForPieces(*next_pos)
				if check == 0:
					break
				legal_moves.append(next_pos)
				if check == 2:
					break
				spaces += 1
			else:
				break
		return legal_moves

	# check the position x,y for allied or enemy pieces
	def checkPosForPieces(self, x, y):
		proposed_color = self.board.color_at((x,y))
		if self.color == proposed_color:
			return 0 # white piece can't move onto or past another white piece 0==False (unless castling)
		if proposed_color == None:
			return 1 # white piece can move onto or past an empty square 1==True
		if self.color != proposed_color:
			return 2 # white piece can capture a black piece, however cannot move any further: 2==True + special case

	def checkLegalPos(self, x, y):
		if x < 0 or x > 7 or y < 0 or y > 7:
			return False
		posForPieces = self.checkPosForPieces(x, y)
		if posForPieces == 0:
			return False
		if posForPieces == 1:
			return x,y
		if posForPieces == 2:
			return x,y


	def pos_update(self, x_offset, y_offset, spaces = 1):
		if self.color == 'white':
			pos_x = self.pos['x'] - x_offset * spaces # -x is up for white   | +x is down for white
			pos_y = self.pos['y'] - y_offset * spaces # -y is left for white | +y is right for white
		if self.color == 'black':
			pos_x = self.pos['x'] + x_offset * spaces # +x is up for black   | -x is down for black
			pos_y = self.pos['y'] + y_offset * spaces # +y is left for black | -y is right for white
		return pos_x, pos_y

	# relative upward position for white and black side --> only really useful for pawns?
	def pos_up(self, spaces=1):
		pos = self.pos_update(x_offset = 1, y_offset = 0, spaces = spaces)
		return self.checkLegalPos(*pos)

	def pos_down(self, spaces=1):
		pos = self.pos_update(x_offset = -1, y_offset = 0, spaces = spaces)
		return self.checkLegalPos(*pos) 

	def pos_left(self, spaces=1):
		# need to check if we go off the board left or right
		pos = self.pos_update(x_offset = 0, y_offset = 1, spaces = spaces)
		return self.checkLegalPos(*pos)

	def pos_right(self, spaces=1):
		# need to check if we go off the board left or right
		pos = self.pos_update(x_offset = 0, y_offset = -1, spaces = spaces)
		return self.checkLegalPos(*pos)

	# diagonal move up and to the left
	def pos_up_left(self, spaces=1):
		# need to check if we go off the board left or right
		pos = self.pos_update(x_offset = 1, y_offset = 1, spaces = spaces)
		return self.checkLegalPos(*pos)
	#
	def pos_up_right(self, spaces=1):
		# need to check if we go off the board left or right
		pos = self.pos_update(x_offset = 1, y_offset = -1, spaces = spaces)
		return self.checkLegalPos(*pos)
	#
	def pos_down_left(self, spaces=1):
		pos = self.pos_update(x_offset = -1, y_offset = 1, spaces = spaces)
		return self.checkLegalPos(*pos)
	#
	def pos_down_right(self, spaces=1):
		pos = self.pos_update(x_offset = -1, y_offset = -1, spaces = spaces)
		return self.checkLegalPos(*pos)

class Pawn(Piece):
	# Pawn can move ahead 1 or 2 squares or capture piece or en passant
	def __init__(self, start_pos, color):
		super(Pawn, self).__init__(start_pos, color)
		self.start_pos = self.set_initial_pos(start_pos)
		self.letter = 'p'
		if self.color == 'white':
			self.unicode = '♙'
		else:
			self.unicode = '♟︎';

	def get_legal_moves(self, state):
		super(Pawn, self).get_legal_moves(state)
		board = state.board
		turn = state.turn
		
		legal_moves = []
		m1 = self.pos_up(spaces=1)
		if m1:
			legal_moves.append(m1)
		if self.pos['x'] == self.start_pos['x'] and self.pos['y'] == self.start_pos['y']:
			m2 = self.pos_up(spaces=2)
			if m2:
				legal_moves.append(m2)
		m3 = self.pos_up_right(spaces=1) # for captures
		m4 = self.pos_up_left(spaces=1)  # for captures]
		if m3:
			legal_moves.append(m3)
		if m4:
			legal_moves.append(m4)
		return [coordsToPos[move[0]][move[1]] for move in legal_moves]


# TODO: Add Castling, 
class Rook(Piece):
	# rook moves forward as many squares until it captures or reaches end of row 
	def __init__(self, start_pos, color):
		super(Rook, self).__init__(start_pos, color)
		self.letter = 'R'
		if self.color == "white":
			self.unicode = '♖'
		else:
			self.unicode = '♜'

	def get_legal_moves(self, state):
		super(Rook, self).get_legal_moves(state)
		offset_fns = [self.pos_up, self.pos_down, self.pos_left, self.pos_right]
		legal_moves = []
		for offset_fn in offset_fns:
			legal_moves.extend(self.check_pos(offset_fn))
		return [coordsToPos[move[0]][move[1]] for move in legal_moves]


class Knight(Piece):
	def __init__(self, start_pos, color):
		super(Knight, self).__init__(start_pos, color)
		self.letter = 'N'
		if self.color == "white":
			self.unicode = '♘'
		else:
			self.unicode = '♞'

	def knight_moves(self):
		moves = []
		offsets = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
		for offset_x, offset_y in offsets:
			pos = self.pos_update(offset_x, offset_y)
			if self.checkLegalPos(*pos):
				moves.append(pos)
		return moves

	def get_legal_moves(self, state):
		super(Knight, self).get_legal_moves(state)
		legal_moves = self.knight_moves()
		return [coordsToPos[move[0]][move[1]] for move in legal_moves]		


class Bishop(Piece):
	def __init__(self, start_pos, color):
		super(Bishop, self).__init__(start_pos, color)
		self.letter = 'B'
		if self.color == 'white':
			self.unicode = '♗'
		else:
			self.unicode = '♝'

	def get_legal_moves(self, state):
		super(Bishop, self).get_legal_moves(state)
		offset_fns = [self.pos_up_right, self.pos_up_left, self.pos_down_right, self.pos_down_left]
		legal_moves = []
		for offset_fn in offset_fns:
			legal_moves.extend(self.check_pos(offset_fn))
		return [coordsToPos[move[0]][move[1]] for move in legal_moves]


class Queen(Piece):
	def __init__(self, start_pos, color):
		super(Queen, self).__init__(start_pos, color)
		self.letter = 'Q'
		if self.color == 'white':
			self.unicode = '♕'
		else:
			self.unicode = '♛'

	def get_legal_moves(self, state):
		super(Queen, self).get_legal_moves(state)
		offset_fns = [self.pos_up, self.pos_down, self.pos_left, self.pos_right, 
				   self.pos_up_right, self.pos_up_left, self.pos_down_right, self.pos_down_left]
		legal_moves = []
		for offset_fn in offset_fns:
			legal_moves.extend(self.check_pos(offset_fn))
		return [coordsToPos[move[0]][move[1]] for move in legal_moves]
	

# TODO: Add Castling, 
class King(Piece):
	def __init__(self, start_pos, color):
		super(King, self).__init__(start_pos, color)
		self.letter = 'K'
		if self.color == "white":
			self.unicode = '♔'
		else:
			self.unicode = '♚'

	def king_moves(self):
		moves = []
		offsets = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
		for offset_x, offset_y in offsets:
			pos = self.pos_update(offset_x, offset_y)
			if self.checkLegalPos(*pos):
				moves.append(pos)
		return moves

	def get_legal_moves(self, state):
		super(King, self).get_legal_moves(state)
		legal_moves = self.king_moves()
		return [coordsToPos[move[0]][move[1]] for move in legal_moves]	