from Backgammon import *

class Env():
	def __init__(self, state_space = 198, action_space = 1352):
		self.state_space = state_space
		self.action_space = action_space


	def reset(self):
		self.game = Backgammon()
		return self.game.cur_player.value, self.game.observation_tensor(self.game.cur_player), self.game.get_legal_actions(), 0

	def step(self, action):
		# player, obs, legal_actions, reward, done
		return self.game.step(action)

	def step_back(self, action, player):
		return self.game.step_back(action, player)
