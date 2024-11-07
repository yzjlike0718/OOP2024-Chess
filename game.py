from abc import ABC, abstractmethod
from game_rule import *

# 抽象产品：Game
class Game(ABC):
    @abstractmethod
    def play(self):
        pass

# 具体产品（五子棋）
class GomokuGame(Game):
    def __init__(self) -> None:
        super().__init__()
        self.rule = GomokuRule()
        
    def play(self):
        print("Playing Gomoku Game")
        raise NotImplementedError

# 具体产品（围棋）
class GoGame(Game):
    def __init__(self) -> None:
        super().__init__()
        self.rule = GoRule()
        
    def play(self):
        print("Playing Go Game")
        raise NotImplementedError