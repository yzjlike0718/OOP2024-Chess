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
    
    @abstractmethod
    def make_move(self, row: int, col: int, curr_turn: str):
        pass
    
    
    @abstractmethod
    def allow_winner_check(self) -> bool:
        pass
    
    @abstractmethod
    def set_skip_last_turn(self, turn: str, skip: bool):
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

    def make_move(self, row, col, curr_turn):
        self.chessboard.set_chess(row, col, curr_turn)

    def allow_winner_check(self):
        return True
        
    def set_skip_last_turn(self, turn, skip):
        pass

# 具体产品（围棋）
class GoGame(Game):
    def __init__(self) -> None:
        super().__init__()
        self.rule = GoRule()
        self.chessboard: Chessboard = None
        self.black_skip_last_turn: bool = False
        self.white_skip_last_turn: bool = False
        
    def create_memento(self):
        return Memento(self.chessboard)
        
    def restore_memento(self, memento: Memento):
        self.chessboard = copy.deepcopy(memento.get_state())
    
    def get_state(self):
        return self.chessboard

    def set_state(self, state: Chessboard):
        self.chessboard = copy.deepcopy(state)
        
    def make_move(self, row, col, curr_turn):
        self.chessboard.set_chess(row, col, curr_turn)
        
    def allow_winner_check(self):
        return self.black_skip_last_turn and self.white_skip_last_turn
    
    def set_skip_last_turn(self, turn, skip):
        if turn == "BLACK":
            self.black_skip_last_turn = skip
        elif turn == "WHITE":
            self.white_skip_last_turn = skip
    