import random
import time

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
    def __init__(self, print_board=True):
        self.board = Board()  # instantiate an empty board
        self.curr_color = Color.BLACK
        self.opp_color = Color.WHITE
        self.score = [2, 2]
        self.legal_moves = self.board.get_legal_moves(self.curr_color)
        self.game_over = False
        self.pass_turn = False
        self.print_board = print_board

    def play_game(self):
        pass

    def play_random_game(self):
        # select a random player to start the game
        player = [Color.WHITE, Color.BLACK][int(random.random() * 2)]
        if player == self.opp_color:
            self.curr_color, self.opp_color = self.opp_color, self.curr_color
            self.legal_moves = self.board.get_legal_moves(self.curr_color)

        while not self.game_over:
            # time.sleep(1)
            n = len(self.legal_moves)
            choice = int(random.random() * (n - 1))

            spot = self.select_move(choice)

            # Play a turn
            self.turn(spot)
        return self.score, self.__str__(), player

    def select_move(self, idx):
        return list(self.legal_moves.keys())[idx]

    def turn(self, spot):
        if self.print_board:
            print(self)

        if not self.pass_turn:
            # Set the chosen square to the current player's color
            self.board.set_square(*spot, self.curr_color)

            # Retrieve tiles to be flipped
            # TODO: get this from self.legal_moves instead for speedup?
            flips = self.legal_moves[spot]

            # Flip tiles
            for flip in flips:
                self.board.set_square(*flip, self.curr_color)

            num_flips = len(flips)
            self.score[self.curr_color.value] += num_flips + \
                1  # + 1 for chosen spot
            self.score[self.opp_color.value] -= num_flips

        # Swap current and opposite player
        self.curr_color, self.opp_color = self.opp_color, self.curr_color

        # Compute the legal moves for the next turn
        self.legal_moves = self.board.get_legal_moves(self.curr_color)

        # Check if game is over:
        # no legal moves for either player or out of spots (no legal moves for either player)
        if len(self.legal_moves) == 0:
            # no legal moves
            if self.pass_turn:
                if self.print_board:
                    print(self)
                    print('\nGame is over!')
                self.game_over = True
            else:
                if len(self.board.get_empty_positions()) == 0:
                    if self.print_board:
                        print(self)
                        print('\nGame is over!')
                    self.game_over = True
                else:
                    self.pass_turn = True
                    self.turn(None)  # pass turn
        else:
            self.pass_turn = False

    def to_string_debugging(self):
        return '\n'.join(str(s) for s in self.legal_moves.items()) + "\n\n\n" + str(self.board)

    def __str__(self):
        s = '\n\nWhite: {}\tBlack: {}'.format(
            *self.score) + "\n" + str(self.board)
        s += '{}: {}\n{}'.format(self.curr_color,
                                 self.legal_moves, self.pass_turn)
        return s


class Board:
    def __init__(self, rows=8, cols=8):
        self.board = [Color.EMPTY] * rows * cols
        self.board[3 * 8 + 3] = self.board[4 * 8 + 4] = Color.WHITE
        self.board[3 * 8 + 4] = self.board[4 * 8 + 3] = Color.BLACK
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

    def get_square_status(self, spot, curr_color):
        assert self.is_spot_in_board(*spot)
        # one of Color.WHITE, Color.BLACK, Color.EMPTY
        square = self.get_square(*spot)
        if square == Color.EMPTY:
            return Square.EMPTY
        if square == curr_color:
            return Square.FRIENDLY
        return Square.ENEMY

    def set_square(self, x: int, y: int, color: Color) -> None:
        self.board[x * self.rows + y] = color

    def flip_square(self, spot: Tuple[int, int]) -> None:
        current_color = Board.get_square(*spot)
        assert current_color is not Color.EMPTY
        color = None
        if current_color is Color.BLACK:
            color = Color.WHITE
        if current_color is Color.WHITE:
            color = Color.BLACK
        self.set_square(*spot, color)

    def get_flips_in_direction(self, spot, move, curr_color):
        if not self.is_spot_in_board(*spot):
            return []
        spot = Board.move(spot, move)
        flips = []

        while self.is_spot_in_board(*spot):
            status = self.get_square_status(spot, curr_color)
            if status == Square.EMPTY:
                return []
            if status == Square.ENEMY:
                flips.append(spot)
            elif status == Square.FRIENDLY:
                return flips
            spot = Board.move(spot, move)
        return []

    def get_flips(self, spot, curr_color):
        if self.get_square_status(spot, curr_color) != Square.EMPTY:
            return []

        flips = []
        for move in Board.get_move_directions():
            flips.extend(self.get_flips_in_direction(spot, move, curr_color))
        return flips

    def get_legal_moves(self, curr_color):
        spots = {}
        for spot in self.get_empty_positions():
            flips = self.get_flips(spot, curr_color)
            if len(flips) > 0:
                spots[spot] = flips
        return spots

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
    game = Othello(print_board=True)
    # print(game)
    # print(game.board.get_empty_positions())
    # print(game.board.get_white_positions())
    # print(game.board.get_black_positions())
    #scores = [game.play_random_game() for _ in range(1000000)]

    game.play_random_game()
