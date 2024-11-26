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
    
    @abstractmethod
    def set_chess(self, row: int, col: int, board: Chessboard, curr_turn: str):
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

    def set_chess(self, row, col, board, curr_turn):
        board.set_chess(row, col, curr_turn)

# 具体策略类：围棋规则
class GoRule(GameRule):
    def get_territory(self, row: int, col: int, board: Chessboard) -> list[(int, int)]:
        visited = [[False for _ in range(board.get_size())] for _ in range(board.get_size())]
        
        def dfs(row, col, color):
            # 深搜：找到一方棋子连接的所有点
            stack = [(row, col)]
            territory = []
            while stack != []:
                r, c = stack.pop()
                if not self.is_within_board(r, c, board) or visited[r][c]:
                    continue
                if board.get_chess(r, c) == color:
                    visited[r][c] = True
                    territory.append((r, c))
                    # 向四个方向扩展
                    stack.append((r + 1, c))
                    stack.append((r - 1, c))
                    stack.append((r, c + 1))
                    stack.append((r, c - 1))
            return territory
        
        return dfs(row, col, board.get_chess(row, col))
        
    def has_liberty(self, territory: list[(int, int)], board: Chessboard) -> bool:
        # 检查 territory 是否有气
        print(f"check has_liberty territory: {territory}")
        for (row, col) in territory:
            neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
            for (r, c) in neighbors:
                if self.is_within_board(r, c, board):
                    if board.get_chess(r, c) == None:  # 空位表示有气
                        return True
        
        # 如果遍历所有点都没有找到气，则返回 False
        return False
     
    def get_curr_capture(self, row: int, col: int, board: Chessboard) -> list[(int, int)]:
        # 检查当前在 (row, col) 落子后，上下左右可以提的子
                        
        assert self.is_within_board(row, col, board)
        self_color = board.get_chess(row, col)
        rival_color = "WHITE" if self_color == "BLACK" else "BLACK"
        
        curr_capture = []
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for (r, c) in neighbors:
            if self.is_within_board(r, c, board) and board.get_chess(r, c) == rival_color:
                rival_territory = self.get_territory(r, c, board) # 对手的连通域
                if not self.has_liberty(rival_territory, board): # 对手的连通域没有气，可以提
                    curr_capture.extend(rival_territory)
        return curr_capture
     
    def capture(self, territory: list[(int, int)], board: Chessboard):
        # 提子
        for (row, col) in territory:
            board.set_chess(row, col, None)
               
    def is_valid_move(self, row, col, board, curr_turn):
        print(f"GoRule is_valid_move row={row}, col={col}, curr_turn={curr_turn}")
        if not self.is_within_board(row, col, board):
            return False
        if board.get_chess(row=row, col=col) is not None:
            return False
    
        # 暂时落子
        board.set_chess(row, col, curr_turn)
        curr_territory = self.get_territory(row, col, board)
        
        if not self.has_liberty(curr_territory, board):
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
        # 清除无气的子
        for row in range(board.get_size()):
            for col in range(board.get_size()):
                territory = self.get_territory(row, col, board)
                if not self.has_liberty(territory, board):
                    self.capture(territory, board)
                    
        black_points = 0
        white_points = 3.25 # 黑子让六目半
        visited = [[False for _ in range(board.get_size())] for _ in range(board.get_size())]

        for row in range(board.get_size()):
            for col in range(board.get_size()):
                if visited[row][col]:
                    continue
                territory = self.get_territory(row, col, board) # 当前领土面积
                if board.get_chess(row, col) == "BLACK":
                    black_points += len(territory)
                elif board.get_chess(row, col) == "WHITE":
                    white_points += len(territory)
                for (r, c) in territory:
                    visited[r][c] = True
        print(f"black_points: {black_points}, white_points: {white_points}")
        if black_points > white_points:
            return "BLACK"
        elif white_points > black_points:
            return "WHITE"
    
    def check_draw(self, board):
        pass # TODO: 围棋有平局吗？
    
    def set_chess(self, row, col, board, curr_turn):
        board.set_chess(row, col, curr_turn)
        curr_capture = self.get_curr_capture(row, col, board)
        self.capture(curr_capture, board)
        