import torch.nn as nn
import torch.nn.functional as F


class BackgammonModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(BackgammonModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return x
    
    # action is either random or max probability estimated by Qnet
    def sample_action(self, obs, epsilon): 
        coin = random.random()
        if coin < epsilon:
            return random.randint(0, self.n_actions-1)
        else:
            return self.forward(obs).argmax().item() # don't need if random action