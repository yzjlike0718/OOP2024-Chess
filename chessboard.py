# 棋盘类
class Chessboard:
    def __init__(self, size: int) -> None:
        """
        初始化棋盘
        :param size: 棋盘的尺寸（大小为 size x size）
        """
        self.size: int = size # 棋盘的大小
        # 创建一个 size x size 的二维数组，初始值为 None，表示没有棋子
        self.board: list[str] = [[None for _ in range(size)] for _ in range(size)]
    
    def get_size(self) -> int:
        """
        获取棋盘的当前大小
        :return: 棋盘的尺寸
        """
        return self.size
        
    def set_size(self, size):
        """
        设置棋盘大小并重新初始化棋盘
        :param size: 新的棋盘尺寸
        """
        self.size = size # 更新棋盘大小
        # 根据新的尺寸创建一个空棋盘
        self.board = [[None for _ in range(size)] for _ in range(size)]

    def set_chess(self, row, col, chess_type):
        """
        在指定位置放置棋子
        :param row: 行坐标
        :param col: 列坐标
        :param chess_type: 棋子的类型（如 "BLACK" 或 "WHITE"）
        """
        self.board[row][col] = chess_type
        
    def get_chess(self, row, col) -> str:
        """
        获取指定位置的棋子类型
        :param row: 行坐标
        :param col: 列坐标
        :return: 棋子的类型（如 "BLACK"、"WHITE" 或 None）
        """
        return self.board[row][col]
