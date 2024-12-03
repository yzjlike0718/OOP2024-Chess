import random
from game_rule import *
from abc import ABC, abstractmethod
from player import *

class GameAI(ABC, Player):
    def __init__(self, name: str, color: str):
        super().__init__(False, True, name, color)
        self.color = color
        self.rule: GameRule = None
        
    @ abstractmethod
    def calculate_move(self, chessboard: Chessboard) -> tuple[int, int]:
        """
        计算 AI 的落子位置。
        :param chessboard: 当前棋盘对象
        :return: 落子位置 (row, col)
        """
        pass
    
# 五子棋
class GomokuAI(GameAI):
    def __init__(self, name, color):
        super().__init__(name, color)
        self.rule: GomokuRule = GomokuRule()
    
    @ abstractmethod
    def calculate_move(self, chessboard):
        pass

class GomokuAILevel1(GomokuAI):
    def __init__(self, name, color):
        super().__init__(name, color)
        
    def calculate_move(self, chessboard: Chessboard):
        """
        执行五子棋一级 AI：在合法位置随机落子。
        :param chessboard: 当前棋盘对象（Chessboard 类实例）
        :return: 随机合法落子的位置 (row, col)
        """
        size = chessboard.get_size()
        valid_moves = []

        # 遍历棋盘，找到所有合法位置
        for row in range(size):
            for col in range(size):
                if self.rule.is_valid_move(row, col, chessboard, self.color, False)[0]:
                    valid_moves.append((row, col))

        # 从合法位置中随机选择一个
        if valid_moves:
            return random.choice(valid_moves)
        else:
            return None  # 无合法位置

class GomokuAILevel2(GomokuAI):
    def __init__(self, name, color):
        super().__init__(name, color)
    
    def calculate_move(self, chessboard: Chessboard):
        """
        执行五子棋二级 AI：基于评分函数选择最优落子。通过简单的规则判断潜在的获胜机会或阻止对手获胜。
        :param chessboard: 当前棋盘对象（Chessboard 类实例）
        :return: 最优落子的位置 (row, col)
        评分策略：
            - 进攻性：己方连续棋子数越多评分越高。
            - 防守性：对手连续棋子数越多评分越高（阻止对手）。
        权重分配：
            - 己方的连续棋子：1 连=10 分，2 连=50 分，3 连=200 分，4 连=1000 分。
            - 对手的连续棋子：1 连=15 分，2 连=70 分，3 连=300 分，4 连=1500 分（防守权重更高）。
        """
        size = chessboard.get_size()
        opponent_color = "BLACK" if self.color == "WHITE" else "WHITE"
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # 横、竖、正斜、反斜方向
        max_score = -1
        best_move = None

        def evaluate_line(row, col, d_row, d_col, color):
            """
            计算从指定位置出发，在某个方向上的连续棋子数。
            :param row: 起始行坐标
            :param col: 起始列坐标
            :param d_row: 行方向增量
            :param d_col: 列方向增量
            :param color: 棋子颜色
            :return: 连续棋子数
            """
            count = 0
            r, c = row + d_row, col + d_col
            while 0 <= r < size and 0 <= c < size and chessboard.get_chess(r, c) == color:
                count += 1
                r += d_row
                c += d_col
            return count

        def score_position(row, col):
            """
            计算某个位置的评分。
            :param row: 行坐标
            :param col: 列坐标
            :return: 评分
            """
            if not self.rule.is_valid_move(row, col, chessboard, self.color, False)[0]:
                return -100  # 非法位置，跳过

            score = 0
            for d_row, d_col in directions:
                # 己方得分
                my_count = evaluate_line(row, col, d_row, d_col, self.color)
                score += [0, 10, 50, 200, 1000][my_count]
                
                # 对手得分（防守权重更高）
                opponent_count = evaluate_line(row, col, d_row, d_col, opponent_color)
                score += [0, 15, 70, 300, 1500][opponent_count]

            return score

        # 遍历棋盘计算每个合法位置的评分
        for row in range(size):
            for col in range(size):
                current_score = score_position(row, col)
                if current_score > max_score:
                    max_score = current_score
                    best_move = (row, col)

        return best_move

# 黑白棋
class OthelloAI(GameAI):
    def __init__(self, name, color):
        super().__init__(name, color)
        self.rule: OthelloRule = OthelloRule()
    
    @ abstractmethod
    def calculate_move(self, chessboard):
        pass
    
class OthelloAILevel1(OthelloAI):
    def __init__(self, name, color):
        super().__init__(name, color)
        
    def calculate_move(self, chessboard: Chessboard):
        """
        执行黑白棋一级 AI：在合法位置随机落子。
        :param chessboard: 当前棋盘对象（Chessboard 类实例）
        :return: 随机合法落子的位置 (row, col)
        """
        size = chessboard.get_size()
        valid_moves = []

        # 遍历棋盘，找到所有合法位置
        for row in range(size):
            for col in range(size):
                if self.rule.is_valid_move(row, col, chessboard, self.color, False)[0]:
                    valid_moves.append((row, col))

        # 从合法位置中随机选择一个
        if valid_moves:
            return random.choice(valid_moves)
        else:
            return None  # 无合法位置

class OthelloAILevel2(OthelloAI):
    def __init__(self, name, color):
        super().__init__(name, color)

    def calculate_move(self, chessboard: Chessboard):
        """
        二级 AI：基于评分函数的策略性落子。
        评分函数设计：
            - 角落优先：棋盘的四个角具有最高评分。
            - 边缘优先：边缘位置的棋子更难被翻转。
            - 翻转棋子数量：能够翻转更多对手棋子的点得分更高。
            - 避免危险区域：避免落子在对手容易占角的位置（如角落的相邻点）。
        :param chessboard: 当前棋盘对象（Chessboard 类实例）
        :return: 最优落子的位置 (row, col)
        """
        size = chessboard.get_size()
        max_score = -1
        best_move = None

        # 评分函数的参数
        corner_positions = [(0, 0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)]
        edge_bonus = 3  # 边缘优先的评分加成
        corner_bonus = 10  # 角落的评分加成
        danger_penalty = -5  # 危险区域的评分惩罚

        def score_position(row, col):
            """
            计算某个位置的评分。
            :param row: 行坐标
            :param col: 列坐标
            :return: 评分
            """
            if not self.rule.is_valid_move(row, col, chessboard, self.color, False)[0]:
                return -100  # 非法位置

            score = 0

            # 加分：翻转的棋子数量
            flippable = self.rule.get_flippable_chess(row, col, chessboard, self.color)
            score += len(flippable)

            # 加分：角落位置
            if (row, col) in corner_positions:
                score += corner_bonus

            # 加分：边缘位置
            if row == 0 or row == size - 1 or col == 0 or col == size - 1:
                score += edge_bonus

            # 减分：危险区域（角落旁边的点）
            danger_positions = [
                (0, 1), (1, 0), (1, 1),  # 左上角
                (0, size - 2), (1, size - 2), (1, size - 1),  # 右上角
                (size - 2, 0), (size - 2, 1), (size - 1, 1),  # 左下角
                (size - 2, size - 2), (size - 1, size - 2), (size - 2, size - 1)  # 右下角
            ]
            if (row, col) in danger_positions:
                score += danger_penalty

            return score

        # 遍历棋盘，计算每个合法位置的评分
        for row in range(size):
            for col in range(size):
                current_score = score_position(row, col)
                if current_score > max_score:
                    max_score = current_score
                    best_move = (row, col)

        return best_move
