from chessboard import *
import copy

# 备忘录类
class Memento:
    def __init__(self, state: Chessboard):
        self.state: Chessboard = copy.deepcopy(state)
        
    def get_state(self) -> Chessboard:
        return self.state
    
    def set_state(self, state: Chessboard):
        self.state = copy.deepcopy(state)

# 负责人角色
class Caretaker:
    def __init__(self):
        self.memento_list: list[Memento] = []

    def save_memento(self, memento: Memento):
        """保存当前棋盘状态"""
        self.memento_list.append(memento)

    def undo(self) -> Memento:
        """
        悔棋逻辑：回退两步
        1. 检查是否有足够的历史记录。
        2. 回退对手和自己的最近一步操作，返回上一个自己落子前的状态。
        """
        if len(self.memento_list) < 2:
            # 历史记录不足，无法悔棋
            return None

        # 回退两步
        self.memento_list.pop()  # 对手的最近一步
        return self.memento_list.pop()  # 自己的上一次状态
