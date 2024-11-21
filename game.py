from abc import ABC, abstractmethod
from game_rule import *
from memento import *
from chessboard import *
import copy

# 抽象产品 & 发起人角色：Game
class Game(ABC):
    def __init__(self):
        self.rule: GameRule = None
        self.chessboard: Chessboard = None
    
    @abstractmethod
    def create_memento(self) -> Memento:
        pass
    
    @abstractmethod
    def restore_memento(self):
        pass
    
    @abstractmethod
    def get_state(self) -> Chessboard:
        pass
    
    @abstractmethod
    def set_state(self):
        pass

# 具体产品（五子棋）
class GomokuGame(Game):
    def __init__(self) -> None:
        super().__init__()
        self.rule = GomokuRule()
        self.chessboard: Chessboard = None
        
    def create_memento(self):
        return Memento(self.chessboard)
        
    def restore_memento(self, memento: Memento):
        self.chessboard = copy.deepcopy(memento.get_state())
    
    def get_state(self):
        return self.chessboard

    def set_state(self, state: Chessboard):
        self.chessboard = copy.deepcopy(state)

# 具体产品（围棋）
class GoGame(Game):
    def __init__(self) -> None:
        super().__init__()
        self.rule = GoRule()
        self.chessboard: Chessboard = None
        
    def create_memento(self):
        return Memento(self.chessboard)
        
    def restore_memento(self, memento: Memento):
        self.chessboard = copy.deepcopy(memento.get_state())
    
    def get_state(self):
        return self.chessboard

    def set_state(self, state: Chessboard):
        self.chessboard = copy.deepcopy(state)
    