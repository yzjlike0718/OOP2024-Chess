from abc import ABC, abstractmethod
from game import *

# 抽象工厂
class GameFactory(ABC):
    @abstractmethod
    def createGame(self):
        pass

# 具体工厂（五子棋）
class GomokuFactory(GameFactory):
    def createGame(self):
        return GomokuGame()

# 具体工厂（围棋）
class GoFactory(GameFactory):
    def createGame(self):
        return GoGame()