from abc import ABC, abstractmethod
from UI import *


# 抽象工厂
class UIFactory(ABC):
    
    @abstractmethod
    def createUI(self):
        pass

# 具体工厂（五子棋 UI）
class GomokuUIFactory(UIFactory):
    def createUI(self):
        return GomokuUI()

# 具体工厂（围棋 UI）
class GoUIFactory(UIFactory):
    def createUI(self):
        return GoUI()
    