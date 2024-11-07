from abc import ABC, abstractmethod

# 抽象模板类
class GameProcessTemplate(ABC):
    def playGame(self):
        self.init_board()
        while True:
            self.take_turn()
            if self.is_end():
                break
        self.end_game()

    @abstractmethod
    def init_board(self):
        pass

    @abstractmethod
    def take_turn(self):
        pass

    @abstractmethod
    def is_end(self):
        pass

    @abstractmethod
    def end_game(self):
        pass

# 具体实现类：五子棋游戏流程
class GomokuProcess(GameProcessTemplate):
    def __init__(self):
        raise NotImplementedError

    def init_board(self):
        raise NotImplementedError

    def take_turn(self):
        raise NotImplementedError

    def is_end(self):
        raise NotImplementedError

    def end_game(self):
        raise NotImplementedError

# 具体实现类：围棋游戏流程
class GoProcess(GameProcessTemplate):
    def __init__(self):
        raise NotImplementedError

    def init_board(self):
        raise NotImplementedError
    
    def take_turn(self):
        raise NotImplementedError

    def is_end(self):
        raise NotImplementedError

    def end_game(self):
        raise NotImplementedError
