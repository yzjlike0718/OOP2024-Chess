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
                    cls._instance.board = [[' ' for _ in range(size)] for _ in range(size)]
        return cls._instance
    
    def is_valid_size(size_str):
        if not size_str.isdigit():
            return False
        size = int(size_str)
        return 8 <= size <= 19

    def display(self):
        print("Current board:")
        horizontal_line = ''.join(['--' for i in range(self._instance.size)]) + '-'
        print(horizontal_line)
        for row in self.board:
            print('|' + '|'.join(row + [' ']))
            print(horizontal_line)
