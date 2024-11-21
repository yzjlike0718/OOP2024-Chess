# 棋盘类
class Chessboard:
    def __init__(self, size) -> None:
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]
    
    def get_size(self):
        return self.size
        
    def set_size(self, size):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]

    def set_chess(self, row, col, chess_type):
        self.board[row][col] = chess_type
        
    def get_chess(self, row, col):
        return self.board[row][col]
