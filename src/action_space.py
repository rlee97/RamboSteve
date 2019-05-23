import random

class ActionSpace:
    def __init__(self, actions=[]):
        self.actions = ['forward 1', 'back 1', 'left 1', 'right 1'] + actions
        self.n = len(actions)
    
    def sample(self):
        return random.choice(self.actions)