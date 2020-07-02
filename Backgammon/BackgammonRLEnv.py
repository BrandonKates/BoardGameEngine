from Backgammon import *
from BackgammonModel import BackgammonModel

import torch
import numpy as np

class Env():
	def __init__(self, state_space = 198, action_space = 1352):
		self.state_space = state_space
		self.action_space = action_space
		self.agents = [TDAgent(player = 0, net = BackgammonModel(198, 50, 1), env = self)]


	def reset(self):
		self.game = Backgammon()
		return self.game.cur_player.value, self.game.observation_tensor(self.game.cur_player), self.game.get_legal_actions(), 0

	def step(self, action):
		# player, obs, legal_actions, reward, done
		return self.game.step(action)

	def step_back(self, action):
		return self.game.step_back(action)


class TDAgent():
	def __init__(self, player, net, env):
		self.player = player
		self.net = net
		self.env = env

	def choose_best_action(self, actions):
		obs_ = []
		for a in actions:
			_, obs, _, _ = self.env.step(a)
			_ = self.env.step_back(a)
			obs_.append(obs)
		values = self.net(torch.FloatTensor(obs_)).detach().numpy()
		best_ind = int(values.argmax()) if self.player == 0 else int(values.argmin())
		return actions[best_ind]