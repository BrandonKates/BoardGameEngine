import time
from Backgammon import Backgammon

t= time.time()
for i in range(100):
    _,_ = Backgammon(verbose = False).play_game()
end = time.time() - t
print("Time: ", end)