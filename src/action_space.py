import random

class ActionSpace:
    def __init__(self, actions=[]):
        self.actions = ['forward 1', 'forward 0', 'forward -1', 'left 1', 'right 1', 'moveMouse -100 0', 'moveMouse 100 0', 'attack 1', 'attack 0'] + actions
        self.n = len(actions)
    
    def get_length(self):
        return self.n

    def sample(self):
        return random.choice(self.actions)