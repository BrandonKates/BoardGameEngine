import torch.nn as nn
import torch.nn.functional as F


class BackgammonModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(BackgammonModel, self).__init__()
        self.fc1 = nn.Sequential(
    		nn.Linear(input_size, hidden_size),
    		nn.Sigmoid()
        )
        self.fc2 = nn.Sequential(
        	nn.Linear(hidden_size, output_size),
        	nn.Sigmoid()
        )
        
    def forward(self, x):
        x = self.fc1(x)
        x = self.fc2(x)
        return x
    


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