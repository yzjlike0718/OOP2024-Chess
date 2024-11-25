from abc import ABC, abstractmethod
from chessboard import Chessboard

# 策略接口
class GameRule(ABC):
    @abstractmethod
    def is_valid_move(self, row: int, col: int, board: Chessboard, curr_turn: str):
        pass
    
    @abstractmethod
    def is_within_board(self, row: int, col: int, board: Chessboard):
        pass

    @abstractmethod
    def check_win(self, board: Chessboard):
        pass
    
    @abstractmethod
    def check_draw(self, board: Chessboard):
        pass

# 具体策略类：五子棋规则
class GomokuRule(GameRule):
    def is_valid_move(self, row, col, board, curr_turn):
        print(f"GomokuRule is_valid_move row={row}, col={col}")
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
    
    def check_draw(self, board):
        return all(board.get_chess(row, col) is not None for row in range(board.get_size()) for col in range(board.get_size()))


# 具体策略类：围棋规则
class GoRule(GameRule):
    def has_liberty(self, row: int, col: int, board: Chessboard):
        # 检查 (row, col) 位置的棋子是否有气
        assert self.is_within_board(row, col, board)
        color = board.get_chess(row, col)
        if self.is_within_board(row + 1, col, board):
            if board.get_chess(row + 1, col) == color or board.get_chess(row + 1, col) is None:
                return True
        if self.is_within_board(row - 1, col, board):
            if board.get_chess(row - 1, col) == color or board.get_chess(row - 1, col) is None:
                return True
        if self.is_within_board(row, col + 1, board):
            if board.get_chess(row, col + 1) == color or board.get_chess(row, col + 1) is None:
                return True
        if self.is_within_board(row, col - 1, board):
            if board.get_chess(row, col - 1) == color or board.get_chess(row, col - 1) is None:
                return True
        return False
     
    def get_curr_capture(self, row: int, col: int, board: Chessboard):
        # 检查当前在 (row, col) 落子后，上下左右可以提的子
                        
        assert self.is_within_board(row, col, board)
        
        curr_capture = []
        
        if self.is_within_board(row + 1, col, board) and not self.has_liberty(row + 1, col, board):
            curr_capture.append((row + 1, col))
        if self.is_within_board(row - 1, col, board) and not self.has_liberty(row - 1, col, board):
            curr_capture.append((row - 1, col))
        if self.is_within_board(row, col + 1, board) and not self.has_liberty(row, col + 1, board):
            curr_capture.append((row, col + 1))
        if self.is_within_board(row, col - 1, board) and not self.has_liberty(row, col - 1, board):
            curr_capture.append((row, col - 1))
            
        return curr_capture
     
    def capture(self, row: int, col: int, board: Chessboard):
        # 提子
        board.set_chess(row, col, None)
               
    def is_valid_move(self, row, col, board, curr_turn):
        print(f"GoRule is_valid_move row={row}, col={col}, curr_turn={curr_turn}")
        if not self.is_within_board(row, col, board):
            return False
        if board.get_chess(row=row, col=col) is not None:
            return False
    
        # 暂时落子
        board.set_chess(row, col, curr_turn)
        if not self.has_liberty(row, col, board):
            # 判断落子后是否可提子
            if self.get_curr_capture(row, col, board) != []:
                board.set_chess(row, col, None)
                return True
            else:
                board.set_chess(row, col, None)
                return False
        else:
            board.set_chess(row, col, None)
            return True
    
    def is_within_board(self, row, col, board):
        return 0 <= row < board.get_size() and 0 <= col < board.get_size()

    def check_win(self, board):
        black_points = 0
        white_points = 0
        visited = [[False for _ in range(board.get_size())] for _ in range(board.get_size())]
        
        def dfs(row, col, color):
            # 深搜：找到一方棋子连接的所有点
            stack = [(row, col)]
            territory = set()
            while stack != []:
                r, c = stack.pop()
                if not self.is_within_board(r, c, board) or visited[r][c]:
                    continue
                if board.get_chess(r, c) == color:
                    visited[r][c] = True
                    territory.add((r, c))
                    # 向四个方向扩展
                    stack.append((r + 1, c))
                    stack.append((r - 1, c))
                    stack.append((r, c + 1))
                    stack.append((r, c - 1))
            return territory
        
        # 清除无气的子
        for r in range(board.get_size()):
            for c in range(board.get_size()):
                if not self.has_liberty(r, c, board):
                    self.capture(r, c, board)

        for r in range(board.get_size()):
            for c in range(board.get_size()):
                if visited[r][c]:
                    continue
                if board.get_chess(r, c) == "BLACK":
                    # 计算黑棋占据的点
                    territory = dfs(r, c, "BLACK")
                    black_points += len(territory)
                elif board.get_chess(r, c) == "WHITE":
                    # 计算白棋占据的点
                    territory = dfs(r, c, "WHITE")
                    white_points += len(territory)
        print(f"black_points: {black_points}, white_points: {white_points}")
        if black_points > white_points:
            return "BLACK"
        elif white_points > black_points:
            return "WHITE"
    
    def check_draw(self, board):
        pass # TODO: 围棋有平局吗？