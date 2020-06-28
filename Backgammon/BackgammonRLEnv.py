from Backgammon import Backgammon

class Env():
	def __init__(self, state_space = 198, action_space = 1352):
		self.state_space = state_space
		self.action_space = action_space


	def reset(self):
		self.game = Backgammon()
		self.game.set_start_player()

	def step(self, action):
		pass
