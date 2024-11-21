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
        self.memento_list.append(memento)

    def undo(self) -> Memento:
        if len(self.memento_list) >= 3:
            self.memento_list.pop() # 上一局（对手行棋后的结果）
            self.memento_list.pop() # 上上一局（自己行棋后的结果）
            return self.memento_list.pop() # 上上一局（自己行棋前的结果），上上上一局（自己行棋后的结果）
        else:
            return None
