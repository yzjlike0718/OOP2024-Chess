from abc import ABC, abstractmethod
from AI import *

# 抽象工厂
class AIFactory(ABC):
    """
    抽象工厂类，定义创建 AI 的接口。
    不同的具体工厂将根据游戏类型（如五子棋、黑白棋）创建对应的 AI。
    """
    @abstractmethod
    def createAI(self, level, color):
        """
        创建具体的 AI 对象。
        :param level: AI 等级
        :param color: AI 的颜色（"BLACK" 或 "WHITE"）
        :return: 具体的 AI 实例
        """
        pass

# 具体工厂（五子棋 AI）
class GomokuAIFactory(AIFactory):
    """
    五子棋 AI 工厂，负责创建五子棋的 AI。
    """
    def createAI(self, level, color):
        """
        创建五子棋的具体 AI 对象。
        :param level: AI 等级
        :param color: AI 的颜色（"BLACK" 或 "WHITE"）
        :return: 五子棋 AI 对象
        """
        name = f"GomokuAI-L{level}"
        if level == 1:
            return GomokuAILevel1(name, color)
        elif level == 2:
            return GomokuAILevel2(name, color)
        else:
            raise ValueError("Unsupported AI level for Gomoku.")

# 具体工厂（黑白棋 AI）
class OthelloAIFactory(AIFactory):
    """
    黑白棋 AI 工厂，负责创建黑白棋的 AI。
    """
    def createAI(self, level, color):
        """
        创建黑白棋的具体 AI 对象。
        :param level: AI 等级（1 表示简单，2 表示中等）
        :param color: AI 的颜色（"BLACK" 或 "WHITE"）
        :return: 黑白棋 AI 对象
        """
        name = f"OthelloAI-L{level}"
        if level == 1:
            return OthelloAILevel1(name, color)
        elif level == 2:
            return OthelloAILevel2(name, color)
        else:
            raise ValueError("Unsupported AI level for Othello.")
