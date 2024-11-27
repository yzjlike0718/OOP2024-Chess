from abc import ABC, abstractmethod
from UI import *

# 抽象工厂
class UIFactory(ABC):
    """
    抽象工厂类，定义创建用户界面 (UI) 的接口。
    不同的具体工厂将根据游戏类型（如五子棋、围棋）创建对应的 UI。
    """
    @abstractmethod
    def createUI(self):
        """
        创建具体的 UI 对象。
        :return: 具体的 UI 实例
        """
        pass

# 具体工厂（五子棋 UI）
class GomokuUIFactory(UIFactory):
    """
    五子棋 UI 工厂，负责创建五子棋的用户界面。
    """
    def createUI(self):
        """
        创建五子棋的具体 UI 对象。
        :return: GomokuUI 对象
        """
        return GomokuUI()

# 具体工厂（围棋 UI）
class GoUIFactory(UIFactory):
    """
    围棋 UI 工厂，负责创建围棋的用户界面。
    """
    def createUI(self):
        """
        创建围棋的具体 UI 对象。
        :return: GoUI 对象
        """
        return GoUI()
    