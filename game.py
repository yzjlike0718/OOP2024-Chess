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
        self.states_stored: list[str] = []  # 当前游戏存储的历史局面
        self.curr_move: tuple[int, int] = None
        self.hints: str = None  # 游戏规则，指导玩家下棋
    
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
    
    def make_move(self, row: int, col: int, curr_turn: str):
        """
        执行玩家的落子操作。
        :param row: 落子行坐标
        :param col: 落子列坐标
        :param curr_turn: 当前玩家的颜色（"BLACK" 或 "WHITE"）
        """
        self.chessboard.set_chess(row, col, curr_turn)
        self.set_turn_taken(True)
        self.curr_move = (row, col)
        
    def reset_curr_move(self):
        self.curr_move = None
        
    @abstractmethod
    def capture(self):
        """
        执行玩家的提子操作。
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
    
    def set_turn_taken(self, taken):
        """
        设置当前回合的玩家是否已经落子。
        :param taken: 是否行棋（布尔值）
        """
        self.turn_taken = taken
        if taken == False:
            self.curr_move = None
        
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
            
        file_dir = os.path.dirname(file_path)  # 提取目录部分
        try:
            os.makedirs(file_dir, exist_ok=True)
        except Exception as e:
            error_message = f"Failed to create directory '{file_dir}': {str(e)}"
            return error_message
        
        state = {"curr_turn": curr_turn,
                 "chessboard": self.chessboard.board}
        with open(file_path, 'w') as f:
            json.dump(state, f)
            
        self.states_stored.append(file_path)
        
        return f"Successfully stored current state to {file_path}."
    
    def load_state(self, file_path: str, curr_turn: str) -> str:
        """
        从指定文件加载历史局面和历史局面对应的下一个行棋方。
        :param file_dir: 指定文件。
        :param curr_turn: 当前回合的玩家。
        :ruturn 成功/不成功
        """
        try:
            with open(file_path, 'r') as f:
                state = json.load(f)
        except Exception as e:
            error_message = f"Failed to load '{file_path}': {str(e)}"
            return error_message
        
        if file_path not in self.states_stored:
            return f"File {file_path} isn't a valid state for current game."
        
        if curr_turn == state["curr_turn"]:
            self.chessboard.set_board(state["chessboard"])
            return f"Successfully loaded history state from {file_path}."
        else:
            return "Player of the state to be loaded dosen't match current state."
        
    @abstractmethod
    def next_turn_allowed(self, end_turn: bool=False) -> tuple[bool, str]:
        """
        是否可以进行下一轮。
        :param end_turn: 是否是玩家主动结束回合
        """
        pass
    
    def get_hints(self) -> str:
        """
        获得当前游戏的提示。
        """
        return self.hints

# 具体产品（五子棋）
class GomokuGame(Game):
    def __init__(self) -> None:
        """
        初始化五子棋游戏。
        """
        super().__init__()
        self.rule = GomokuRule()  # 五子棋规则
        self.chessboard: Chessboard = None  # 棋盘对象
        
        # 游戏规则，指导玩家下棋
        self.hints = (
            "Gomoku Rules: Players alternate placing stones; Black starts. Form a row of 5 stones to win. Stones must stay within the board. "
            "Buttons: Admit Defeat, Restart, Undo, Store State, Load State."
        )
  
    def capture(self):
        pass

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
    
    def next_turn_allowed(self, end_turn=False):
        """
        是否可以进行下一轮。
        """
        if self.turn_taken:
            return True, None
        else:
            return False, "Set chess first."
    
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
        
        # 游戏规则，指导玩家下棋
        self.hints = (
            "Go Rules: Players alternate placing stones; Black starts. Control territory by surrounding empty spaces and capturing opponent's stones. "
            "Stones with no liberties are captured. The game ends when both players skip or no moves are possible. Scoring: Black gives White 3.25 points (komi). "
            "Buttons: Admit Defeat, Restart, Undo, Store State, Load State, Capture, End Turn (or press ENTER)."
        )

    def capture(self):
        """
        执行玩家的提子操作。
        """
        if self.curr_move is not None:
            curr_capture = self.rule.get_curr_capture(self.curr_move[0], self.curr_move[1], self.chessboard)  # 获取可以提的子
            if curr_capture == []:
                return "No chess to capture."
            self.rule.capture(curr_capture, self.chessboard)  # 执行提子操作
            return "Succesfully captured."
        else:
            return "Please set chess first."
        
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
        
    def next_turn_allowed(self, end_turn=False):
        """
        是否可以进行下一轮。
        """
        if not self.turn_taken:  # skip case（虚着）
            return True, None
        
        curr_capture = self.rule.get_curr_capture(self.curr_move[0], self.curr_move[1], self.chessboard)  # 获取可以提的子
        if curr_capture != []:
            return False, "Capture first." if end_turn else None
        else:
            return True, None
