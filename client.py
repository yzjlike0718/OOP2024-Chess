from player import *
from chessboard import *
from game_factory import *

class Client():
    def __init__(self):
        pass
    
    # 初始化玩家
    def init_player(self):
        self.player1 = Player("Player1", "X")
        self.player2 = Player("Player2", "O")
        print(f"Player initialized: {self.player1.name} ({self.player1.symbol}) vs {self.player2.name} ({self.player2.symbol})")
    
    # 让玩家选择围棋/五子棋
    def choose_game(self):
        self.game_name = input("Choose a game (Gomoku/Go): ").strip()
        while self.game_name != "Gomoku" and self.game_name != "Go":
            self.game_name = input("Invalid game! Choose a game (Gomoku/Go): ").strip()

    def set_game(self):
        if self.game_name == "Gomoku":
            self.game_factory = GomokuFactory()
        elif self.game_name == "Go":
            self.game_factory = GoFactory()
        self.game = self.game_factory.createGame()

    # 初始化棋盘
    def init_board(self):
        size = input("Enter chessboard size(min: 8, max: 19): ").strip()
        # while not self.game.rule.is_valid_size(size):
        while not Chessboard.is_valid_size(size):
            size = input("Invalid size! Enter chessboard size(min: 8, max: 19): ").strip()
        self.chessboard = Chessboard(int(size))
    
    def play_game(self): # TODO: 考虑作为模板方法
        self.init_player()
        self.choose_game()
        self.set_game()
        self.init_board()
        while True:
            if self.game.is_game_running():
                self.chessboard.display()
                self.game.take_turn()
                if self.game.is_end():
                    break
                self.game.exit_game()
            else:
                command = input("Enter command (start/exit): ").strip().lower()
                if command == "start":
                    self.game.start_game()
                elif command == "exit":
                    self.game.exit_game()
                    break
                else:
                    print("Invalid command. Please enter 'start' or 'exit'.")
        