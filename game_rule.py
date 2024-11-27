from abc import ABC, abstractmethod
from chessboard import Chessboard

# 策略接口，定义通用的游戏规则方法
class GameRule(ABC):
    @abstractmethod
    def is_valid_move(self, row: int, col: int, board: Chessboard, curr_turn: str, turn_taken: bool) -> tuple[bool, str]:
        """
        检查当前玩家的落子是否有效。
        :param row: 棋子行坐标
        :param col: 棋子列坐标
        :param board: 当前棋盘状态（Chessboard 对象）
        :param curr_turn: 当前玩家的颜色（"BLACK" 或 "WHITE"）
        :param turn_taken: 当前回合玩家是否已经落子
        :return: 是否为有效落子（布尔值），非法时错误信息（str）
        """
        pass
    
    @abstractmethod
    def is_within_board(self, row: int, col: int, board: Chessboard):
        """
        检查指定位置是否在棋盘范围内。
        :param row: 棋子行坐标
        :param col: 棋子列坐标
        :param board: 当前棋盘状态（Chessboard 对象）
        :return: 是否在范围内（布尔值）
        """
        pass

    @abstractmethod
    def check_win(self, board: Chessboard):
        """
        检查是否有人获胜。
        :param board: 当前棋盘状态（Chessboard 对象）
        :return: 获胜方颜色（"BLACK" 或 "WHITE"），若无人获胜则返回 None
        """
        pass
    
    @abstractmethod
    def check_draw(self, board: Chessboard):
        """
        检查是否平局。
        :param board: 当前棋盘状态（Chessboard 对象）
        :return: 是否为平局（布尔值）
        """
        pass
    
    def set_chess(self, row: int, col: int, board: Chessboard, curr_turn: str):
        """
        在棋盘上放置棋子。
        :param row: 棋子行坐标
        :param col: 棋子列坐标
        :param board: 当前棋盘状态（Chessboard 对象）
        :param curr_turn: 当前玩家的颜色（"BLACK" 或 "WHITE"）
        """
        board.set_chess(row, col, curr_turn)

# 具体策略类：五子棋规则
class GomokuRule(GameRule):
    def is_valid_move(self, row, col, board, curr_turn, turn_taken):
        """
        检查五子棋的落子是否有效。
        规则：位置在棋盘内，且为空。
        :param row: 棋子行坐标
        :param col: 棋子列坐标
        :param board: 当前棋盘状态（Chessboard 对象）
        :param curr_turn: 当前玩家的颜色（"BLACK" 或 "WHITE"）
        :param turn_taken: 当前回合玩家是否已经落子
        :return: 是否为有效落子（布尔值）
        """
        if not self.is_within_board(row, col, board):
            return False, None
        if turn_taken:
            return False, "[Invalid move] Turn already taken."
        if board.get_chess(row=row, col=col) is not None:
            return False, "[Invalid move] Chess already set here."
        return True, None

    def is_within_board(self, row, col, board):
        """
        检查是否在棋盘范围内。
        :param row: 棋子行坐标
        :param col: 棋子列坐标
        :param board: 当前棋盘状态（Chessboard 对象）
        :return: 是否在范围内（布尔值）
        """
        return 0 <= row < board.get_size() and 0 <= col < board.get_size()

    def check_win(self, board):
        """
        检查五子棋是否有人获胜。
        判断方法：以每个棋子为中心，检查四个方向（横、纵、正斜、反斜）是否有连续 5 个同色棋子。
        :param board: 当前棋盘状态（Chessboard 对象）
        :return: 获胜方颜色（"BLACK" 或 "WHITE"），若无人获胜则返回 None
        """
        def check_direction(row, col, d_row, d_col):
            """
            检查某个方向上是否有连续 5 个同色棋子。
            :param row: 棋子起始行坐标
            :param col: 棋子起始列坐标
            :param d_row: 行方向的增量
            :param d_col: 列方向的增量
            :return: 是否满足获胜条件（布尔值）
            """
            color = board.get_chess(row, col)
            count = 1
            # 检查正方向
            for i in range(1, 5):
                curr_row, curr_col = row + i * d_row, col + i * d_col
                if self.is_within_board(curr_row, curr_col, board) and board.get_chess(curr_row, curr_col) == color:
                    count += 1
                else:
                    break
            # 检查反方向
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
                # 检查四个方向是否有胜利条件
                if (check_direction(row, col, 0, 1) or  # 横排
                    check_direction(row, col, 1, 0) or  # 纵排
                    check_direction(row, col, 1, 1) or  # 正对角线
                    check_direction(row, col, 1, -1)):  # 反对角线
                    return board.get_chess(row, col)  # 返回获胜方的颜色
        return None
    
    def check_draw(self, board):
        """
        检查是否平局。
        条件：棋盘已满且无人获胜。
        :param board: 当前棋盘状态（Chessboard 对象）
        :return: 是否为平局（布尔值）
        """
        return all(board.get_chess(row, col) is not None for row in range(board.get_size()) for col in range(board.get_size()))

# 具体策略类：围棋规则
class GoRule(GameRule):
    def get_territory(self, row: int, col: int, board: Chessboard) -> list[(int, int)]:
        """
        通过深度优先搜索，找到指定位置棋子的连通区域。
        :param row: 起始行坐标
        :param col: 起始列坐标
        :param board: 棋盘对象
        :return: 连通区域内的所有点（坐标列表）
        """
        visited = [[False for _ in range(board.get_size())] for _ in range(board.get_size())]
        
        def dfs(row, col, color):
            """
            使用深度优先搜索找到与指定棋子颜色连通的所有点。
            :param row: 当前点的行坐标
            :param col: 当前点的列坐标
            :param color: 当前棋子的颜色
            :return: 该棋子连通区域的点列表
            """
            stack = [(row, col)]
            territory = []
            while stack:
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
        """
        检查给定区域是否有气（即是否与空位相邻）。
        :param territory: 检查的区域点列表
        :param board: 棋盘对象
        :return: 是否有气
        """
        for (row, col) in territory:
            neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
            for (r, c) in neighbors:
                if self.is_within_board(r, c, board) and board.get_chess(r, c) is None:  # 空位表示有气
                    return True
        return False
     
    def get_curr_capture(self, row: int, col: int, board: Chessboard) -> list[(int, int)]:
        """
        检查当前落子后可以提取的对方棋子。
        :param row: 当前落子的行坐标
        :param col: 当前落子的列坐标
        :param board: 棋盘对象
        :return: 可以提的对方棋子位置列表
        """
        assert self.is_within_board(row, col, board)
        self_color = board.get_chess(row, col)
        rival_color = "WHITE" if self_color == "BLACK" else "BLACK"
        
        curr_capture = []
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for (r, c) in neighbors:
            if self.is_within_board(r, c, board) and board.get_chess(r, c) == rival_color:
                rival_territory = self.get_territory(r, c, board)  # 对手的连通区域
                if not self.has_liberty(rival_territory, board):  # 对手无气，可以提
                    curr_capture.extend(rival_territory)
        return curr_capture
     
    def capture(self, territory: list[(int, int)], board: Chessboard):
        """
        提子操作，移除棋盘上的指定区域。
        :param territory: 被提的棋子点列表
        :param board: 棋盘对象
        """
        for (row, col) in territory:
            board.set_chess(row, col, None)
          
    def is_valid_move(self, row, col, board, curr_turn, turn_taken):
        """
        检查当前落子是否有效。
        规则：
        1. 落子在棋盘范围内，且位置为空。
        2. 落子后不能无气，除非可以提子。
        :param row: 落子行坐标
        :param col: 落子列坐标
        :param board: 棋盘对象
        :param curr_turn: 当前落子方颜色
        :param turn_taken: 当前回合玩家是否已经落子
        :return: 是否为有效落子
        """
        if not self.is_within_board(row, col, board):
            return False, None
        if turn_taken:
            return False, "[Invalid move] Turn already taken."
        if board.get_chess(row=row, col=col) is not None:
            return False, "[Invalid move] Chess already set here."
    
        # 暂时落子
        board.set_chess(row, col, curr_turn)
        curr_territory = self.get_territory(row, col, board)
        
        if not self.has_liberty(curr_territory, board):
            # 判断落子后是否可提子
            if self.get_curr_capture(row, col, board):
                board.set_chess(row, col, None)
                return True, None
            else:
                board.set_chess(row, col, None)
                return False, "[Invalid move] Lose your liberty while no opponent chess to be captured."
        else:
            board.set_chess(row, col, None)
            return True, None
    
    def is_within_board(self, row, col, board):
        """
        检查指定位置是否在棋盘范围内。
        :param row: 行坐标
        :param col: 列坐标
        :param board: 棋盘对象
        :return: 是否在范围内（布尔值）
        """
        return 0 <= row < board.get_size() and 0 <= col < board.get_size()

    def check_win(self, board):
        """
        检查是否分出胜负，基于围棋计分规则：
        1. 清除棋盘上无气的子。
        2. 根据棋盘状态计算双方得分。
        3. 黑棋让六目半。
        :param board: 棋盘对象
        :return: 获胜方颜色（"BLACK" 或 "WHITE"），若无胜负返回 None
        """
        # 清除无气的子
        for row in range(board.get_size()):
            for col in range(board.get_size()):
                territory = self.get_territory(row, col, board)
                if not self.has_liberty(territory, board):
                    self.capture(territory, board)
                    
        black_points = 0
        white_points = 3.25  # 黑子让六目半
        visited = [[False for _ in range(board.get_size())] for _ in range(board.get_size())]

        for row in range(board.get_size()):
            for col in range(board.get_size()):
                if visited[row][col]:
                    continue
                territory = self.get_territory(row, col, board)  # 当前领土面积
                if board.get_chess(row, col) == "BLACK":
                    black_points += len(territory)
                elif board.get_chess(row, col) == "WHITE":
                    white_points += len(territory)
                for (r, c) in territory:
                    visited[r][c] = True
        if black_points > white_points:
            return "BLACK"
        elif white_points > black_points:
            return "WHITE"
    
    def check_draw(self, board):
        """
        检查围棋是否平局。
        当前逻辑未实现。
        :param board: 棋盘对象
        :return: 是否为平局（布尔值）
        """
        pass  # TODO: 围棋有平局吗？
        