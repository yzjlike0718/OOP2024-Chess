from chessboard import *
import copy

# 备忘录类，用于存储棋盘状态的快照
class Memento:
    def __init__(self, state: Chessboard):
        """
        初始化备忘录，保存当前棋盘的状态。
        :param state: 当前的棋盘状态（Chessboard 对象）
        """
        self.state: Chessboard = copy.deepcopy(state)  # 深拷贝棋盘状态
        
    def get_chessboard(self) -> Chessboard:
        """
        获取备忘录中存储的棋盘状态。
        :return: 保存的棋盘状态（Chessboard 对象）
        """
        return self.state
    
    def set_chessboard(self, state: Chessboard):
        """
        更新备忘录中存储的棋盘状态。
        :param state: 新的棋盘状态（Chessboard 对象）
        """
        self.state = copy.deepcopy(state)  # 深拷贝新状态

# 负责人角色，负责管理棋盘状态的历史记录并提供悔棋功能
class Caretaker:
    def __init__(self):
        """
        初始化负责人，维护一个备忘录列表来记录棋盘的历史状态。
        """
        self.memento_list: list[Memento] = []  # 用于存储棋盘状态的备忘录列表

    def save_memento(self, memento: Memento):
        """
        保存当前棋盘状态到历史记录。
        :param memento: 当前棋盘的备忘录对象
        """
        self.memento_list.append(memento)  # 将备忘录添加到列表末尾

    def undo(self) -> Memento:
        """
        悔棋逻辑：回退两步以恢复到自己上一次落子前的状态。
        :return: 回退后的棋盘状态备忘录（Memento 对象），如果记录不足则返回 None。
        """
        # 检查是否有足够的历史记录
        if len(self.memento_list) < 2:
            # 如果记录不足两步，无法执行悔棋
            return None

        # 依次回退两步
        self.memento_list.pop()  # 移除对手的最近一步棋
        return self.memento_list.pop()  # 移除自己的最近一步棋，返回其之前的状态
