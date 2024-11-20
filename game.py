from abc import ABC, abstractmethod
from game_rule import *

# 抽象产品 & 发起人角色：Game
class Game(ABC):
    def __init__(self):
        self.rule: GameRule = None

    @abstractmethod
    def save_state(self):
        pass
    
    @abstractmethod
    def restore_state(self):
        pass

# 具体产品（五子棋）
class GomokuGame(Game):
    def __init__(self) -> None:
        super().__init__()
        self.rule = GomokuRule()
        
    def save_state(self):
        raise NotImplementedError
        
    def restore_state(self):
        raise NotImplementedError

# 具体产品（围棋）
class GoGame(Game):
    def __init__(self) -> None:
        super().__init__()
        self.rule = GoRule()
        
    def save_state(self):
        raise NotImplementedError
        
    def restore_state(self):
        raise NotImplementedError
    