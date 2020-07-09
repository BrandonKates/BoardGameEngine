import os
import argparse

from BackgammonModel import BackgammonModel


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description='Train TD-Gammon Model')

	parser.add_argument('--start_episode', '-s', type=int, default=1)
	parser.add_argument('--episodes', '-e', type=int, default=100000)
	parser.add_argument('--load_model', '-l', type=str, default=None)
	parser.add_argument('--hidden', type=int)
	args = parser.parse_args()

	model = BackgammonModel( \
		input_size = 198,
		hidden_size = args.hidden,
		output_size = 1,
		trace_decay = 0,
		alpha = 0.1,
		save_interval = 1000,
		saved_model = args.load_model,
		eval_interval = 1000
	)

	model.train(args.start_episode, args.episodes)