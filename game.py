from abc import ABC, abstractmethod

# 抽象产品：Game
class Game(ABC):
    @abstractmethod
    def play(self):
        pass

# 具体产品（五子棋）
class GomokuGame(Game):
    def play(self):
        print("Playing Gomoku Game")
        raise NotImplementedError

# 具体产品（围棋）
class GoGame(Game):
    def play(self):
        print("Playing Go Game")
        raise NotImplementedError