from Backgammon import *

import torch
import numpy as np

from random import choice


class Env:
	def __init__(self, state_space = 198, action_space = 1352, verbose = False, max_turns = 300):
		self.state_space = state_space
		self.action_space = action_space
		self.verbose = verbose
		self.max_turns = max_turns

	def get_legal_actions(self):
		return self.game.get_legal_actions()

	def reset(self):
		self.game = Backgammon(verbose=self.verbose, max_turns = self.max_turns)
		return self.game.cur_player, self.game.observation_tensor(self.game.cur_player), 0, False

	def step(self, action):
		# player, obs, legal_actions, reward, done
		return self.game.step(action)

	def step_back(self, action):
		return self.game.step_back(action)


class Agent:
	def __init__(self, player):
		self.player = player

	def choose_best_action(self, actions):
		raise NotImplementedError

class RandomAgent(Agent):
	def __init__(self, player):
		super().__init__(player)

	def choose_best_action(self, actions):
		return choice(actions)

class HumanAgent(Agent):
	def __init__(self, player):
		super().__init__(player)

	def choose_best_action(self, actions):
		pass

class TDAgent(Agent):
	def __init__(self, player, net, env):
		super().__init__(player)
		self.net = net
		self.env = env

	def choose_best_action(self, actions):
		obs_ = []
		for a in actions:
			_, _, obs, _, _ = self.env.step(a)
			_ = self.env.step_back(a)
			obs_.append(obs)
		values = self.net(torch.FloatTensor(obs_)).detach().numpy()
		best_ind = int(values.argmax()) if self.player == self.env.game.cur_player else int(values.argmin())
		return actions[best_ind]

