from abc import ABC, abstractmethod
from chessboard import Chessboard

# 策略接口
class GameRule(ABC):
    @abstractmethod
    def is_valid_move(self, row: int, col: int, board: Chessboard):
        pass
    
    @abstractmethod
    def is_within_board(self, row: int, col: int, board: Chessboard):
        pass

    @abstractmethod
    def check_win(self, board: Chessboard):
        pass
    
    # TODO: more rules

# 具体策略类：五子棋规则
class GomokuRule(GameRule):
    def is_valid_move(self, row, col, board):
        return self.is_within_board(row, col, board) and board.get_chess(row=row, col=col) is None

    def is_within_board(self, row, col, board):
        return 0 <= row < board.get_size() and 0 <= col < board.get_size()

    def check_win(self, board):
        def check_direction(row, col, d_row, d_col):
            color = board.get_chess(row, col)
            count = 1
            for i in range(1, 5):
                curr_row, curr_col = row + i * d_row, col + i * d_col
                if self.is_within_board(curr_row, curr_col, board) and board.get_chess(curr_row, curr_col) == color:
                    count += 1
                else:
                    break
            for i in range(1, 5):
                curr_row, curr_col = row - i * d_row, col - i * d_col
                if self.is_within_board(curr_row, curr_col, board) and board.get_chess(curr_row, curr_col) == color:
                    count += 1
                else:
                    break
            return count >= 5

        for row in range(board.get_size()):
            for col in range(board.get_size()):
                if board.get_chess(row, col) is None:
                    continue
                if (check_direction(row, col, 0, 1) or  # 横排
                    check_direction(row, col, 1, 0) or  # 纵排
                    check_direction(row, col, 1, 1) or  # 对角线
                    check_direction(row, col, 1, -1)):  # 反对角线
                    return board.get_chess(row, col)
        return None
    
    def check_draw(self, board: Chessboard):
        return all(board.get_chess(row, col) is not None for row in range(board.get_size()) for col in range(board.get_size()))


# 具体策略类：围棋规则
class GoRule(GameRule):
    def is_valid_move(self):
        raise NotImplementedError

    def check_win(self):
        raise NotImplementedError