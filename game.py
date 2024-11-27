from abc import ABC, abstractmethod
from game_rule import *
from memento import *
from chessboard import *
import copy
import os
import json

# 抽象产品 & 发起人角色：Game
class Game(ABC):
    def __init__(self):
        """
        初始化游戏基类，包含棋盘和规则属性。
        """
        self.rule: GameRule = None  # 游戏规则
        self.chessboard: Chessboard = None  # 游戏棋盘
        self.turn_taken: bool = False  # 当前回合的玩家是否已经落子
    
    @abstractmethod
    def create_memento(self) -> Memento:
        """
        创建当前棋盘状态的备忘录。
        :return: 保存棋盘状态的 Memento 对象
        """
        pass
    
    @abstractmethod
    def restore_memento(self, memento: Memento):
        """
        恢复备忘录中的棋盘状态。
        :param memento: 保存棋盘状态的 Memento 对象
        """
        pass
    
    @abstractmethod
    def get_state(self) -> Chessboard:
        """
        获取当前棋盘状态。
        :return: 当前棋盘状态（Chessboard 对象）
        """
        pass
    
    @abstractmethod
    def set_state(self, state: Chessboard):
        """
        设置棋盘状态。
        :param state: 要设置的棋盘状态（Chessboard 对象）
        """
        pass
    
    @abstractmethod
    def make_move(self, row: int, col: int, curr_turn: str):
        """
        执行玩家的落子操作。
        :param row: 落子行坐标
        :param col: 落子列坐标
        :param curr_turn: 当前玩家的颜色（"BLACK" 或 "WHITE"）
        """
        pass
    
    @abstractmethod
    def allow_winner_check(self) -> bool:
        """
        判断是否允许进行胜利条件检查。
        :return: 是否允许检查（布尔值）
        """
        pass
    
    @abstractmethod
    def set_skip_last_turn(self, turn: str, skip: bool):
        """
        设置当前玩家是否跳过上一次回合。
        :param turn: 玩家颜色（"BLACK" 或 "WHITE"）
        :param skip: 是否跳过（布尔值）
        """
        pass
    
    @abstractmethod
    def set_turn_taken(self, taken: bool):
        """
        设置当前回合的玩家是否已经落子。
        :param taken: 是否行棋（布尔值）
        """
        pass
    
    @abstractmethod
    def get_turn_taken(self) -> bool:
        """
        获得当前回合的玩家是否已经落子。
        :ruturn 是否行棋（布尔值）
        """
        pass
    
    @abstractmethod
    def store_state(self, file_dir: str, curr_turn: str) -> str:
        """
        存储当前局面和当前局面对应的下一个行棋方到指定文件。
        :param file_dir: 指定文件。
        :param curr_turn: 当前回合的玩家。
        :ruturn 成功/不成功
        """
        pass

# 具体产品（五子棋）
class GomokuGame(Game):
    def __init__(self) -> None:
        """
        初始化五子棋游戏。
        """
        super().__init__()
        self.rule = GomokuRule()  # 五子棋规则
        self.chessboard: Chessboard = None  # 棋盘对象
        
    def create_memento(self):
        """
        创建当前棋盘状态的备忘录。
        :return: 保存棋盘状态的 Memento 对象
        """
        return Memento(self.chessboard)
        
    def restore_memento(self, memento: Memento):
        """
        恢复备忘录中的棋盘状态。
        :param memento: 保存棋盘状态的 Memento 对象
        """
        self.chessboard = copy.deepcopy(memento.get_state())
    
    def get_state(self):
        """
        获取当前棋盘状态。
        :return: 当前棋盘状态（Chessboard 对象）
        """
        return self.chessboard

    def set_state(self, state: Chessboard):
        """
        设置棋盘状态。
        :param state: 要设置的棋盘状态（Chessboard 对象）
        """
        self.chessboard = copy.deepcopy(state)

    def make_move(self, row, col, curr_turn):
        """
        执行玩家的落子操作。
        :param row: 落子行坐标
        :param col: 落子列坐标
        :param curr_turn: 当前玩家的颜色（"BLACK" 或 "WHITE"）
        """
        self.chessboard.set_chess(row, col, curr_turn)
        self.set_turn_taken(True)

    def allow_winner_check(self):
        """
        判断是否允许进行胜利条件检查（五子棋始终允许检查）。
        :return: 是否允许检查（布尔值）
        """
        return True
        
    def set_skip_last_turn(self, turn, skip):
        """
        设置当前玩家是否跳过上一次回合（五子棋不需要此逻辑）。
        :param turn: 玩家颜色（"BLACK" 或 "WHITE"）
        :param skip: 是否跳过（布尔值）
        """
        pass
    
    def set_turn_taken(self, taken):
        """
        设置当前回合的玩家是否已经落子。
        :param taken: 是否行棋（布尔值）
        """
        self.turn_taken = taken
        
    def get_turn_taken(self):
        """
        获得当前回合的玩家是否已经落子。
        :ruturn 是否行棋（布尔值）
        """
        return self.turn_taken
    
    def store_state(self, file_dir, curr_turn):
        """
        存储当前局面和当前局面对应的下一个行棋方到指定文件。
        :param file_dir: 指定文件。
        :param curr_turn: 当前回合的玩家。
        :ruturn 成功/不成功
        """
        base_name = os.path.splitext(file_dir)[0]
        file_path = base_name + ".json"
        if os.path.exists(file_path):
            return f"Please don't cover existing file {file_path}."
        
        if self.get_turn_taken():
            next_player_for_curr_state = "WHITE" if curr_turn == "BLACK" else "BLACK"
        else:
            next_player_for_curr_state = curr_turn
            
        file_dir = os.path.dirname(file_path)  # 提取目录部分
        try:
            os.makedirs(file_dir, exist_ok=True)
        except Exception as e:
            error_message = f"Failed to create directory '{file_dir}': {str(e)}"
            return error_message
        
        state = {"next_player_for_curr_state": next_player_for_curr_state,
                 "chessboard": self.chessboard.board}
        with open(file_path, 'w') as f:
            json.dump(state, f)
        
        return f"Successfully stored current state to {file_path}."

# 具体产品（围棋）
class GoGame(Game):
    def __init__(self) -> None:
        """
        初始化围棋游戏。
        """
        super().__init__()
        self.rule: GoRule = GoRule()  # 围棋规则
        self.chessboard: Chessboard = None  # 棋盘对象
        self.black_skip_last_turn: bool = False  # 黑棋是否跳过上一回合
        self.white_skip_last_turn: bool = False  # 白棋是否跳过上一回合
        
    def create_memento(self):
        """
        创建当前棋盘状态的备忘录。
        :return: 保存棋盘状态的 Memento 对象
        """
        return Memento(self.chessboard)
        
    def restore_memento(self, memento: Memento):
        """
        恢复备忘录中的棋盘状态。
        :param memento: 保存棋盘状态的 Memento 对象
        """
        self.chessboard = copy.deepcopy(memento.get_state())
    
    def get_state(self):
        """
        获取当前棋盘状态。
        :return: 当前棋盘状态（Chessboard 对象）
        """
        return self.chessboard

    def set_state(self, state: Chessboard):
        """
        设置棋盘状态。
        :param state: 要设置的棋盘状态（Chessboard 对象）
        """
        self.chessboard = copy.deepcopy(state)
        
    def make_move(self, row, col, curr_turn):
        """
        执行玩家的落子操作，同时处理提子逻辑。
        :param row: 落子行坐标
        :param col: 落子列坐标
        :param curr_turn: 当前玩家的颜色（"BLACK" 或 "WHITE"）
        """
        self.chessboard.set_chess(row, col, curr_turn)
        curr_capture = self.rule.get_curr_capture(row, col, self.chessboard)  # 获取可以提的子
        self.rule.capture(curr_capture, self.chessboard)  # 执行提子操作
        self.set_turn_taken(True)
        
    def allow_winner_check(self):
        """
        判断是否允许进行胜利条件检查（围棋需要双方连续跳过回合）。
        :return: 是否允许检查（布尔值）
        """
        return self.black_skip_last_turn and self.white_skip_last_turn
    
    def set_skip_last_turn(self, turn, skip):
        """
        设置当前玩家是否跳过上一次回合。
        :param turn: 玩家颜色（"BLACK" 或 "WHITE"）
        :param skip: 是否跳过（布尔值）
        """
        if turn == "BLACK":
            self.black_skip_last_turn = skip
        elif turn == "WHITE":
            self.white_skip_last_turn = skip

    def set_turn_taken(self, taken):
        """
        设置当前回合的玩家是否已经落子。
        :param taken: 是否行棋（布尔值）
        """
        self.turn_taken = taken
        
    def get_turn_taken(self):
        """
        获得当前回合的玩家是否已经落子。
        :ruturn 是否行棋（布尔值）
        """
        return self.turn_taken
    
    def store_state(self, file_dir, curr_turn):
        """
        存储当前局面和当前局面对应的下一个行棋方到指定文件。
        :param file_dir: 指定文件。
        :param curr_turn: 当前回合的玩家。
        :ruturn 成功/不成功
        """
        base_name = os.path.splitext(file_dir)[0]
        file_dir = base_name + ".json"
        if os.path.exists(file_dir):
            return f"Please don't cover existing file {file_dir}."
        if self.get_turn_taken():
            next_player_for_curr_state = "WHITE" if curr_turn == "BLACK" else "BLACK"
        else:
            next_player_for_curr_state = curr_turn
        try:
            os.makedirs(file_dir)
        except Exception as e:
            error_message = f"Failed to create directory '{file_dir}': {str(e)}"
            return error_message
        
        state = {"next_player_for_curr_state": next_player_for_curr_state,
                 "chessboard": self.chessboard.board}
        with open(file_dir, 'w') as f:
                json.dump(state, f)
