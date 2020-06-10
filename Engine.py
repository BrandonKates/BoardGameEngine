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
def pieceAtPos(self, board, pos):
	if board[pos] == 


class Engine:
	def __init__(self):
		self.turn = 0
		self.player = 'white'
		self.board = ChessBoard()
	
	def updatePlayer(self, turn):
		return 'white' if turn % 2 == 0 else 'black'

class ChessBoard:
	def __init__(self):
		self.board = None

class Piece():
	def __init__(self, start_pos, color):
		self.pos = start_pos
		self.color = color # 'white' or 'black'
		#self.legal_moves = self.get_legal_moves()
	

	def get_legal_moves(self, state):
		return None

	def checkLegalPos(self, pos):
		if pos > 63 or pos < 0:
			return False
		else:
			return True

	def computeRow(self, pos):
		return pos // 8
	# relative upward position for white and black side
	def pos_up(self, spaces=1):
		pos = None
		if self.color == 'white':
			pos = self.pos - (8 * spaces)
		elif self.color == 'black':
			pos = self.pos + (8 * spaces)
		return pos if self.checkLegalPos(pos) else -1

	def pos_down(self, spaces=1):
		pos = None
		if self.color == 'black':
			pos = self.pos - (8 * spaces)
		elif self.color == 'white':
			pos = self.pos + (8 * spaces)
		return pos if self.checkLegalPos(pos) else -1

	def pos_left(self, spaces=1):
		# need to check if we go off the board left or right
		row = self.computeRow(self.pos)
		if self.color == 'white':
			pos = self.pos - (1 * spaces)
		elif self.color == 'black':
			pos = self.pos + (1 * spaces)
		if row == self.computeRow(pos) and self.checkLegalPos(pos):
			return pos
		return -1

	def pos_right(self, spaces=1):
		# need to check if we go off the board left or right
		row = self.computeRow(self.pos)
		if self.color == 'black':
			pos = self.pos - (1 * spaces)
		elif self.color == 'white':
			pos = self.pos + (1 * spaces)
		if row == self.computeRow(pos) and self.checkLegalPos(pos):
			return pos
		return -1

	# diagonal move up and to the left
	def pos_up_left(self, spaces=1):
		# need to check if we go off the board left or right
		row = self.computeRow(self.pos)
		if self.color == 'white':
			pos = self.pos - (9 * spaces)
		elif self.color == 'black':
			pos = self.pos + (9 * spaces)
		if abs(row - self.computeRow(pos)) == spaces and self.checkLegalPos(pos):
			return pos
		return -1	
	#
	def pos_up_right(self, spaces=1):
		# need to check if we go off the board left or right
		row = self.computeRow(self.pos)
		if self.color == 'white':
			pos = self.pos - (7 * spaces)
		elif self.color == 'black':
			pos = self.pos + (7 * spaces)
		if abs(row - self.computeRow(pos)) == spaces and self.checkLegalPos(pos):
			return pos
		return -1
	#
	def pos_down_left(self, spaces=1):
		row = self.computeRow(self.pos)
		if self.color == 'black':
			pos = self.pos - (7 * spaces)
		elif self.color == 'white':
			pos = self.pos + (7 * spaces)
		if abs(row - self.computeRow(pos)) == spaces and self.checkLegalPos(pos):
			return pos
		return -1
	#
	def pos_down_right(self, spaces=1):
		row = self.computeRow(self.pos)
		if self.color == 'white':
			pos = self.pos - (9 * spaces)
		elif self.color == 'black':
			pos = self.pos + (9 * spaces)
		if abs(row - self.computeRow(pos)) == spaces and self.checkLegalPos(pos):
			return pos
		return -1

class Pawn(Piece):
	# Pawn can move ahead 1 or 2 squares or capture piece or en passant
	def __init__(self, start_pos, color):
		super(Pawn, self).__init__(start_pos, color)

	def get_legal_moves(self, state):
		board = state.board
		turn = state.turn

		if self.color == 'white':
			return

class Rook(Piece):
	# rook moves forward as many squares until it captures or reaches end of row 
	def __init__(self, start_pos, color):
		super(Rook, self).__init__(start_pos, color)

	def check_pos(self, pos_fn):
		legal_moves = []
		spaces = 1
		while True:
			next_pos = pos_fn(spaces)
			if next_pos == -1:
				break
			else:
				legal_moves.append(next_pos)
				spaces += 1
		return legal_moves
	def get_legal_moves(self, state):
		legal_moves = []
		legal_moves.extend(self.check_pos(self.pos_up))
		legal_moves.extend(self.check_pos(self.pos_down))
		legal_moves.extend(self.check_pos(self.pos_left))
		legal_moves.extend(self.check_pos(self.pos_right))
		return legal_moves

class Knight(Piece):
	pass
class Bishop(Piece):
	pass
class Queen(Piece):
	pass
class King(Piece):
	pass