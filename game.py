from abc import ABC, abstractmethod
from game_rule import *

# 抽象产品 & 发起人角色：Game
class Game(ABC):
    @abstractmethod
    def is_game_running(self):
        pass
    
    @abstractmethod
    def start_game(self):
        pass
    
    @abstractmethod
    def exit_game(self):
        pass
    
    @abstractmethod
    def take_turn(self):
        pass
    
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
        self.game_running = False
        self.rule = GomokuRule()
        
    def is_game_running(self):
        return self.game_running
    
    def start_game(self):
        self.game_running = True
        
    def exit_game(self):
        self.game_running = False
        
    def take_turn(self):
        raise NotImplementedError
    
    def save_state(self):
        raise NotImplementedError
        
    def restore_state(self):
        raise NotImplementedError

# 具体产品（围棋）
class GoGame(Game):
    def __init__(self) -> None:
        super().__init__()
        self.game_running = False
        self.rule = GoRule()
        
    def is_game_running(self):
        return self.game_running
    
    def start_game(self):
        self.game_running = True
    
    def exit_game(self):
        self.game_running = False
        
    def take_turn(self):
        raise NotImplementedError
    
    def save_state(self):
        raise NotImplementedError
        
    def restore_state(self):
        raise NotImplementedError
    