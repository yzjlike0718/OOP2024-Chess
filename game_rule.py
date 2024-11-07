from abc import ABC, abstractmethod

# 策略接口
class GameRule(ABC):
    @abstractmethod
    def is_valid_move(self):
        pass

    @abstractmethod
    def check_win(self):
        pass
    
    # TODO: more rules

# 具体策略类：五子棋规则
class GomokuRule(GameRule):
    def is_valid_move(self):
        raise NotImplementedError

    def check_win(self):
        raise NotImplementedError

# 具体策略类：围棋规则
class GoRule(GameRule):
    def is_valid_move(self):
        raise NotImplementedError

    def check_win(self):
        raise NotImplementedError