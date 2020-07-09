import sys

from BackgammonModel import BackgammonModel

model = BackgammonModel( \
    input_size = 198,
    hidden_size = int(sys.argv[2]),
    output_size = 1,
    trace_decay = 0,
    alpha = 0.1,
    save_interval = 1000,
    saved_model = sys.argv[1], #'./checkpoints/50/checkpoint_181000.pt',
    eval_interval = 1000
)

model.play_against_agent()