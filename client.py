from game_factory import *
from game import *
import pygame
from commons import *
from UI_factory import *
from UI import *
from account_manager import *
from AI_factory import *
from player import *
import time

class Client():
    def __init__(self):
        # 游戏初始化参数
        self.game_name: str = None  # 当前选择的游戏名称（如 Gomoku 或 Go）
        self.game_over: bool = True  # 游戏是否结束的标志
        self.turn: int = 0  # 当前轮到的玩家，初始为0
        self.chess_color: list[str, str] = ["BLACK", "WHITE"]
        self.game_factory: GameFactory = None  # 游戏工厂，用于创建具体的游戏对象
        self.game: Game = None  # 当前的游戏对象
        self.caretaker: Caretaker = None  # 负责管理悔棋历史的对象
        self.UI_factory: UIFactory = None  # UI 工厂，用于创建具体游戏的 UI
        self.UI_platform: UITemplate = UITemplate()  # 当前的 UI 模板
        self.winner: str = None  # 游戏的获胜者
        self.allow_undo: bool = True  # 是否允许当前玩家悔棋
        self.players: tuple[Player, Player] = [None, None]
        self.account_manager = ProxyAccountManager(RealAccountManager())
        self.AI_factory: AIFactory = None  # AI 工厂

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
        self.game.set_chessboard(board_size)  # 设置棋盘为指定大小
        self.caretaker.save_memento(self.game.create_memento())  # 存储初始棋盘
    
    def set_game(self):
        """
        根据游戏名称创建对应的游戏对象和 UI，并初始化工厂和 Caretaker。
        """
        if self.game_name == "Gomoku":
            self.game_factory = GomokuFactory()
            self.UI_factory = GomokuUIFactory()
            self.AI_factory = GomokuAIFactory()
        elif self.game_name == "Go":
            self.game_factory = GoFactory()
            self.UI_factory = GoUIFactory()
        elif self.game_name == "Othello":
            self.game_factory = OthelloFactory()
            self.UI_factory = OthelloUIFactory()
            self.AI_factory = OthelloAIFactory()
        self.game = self.game_factory.createGame()  # 创建具体游戏对象
        self.caretaker = Caretaker()  # 初始化负责人对象
        self.UI_platform = self.UI_factory.createUI()  # 创建对应的 UI 平台
    
    def make_move(self, row: int, col: int):
        """
        执行行棋操作。
        :param row: 落子的行坐标
        :param col: 落子的列坐标
        """
        self.game.make_move(row=row, col=col, curr_turn=self.chess_color[self.turn])  # 在棋盘上落子
        self.caretaker.save_memento(self.game.create_memento())  # 保存当前状态

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
        self.turn = 1 - self.turn  # 切换玩家
        self.game.set_turn_taken(False)  # 新回合的玩家还没有落子
        self.game.reset_curr_move()  # 清除 move
        
    def check_finish(self):
        """
        检查游戏是否结束（一方胜利或者平局）。
        """
        if self.game.allow_winner_check(self.chess_color[self.turn]):
            winner_color = self.game.rule.check_win(self.game.get_chessboard())
            if winner_color:
                if self.players[0].color == winner_color:
                    self.winner = self.players[0].name
                else:
                    self.winner = self.players[1].name
                self.update_account_info()
                self.UI_platform.display_chessboard(self.game.get_chessboard(), self.chess_color[self.turn], self.players[self.turn].name, self.players[self.turn].games, self.players[self.turn].wins)
                time.sleep(1)
                self.UI_platform.show_winner(self.winner)
                self.play_game()
            elif self.game.rule.check_draw(self.game.get_chessboard()):  # 平局情况
                self.update_account_info()
                self.UI_platform.display_chessboard(self.game.get_chessboard(), self.chess_color[self.turn], self.players[self.turn].name, self.players[self.turn].games, self.players[self.turn].wins)
                time.sleep(1)
                self.UI_platform.show_winner(None)
                self.play_game()
                
    def next_turn(self, end_turn: bool=False):
        """
        玩家请求结束当前回合
        :param end_turn: 是否是玩家主动结束回合
        """
        next_turn_allowed, message = self.game.next_turn_allowed(end_turn)
        if next_turn_allowed:  # 当前玩家已经落子（或围棋玩家选择 skip）
            self.check_finish()  # 检查是否终局
            self.new_turn()  # 切换到下一轮
        else:
            self.UI_platform.pop_message(message)
            
    def init_player(self, is_first_hand: bool) -> tuple[bool, bool, str]:
        """
        玩家登录或注册。
        :param: is_first_hand 是否为先手玩家。
        :return: is_guest，is_AI，玩家名。
        """
        if is_first_hand:
            message = "Set the first player."
            color = "BLACK"
        else:
            message = "Set the second player."
            color = "WHITE"
        self.UI_platform.pop_message(message)
        is_guest, is_AI, is_registered_user, username, password, ai_level = self.UI_platform.choose_player()
        if is_guest:
            return Player(is_guest=True, is_AI=False, name="GUEST", color=color)
        if is_AI:
            return self.AI_factory.createAI(ai_level, color)
        # 用户输入 username 和 password
        if is_registered_user:
            # 已注册用户登陆
            if is_first_hand == False and username == self.players[0].name:
                # 后手不能和先手是同一玩家
                is_valid = False
                message = "The second player cannot be the same as the first."
            else:
                is_valid, message, game_history = self.account_manager.login(username, password)
        else:
            # 未登录用户注册
            is_valid, message, game_history = self.account_manager.register(username, password)
        self.UI_platform.pop_message(message)
        if not is_valid:
            return None
        if game_history is not None:
            games, wins = game_history
        return Player(is_guest=False, is_AI=False, name=username, color=color, games=games, wins=wins)
        
    def update_account_info(self):
        """
        调用平台系统更新登录玩家的战绩信息
        """
        for player in self.players:
            if player.is_AI or player.is_guest:
                continue
            player.games += 1
            if self.winner == player.name:
                player.wins += 1
            self.account_manager.update_account_info(player=player)
            
    def play_game(self, game_name: str=None, board_size: int=None):  # TODO: 考虑作为模板方法
        """
        开始游戏主循环。
        :param game_name: 游戏名称（可选）
        :param board_size: 棋盘大小（可选）
        """
        # 初始化游戏状态
        self.__init__()
        self.choose_game(game_name)  # 选择游戏
        self.set_game()  # 创建游戏和 UI
        
        # 玩家登录或注册，包括游客玩家或AI玩家
        while self.players[0] is None:
            self.players[0] = self.init_player(is_first_hand=True)
        # self.players[0].show_info()
        while self.players[1] is None:
            self.players[1] = self.init_player(is_first_hand=False)
        # self.players[1].show_info()

        self.game.set_turn_taken(False)  # 新游戏的玩家还没有落子
        self.init_board(board_size)  # 初始化棋盘
        
        while True:
            # 每轮更新 UI 显示棋盘状态
            self.UI_platform.display_chessboard(self.game.get_chessboard(), self.chess_color[self.turn], self.players[self.turn].name, self.players[self.turn].games, self.players[self.turn].wins)
            
            # 没有合法步可以走
            if not self.game.rule.has_valid_moves(self.game.chessboard, self.chess_color[self.turn]):
                self.UI_platform.pop_message("No valid moves.")
                self.game.set_skip_last_turn(self.chess_color[self.turn], True)
                self.check_finish()
                self.game.set_turn_taken(True)
                self.next_turn()
                
            if self.players[self.turn].is_AI:
                time.sleep(1)
                row, col = self.players[self.turn].calculate_move(self.game.chessboard)
                x = (col + 1) * GRID_SIZE
                y = (row + 1) * GRID_SIZE
                event = (pygame.MOUSEBUTTONDOWN, (x, y))
            else:
                event = self.UI_platform.detect_event()  # 检测 UI 操作事件
            if event is not None:
                event_type, event_val = event
                if event_type == pygame.MOUSEBUTTONDOWN:
                    # 计算点击位置对应的棋盘坐标
                    x, y = event_val
                    col = round((x - GRID_SIZE) / GRID_SIZE)
                    row = round((y - GRID_SIZE) / GRID_SIZE)
                    # print(f"turn: {self.turn}, row: {row}, col: {col}")
                    is_valid_move, message = self.game.rule.is_valid_move(row, col, self.game.get_chessboard(), self.chess_color[self.turn], self.game.get_turn_taken())
                    if is_valid_move:
                        # 如果是合法落子，保存状态并更新棋盘
                        self.make_move(row, col)
                        self.game.set_skip_last_turn(self.chess_color[self.turn], False)  # 围棋中取消跳过落子标记
                        self.next_turn()
                    elif self.UI_platform.admit_defeat(mouse_pos=event_val):
                        # 玩家认输
                        self.winner = self.players[1 - self.turn].name
                        self.UI_platform.show_winner(self.winner)
                        self.update_account_info()
                        self.play_game()
                    elif self.UI_platform.restart(mouse_pos=event_val):
                        # 重新开始游戏
                        self.play_game()
                    elif self.UI_platform.undo(mouse_pos=event_val):
                        # 玩家请求悔棋
                        message = self.undo_move()
                        self.UI_platform.pop_message(message)
                    elif self.UI_platform.store_state(mouse_pos=event_val):
                        # 玩家请求存储当前局面
                        if self.game.get_turn_taken():  # 玩家只能在自己行棋之前存储局面
                            self.UI_platform.pop_message("You can only Store State before taking move.")
                            continue
                        file_path = self.UI_platform.select_file(is_store=True)
                        message = self.game.store_state(file_path, self.turn, self.caretaker.memento_list)
                        self.UI_platform.pop_message(message)
                    elif self.UI_platform.load_state(mouse_pos=event_val):
                        # 玩家请求加载历史局面
                        if self.game.get_turn_taken():  # 玩家只能在自己行棋之前加载历史局面
                            self.UI_platform.pop_message("You can only Load State before taking move.")
                            continue
                        file_path = self.UI_platform.select_file(is_store=False)
                        is_valid, message = self.game.load_state(file_path, self.turn, playback=False)
                        self.UI_platform.pop_message(message)
                    elif self.UI_platform.playback(mouse_pos=event_val):
                        # 玩家请求回放历史局面
                        file_path = self.UI_platform.select_file(is_store=False)
                        is_valid, _ = self.game.load_state(file_path, self.turn, playback=True)
                        if not is_valid:
                            message = _
                            self.UI_platform.pop_message(message)
                        else:
                            chessboards = _
                            temp_chessboard = Chessboard(self.game.chessboard.get_size())
                            turn = 0
                            for chessboard in chessboards:
                                temp_chessboard.set_board(chessboard)
                                self.UI_platform.display_chessboard(chessboard=temp_chessboard, turn=self.chess_color[turn], player_name=self.players[turn].name, games=self.players[turn].games, wins=self.players[turn].wins)
                                turn = 1 - turn
                                time.sleep(1)
                            self.UI_platform.pop_message("Playback finished.")
                                
                    elif self.UI_platform.capture(mouse_pos=event_val):
                        # 围棋玩家请求提子
                        message = self.game.capture()
                        self.UI_platform.pop_message(message)
                    elif self.UI_platform.end_turn(mouse_pos=event_val):
                        # 只有围棋玩家有该按键
                        if self.game.get_turn_taken() == False:  # 玩家执行虚着
                            self.game.set_skip_last_turn(self.chess_color[self.turn], True)
                            self.check_finish()
                        self.next_turn(end_turn=True)
                    elif self.UI_platform.view_hints(mouse_pos=event_val):
                        self.UI_platform.pop_message(self.game.get_hints(), text_color=BLACK)
                    else:  # 没有合法落子且没有点击其它按键
                        self.UI_platform.pop_message(message)
                elif event_type == pygame.KEYDOWN:
                    if event_val == pygame.K_RETURN:
                        self.next_turn(end_turn=True)
            