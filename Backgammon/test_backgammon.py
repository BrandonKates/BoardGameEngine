from Backgammon import *

def test_die_roll():
	assert Backgammon(verbose=False).roll_die() in [1,2,3,4,5,6]

def test_opposite_color():
	assert Color.LIGHT.opponent() == Color.DARK and \
	Color.DARK.opponent() == Color.LIGHT