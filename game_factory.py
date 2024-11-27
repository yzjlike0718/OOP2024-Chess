from abc import ABC, abstractmethod
from game import *

# 抽象工厂类，用于定义游戏工厂的接口
class GameFactory(ABC):
    @abstractmethod
    def createGame(self):
        """
        抽象方法，创建具体游戏对象。
        每个具体工厂需实现此方法以返回对应的游戏实例。
        """
        pass

# 具体工厂类（五子棋），负责创建五子棋游戏实例
class GomokuFactory(GameFactory):
    def createGame(self):
        """
        创建并返回五子棋游戏实例。
        :return: GomokuGame 对象
        """
        return GomokuGame()

# 具体工厂类（围棋），负责创建围棋游戏实例
class GoFactory(GameFactory):
    def createGame(self):
        """
        创建并返回围棋游戏实例。
        :return: GoGame 对象
        """
        return GoGame()
