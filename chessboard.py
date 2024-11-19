import threading

# 棋盘类（单例模式）
class Chessboard:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, size):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Chessboard, cls).__new__(cls)
                    cls._instance.size = size
                    cls._instance.board = [[None for _ in range(size)] for _ in range(size)]
        else:
            raise ValueError("Chessboard instance already created.")
        return cls._instance

    @staticmethod
    def get_instance():
        if Chessboard._instance is None:
            raise Exception("Chessboard has not been initialized yet.")
        return Chessboard._instance
    
    def get_size(self):
        return self.size
        
    def set_size(self, size):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]

    def set_chess(self, row, col, chess_type):
        self.board[row][col] = chess_type
        
    def get_chess(self, row, col):
        return self.board[row][col]
