from abc import ABCMeta, abstractmethod
class Agent():
    __metaclass__=ABCMeta
    
    def __init__(self):
        pass

    @abstractmethod
    def select_move(self, gamestate):
        pass