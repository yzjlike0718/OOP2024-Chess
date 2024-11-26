from chessboard import *
from game_factory import *
from game import *
import pygame
import sys
from commons import *
from UI_factory import *
from UI import *

class Client():
    def __init__(self):
        self.game_name: str = None
        self.game_over: bool = True
        self.turn: str = "BLACK"
        self.game_factory: GameFactory = None
        self.game: Game = None
        self.caretaker: Caretaker = None
        self.UI_factory: UIFactory = None
        self.UI_platform: UITemplate = UITemplate()
        self.winner: str = None
        self.allow_undo: bool = True
        
    def choose_game(self):
        self.game_name = self.UI_platform.choose_game()

    def init_board(self):
        self.board_size = self.UI_platform.choose_board_size()
        self.game.set_state(Chessboard(self.board_size))
        self.caretaker.save_memento(self.game.create_memento()) # 存储第一回合开始时的空棋盘
    
    def set_game(self):
        if self.game_name == "Gomoku":
            self.game_factory = GomokuFactory()
            self.UI_factory = GomokuUIFactory()
        elif self.game_name == "Go":
            self.game_factory = GoFactory()
            self.UI_factory = GoUIFactory()
        self.game = self.game_factory.createGame()
        self.caretaker = Caretaker()
        self.UI_platform = self.UI_factory.createUI()
        # print(f"self.game: {type(self.game)}, self.UI_platform: {type(self.UI_platform)}")
    
    def play_game(self): # TODO: 考虑作为模板方法
        self.game_over = False
        self.turn = "BLACK"
        self.winner = None
        self.allow_undo = True
        self.choose_game()
        self.set_game()
        self.init_board()
        while True:
            event = self.UI_platform.detect_event()
            if event is not None:
                event_type, event_val = event
                if event_type == pygame.MOUSEBUTTONDOWN:
                    x, y = event_val
                    col = round((x - GRID_SIZE) / GRID_SIZE)
                    row = round((y - GRID_SIZE) / GRID_SIZE)
                    if self.game.rule.is_valid_move(row, col, self.game.get_state(), self.turn):
                        self.game.rule.set_chess(row=row, col=col, board=self.game.get_state(), curr_turn=self.turn)
                        
                        self.game.set_skip_last_turn(self.turn, False) # 围棋：当前方选择落子
                        
                        if self.game.allow_winner_check():
                            self.winner = self.game.rule.check_win(self.game.get_state())
                            if self.winner:
                                self.UI_platform.show_winner(self.winner)
                                self.play_game()
                            elif self.game.rule.check_draw(self.game.get_state()):
                                self.UI_platform.show_winner(None)
                                self.play_game()
                                
                        # 下一轮开始前：
                        self.allow_undo = True # 允许悔棋一次
                        self.turn = "WHITE" if self.turn == "BLACK" else "BLACK" # 交换轮次
                        self.caretaker.save_memento(self.game.create_memento()) # 存储当前棋盘状态
                        
                    elif self.UI_platform.admit_defeat(mouse_pos=event_val):
                        self.winner = "WHITE" if self.turn == "BLACK" else "BLACK"
                        self.UI_platform.show_winner(self.winner)
                        self.play_game()
                    elif self.UI_platform.restart(mouse_pos=event_val):
                        self.play_game()
                    elif self.UI_platform.undo(mouse_pos=event_val):
                        if self.allow_undo:
                            new_memento: Memento = self.caretaker.undo()
                            if new_memento is None:
                                pass
                            else:
                                self.game.restore_memento(new_memento)
                            self.allow_undo = False
                    elif self.UI_platform.skip(mouse_pos=event_val):
                        # 围棋：当前方选择不落子
                        self.game.set_skip_last_turn(self.turn, True)
                        if self.game.allow_winner_check():
                            self.winner = self.game.rule.check_win(self.game.get_state())
                            assert self.winner is not None
                            self.UI_platform.show_winner(self.winner)
                            self.play_game()
                        else:
                            # 下一轮开始前：
                            self.allow_undo = True # 允许悔棋一次
                            self.turn = "WHITE" if self.turn == "BLACK" else "BLACK" # 交换轮次
                            self.caretaker.save_memento(self.game.create_memento()) # 存储当前棋盘状态
                    
            self.UI_platform.display_chessboard(self.game.get_state(), self.turn)
            