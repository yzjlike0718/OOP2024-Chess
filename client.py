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
        self.turn: str = "BALCK"
        self.game_factory: GameFactory = None
        self.game: Game = None
        self.UI_factory: UIFactory = None
        self.UI_platform: UITemplate = UITemplate()
        self.winner: str = None
        
    def choose_game(self):
        self.game_name = self.UI_platform.choose_game()

    def init_board(self):
        self.board_size = self.UI_platform.choose_board_size()
        try:
            self.chessboard = Chessboard(self.board_size)
        except:
            self.chessboard = Chessboard.get_instance()
            self.chessboard.set_size(self.board_size)
    
    def set_game(self):
        if self.game_name == "Gomoku":
            self.game_factory = GomokuFactory()
            self.UI_factory = GomokuUIFactory()
        elif self.game_name == "Go":
            self.game_factory = GoFactory()
            self.UI_factory = GoUIFactory()
        self.game = self.game_factory.createGame()
        self.UI_platform = self.UI_factory.createUI()
        # print(f"self.game: {type(self.game)}, self.UI_platform: {type(self.UI_platform)}")
    
    def play_game(self): # TODO: 考虑作为模板方法
        self.game_over = False
        self.turn = "BALCK"
        self.winner = None
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
                    if self.game.rule.is_valid_move(row, col, self.chessboard, self.turn):
                        self.chessboard.set_chess(row=row, col=col, chess_type=self.turn)

                        self.winner = self.game.rule.check_win(self.chessboard)
                        if self.winner:
                            self.UI_platform.show_winner(self.winner)
                            self.play_game()
                        elif self.game.rule.check_draw(self.chessboard):
                            self.UI_platform.show_winner(None)
                            self.play_game()
                    elif self.UI_platform.admit_defeat(mouse_pos=event_val):
                        self.winner = "WHITE" if self.turn == "BALCK" else "BALCK"
                        self.UI_platform.show_winner(self.winner)
                        self.play_game()

                    self.turn = "WHITE" if self.turn == "BALCK" else "BALCK"
            self.UI_platform.display_chessboard(self.chessboard, self.turn)
            