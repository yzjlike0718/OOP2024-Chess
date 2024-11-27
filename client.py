from chessboard import *
from game_factory import *
from game import *
import pygame
from commons import *
from UI_factory import *
from UI import *

class Client():
    def __init__(self):
        # 游戏初始化参数
        self.game_name: str = None  # 当前选择的游戏名称（如 Gomoku 或 Go）
        self.game_over: bool = True  # 游戏是否结束的标志
        self.turn: str = "BLACK"  # 当前轮到的玩家，初始为黑棋
        self.game_factory: GameFactory = None  # 游戏工厂，用于创建具体的游戏对象
        self.game: Game = None  # 当前的游戏对象
        self.caretaker: Caretaker = None  # 负责管理悔棋历史的对象
        self.UI_factory: UIFactory = None  # UI 工厂，用于创建具体游戏的 UI
        self.UI_platform: UITemplate = UITemplate()  # 当前的 UI 模板
        self.winner: str = None  # 游戏的获胜者
        self.allow_undo: bool = True  # 是否允许当前玩家悔棋

    def choose_game(self, game_name: str=None):
        """
        选择游戏名称。
        :param game_name: 指定的游戏名称（如果为 None，则通过 UI 选择）
        """
        if game_name is None:
            game_name = self.UI_platform.choose_game()
        self.game_name = game_name

    def init_board(self, board_size: int=None):
        """
        初始化棋盘大小。
        :param board_size: 指定的棋盘大小（如果为 None，则通过 UI 选择）
        """
        if board_size is None:
            board_size = self.UI_platform.choose_board_size()
        self.game.set_state(Chessboard(board_size))  # 设置棋盘为指定大小
    
    def set_game(self):
        """
        根据游戏名称创建对应的游戏对象和 UI，并初始化工厂和 Caretaker。
        """
        if self.game_name == "Gomoku":
            self.game_factory = GomokuFactory()
            self.UI_factory = GomokuUIFactory()
        elif self.game_name == "Go":
            self.game_factory = GoFactory()
            self.UI_factory = GoUIFactory()
        self.game = self.game_factory.createGame()  # 创建具体游戏对象
        self.caretaker = Caretaker()  # 初始化负责人对象
        self.UI_platform = self.UI_factory.createUI()  # 创建对应的 UI 平台
    
    def make_move(self, row: int, col: int):
        """
        执行行棋操作。
        :param row: 落子的行坐标
        :param col: 落子的列坐标
        """
        self.caretaker.save_memento(self.game.create_memento())  # 保存当前状态
        self.game.make_move(row=row, col=col, curr_turn=self.turn)  # 在棋盘上落子

    def undo_move(self) -> str:
        """
        执行悔棋操作，回到上一个状态。
        """
        if not self.allow_undo:
            return "Undo not allowed."
        memento = self.caretaker.undo()  # 获取上一个状态
        if memento is None:
            return "Undo not allowed."
        else:
            self.game.restore_memento(memento)  # 恢复到上一个状态
        self.allow_undo = False  # 每轮仅允许悔棋一次
        return "Undo successfully."

    def new_turn(self):
        """
        切换到下一轮玩家。
        """
        self.allow_undo = True  # 允许悔棋
        self.turn = "WHITE" if self.turn == "BLACK" else "BLACK"  # 切换玩家
        self.game.set_turn_taken(False)  # 新回合的玩家还没有落子
        self.game.reset_curr_move()  # 清除 move
        
    def check_finish(self):
        """
        检查游戏是否结束（一方胜利或者平局）。
        """
        if self.game.allow_winner_check():
            self.winner = self.game.rule.check_win(self.game.get_state())
            if self.winner:
                self.UI_platform.show_winner(self.winner)
                self.play_game()
            elif self.game.rule.check_draw(self.game.get_state()):  # 平局情况
                self.UI_platform.show_winner(None)
                self.play_game()
                
    def next_turn(self):
        """
        玩家请求结束当前回合
        """
        next_turn_allowed, message = self.game.next_turn_allowed()
        if next_turn_allowed:  # 当前玩家已经落子（或围棋玩家选择 skip）
            self.check_finish()  # 检查是否终局
            self.new_turn()  # 切换到下一轮
        else:
            self.UI_platform.pop_message(message)

    def play_game(self, game_name: str=None, board_size: int=None):  # TODO: 考虑作为模板方法
        """
        开始游戏主循环。
        :param game_name: 游戏名称（可选）
        :param board_size: 棋盘大小（可选）
        """
        # 初始化游戏状态
        self.game_over = False
        self.turn = "BLACK"
        self.winner = None
        self.allow_undo = True
        self.choose_game(game_name)  # 选择游戏
        self.set_game()  # 创建游戏和 UI
        self.game.set_turn_taken(False)  # 新游戏的玩家还没有落子
        self.init_board(board_size)  # 初始化棋盘
        
        while True:
            event = self.UI_platform.detect_event()  # 检测 UI 操作事件
            if event is not None:
                event_type, event_val = event
                if event_type == pygame.MOUSEBUTTONDOWN:
                    # 计算点击位置对应的棋盘坐标
                    x, y = event_val
                    col = round((x - GRID_SIZE) / GRID_SIZE)
                    row = round((y - GRID_SIZE) / GRID_SIZE)
                    if self.game.rule.is_valid_move(row, col, self.game.get_state(), self.turn, self.game.get_turn_taken()):
                        # 如果是合法落子，保存状态并更新棋盘
                        self.caretaker.save_memento(self.game.create_memento())
                        self.game.make_move(row=row, col=col, curr_turn=self.turn)
                        self.game.set_skip_last_turn(self.turn, False)  # 围棋中取消跳过落子标记
                    elif self.UI_platform.admit_defeat(mouse_pos=event_val):
                        # 玩家认输
                        self.winner = "WHITE" if self.turn == "BLACK" else "BLACK"
                        self.UI_platform.show_winner(self.winner)
                        self.play_game()
                    elif self.UI_platform.restart(mouse_pos=event_val):
                        # 重新开始游戏
                        self.play_game()
                    elif self.UI_platform.undo(mouse_pos=event_val):
                        # 玩家请求悔棋
                        message = self.undo_move()
                        self.UI_platform.pop_message(message)
                    elif self.UI_platform.skip(mouse_pos=event_val):
                        # 围棋玩家选择跳过落子
                        self.game.set_skip_last_turn(self.turn, True)
                        self.game.set_turn_taken(True)
                        if self.game.allow_winner_check():  # 检查是否满足胜利条件
                            self.winner = self.game.rule.check_win(self.game.get_state())
                            assert self.winner is not None
                            self.UI_platform.show_winner(self.winner)
                            self.play_game()
                        self.next_turn()
                    elif self.UI_platform.store_state(mouse_pos=event_val):
                        # 玩家请求存储当前局面
                        file_dir = self.UI_platform.select_file(is_store=True)
                        message = self.game.store_state(file_dir, self.turn)
                        self.UI_platform.pop_message(message)
                    elif self.UI_platform.load_state(mouse_pos=event_val):
                        # 玩家请求加载历史局面
                        file_dir = self.UI_platform.select_file(is_store=False)
                        message = self.game.load_state(file_dir, self.turn)
                        self.UI_platform.pop_message(message)
                    elif self.UI_platform.capture(mouse_pos=event_val):
                        # 围棋玩家请求提子
                        message = self.game.capture()
                        self.UI_platform.pop_message(message)
                    elif self.UI_platform.end_turn(mouse_pos=event_val):
                        self.next_turn()
                    elif self.UI_platform.view_hints(mouse_pos=event_val):
                        self.UI_platform.pop_message(self.game.get_hints(), text_color=BLACK)
                elif event_type == pygame.KEYDOWN:
                    if event_val == pygame.K_RETURN:
                        self.next_turn()
            # 每轮更新 UI 显示棋盘状态
            self.UI_platform.display_chessboard(self.game.get_state(), self.turn)
            