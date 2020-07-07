import torch
import torch.nn as nn
import torch.nn.functional as F
import os

from tqdm import tqdm_notebook as tqdm

from BackgammonRLEnv import Env, RandomAgent, TDAgent, HumanAgent
from Backgammon import Player

class BackgammonModel(nn.Module):
	def __init__(self, input_size, hidden_size, output_size, trace_decay=0, alpha=0.1,
				 save_interval = 1000, save_location = './checkpoints/', saved_model = None,
				 eval_interval = 100):
		super(BackgammonModel, self).__init__()
		self.fc1 = nn.Sequential(
			nn.Linear(input_size, hidden_size),
			nn.Sigmoid()
		)
		self.fc2 = nn.Sequential(
			nn.Linear(hidden_size, output_size),
			nn.Sigmoid()
		)
		self.trace_decay = trace_decay
		self.alpha = alpha
		self.z = [torch.zeros(weights.shape, requires_grad = False) for weights in list(self.parameters())]

		self.save_interval = save_interval
		self.save_location = save_location
		self.saved_model = saved_model
		self.eval_interval = eval_interval

	def forward(self, x):
		x = self.fc1(x)
		x = self.fc2(x)
		return x
	
	def train(self, start_episode, num_episodes):
		if self.saved_model:
			self.load_state_dict(torch.load(self.saved_model))

		self.env = Env()
		agent = TDAgent(player = Player.LIGHT, net = self, env = self.env)
		cur_player = None
		wins = {Player.LIGHT: 0, Player.DARK: 0, Player.EMPTY: 0}
		score = 0
		tot_turns = 0

		for episode in tqdm(range(start_episode, start_episode + num_episodes + 1)):
			cur_player, obs, reward, done = self.env.reset()
			
			while not done:
				p_t = self(torch.FloatTensor(obs))
				legal_actions = self.env.get_legal_actions()
				a = agent.choose_best_action(legal_actions)
				cur_player, winner, obs, reward, done = self.env.step(a)
				p_t1 = self(torch.FloatTensor(obs))

				if not done:
					loss = self.update_weights(p_t, p_t1)
			if winner == agent.player:
				reward = 1
			else:
				reward = 0
			loss = self.update_weights(p_t, reward)

			wins[winner] += 1
			tot_turns += self.env.game.turn_num
			score += reward

			if episode % self.eval_interval == 0:
				eval_wins = self.evaluate(self.env, {Player.LIGHT: TDAgent(player = Player.LIGHT, net = self, env = self.env),
										 	    Player.DARK: RandomAgent(player = Player.DARK)})
				print("Eval, Episode: %s, Wins: %s" % (episode, str(eval_wins)))
			if episode % self.save_interval == 0:
				torch.save(self.state_dict(), os.path.join(self.save_location, 'checkpoint_%s.pt' % episode))
		
		print("Wins: ", wins)
		print("Total Reward: ", score)
		print("Average Turns: ", tot_turns // num_episodes)

	def evaluate(self, env, agents, num_episodes = 100):
		if self.saved_model:
			self.load_state_dict(torch.load(self.saved_model))
			print("loading saved model: %s" % self.saved_model)

		wins = {Player.LIGHT: 0, Player.DARK: 0, Player.EMPTY: 0}
		cur_player = None

		for episode in tqdm(range(0, num_episodes)):
			cur_player, obs, reward, done = env.reset()
			
			while not done:
				agent = agents[cur_player]
				legal_actions = env.get_legal_actions()
				a = agent.choose_best_action(legal_actions)
				cur_player, winner, obs, reward, done = env.step(a)
							
			wins[winner] += 1
		return wins

	def update_weights(self, p_t, p_t1):
		self.zero_grad()
		
		p_t.backward()
		
		with torch.no_grad():
			TD_error = p_t1 - p_t
			for i, weights in enumerate(self.parameters()):
				self.z[i] = self.trace_decay * self.z[i] + weights.grad
				w_new = weights + self.alpha*TD_error*self.z[i]
				weights.copy_(w_new)
		return TD_error

	'''
		Train Agent:
		Initialize S (state)
		z = 0
		for step in episode:
			A ~ pi(.|S) # choose_best_action
			z_t = lambda*z_{t-1} + \grad{P_t}
			TD-error (delta) = P_{t+1} - P_t # on terminal transition P_{t+1} == R_{t+1}
			w_{t+1} = w_t + \alpha*\delta*z_t
			S = S'
		until S' is terminal
	'''


	def play_against_agent(self):
		if self.saved_model:
			self.load_state_dict(torch.load(self.saved_model))
			print("loading saved model: %s" % self.saved_model)
		env = Env(verbose=True, max_turns = 100000)
		agents = {	
			Player.LIGHT: HumanAgent(Player.LIGHT, env = env),
			Player.DARK:  TDAgent(Player.DARK, net = self, env = env)
			}
		cur_player, obs, reward, done = env.reset()
	
		while not done:
			agent = agents[cur_player]
			legal_actions = env.get_legal_actions()
			print(env.game_repr())
			a = agent.choose_best_action(legal_actions)
			cur_player, winner, obs, reward, done = env.step(a)
		
		print(env.game_repr())
		print("Game Over: Winner is %s!" % winner)