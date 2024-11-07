# 备忘录类
class Memento:
    def __init__(self, chess_label, x, y):
        self.chess_label = chess_label
        self.x = x
        self.y = y

# 负责人角色
class Caretaker:
    def __init__(self):
        self.memento_list = []
        self.index = -1

    def add_memento(self, memento):
        self.memento_list.append(memento)
        self.index += 1

    def get_memento(self, i):
        if 0 <= i < len(self.memento_list):
            return self.memento_list[i]
        else:
            return None

    def undo(self):
        if self.index > 0:
            self.index -= 1
            return self.memento_list[self.index]
        else:
            print("无法悔棋")
            return None

    def redo(self):
        if self.index < len(self.memento_list) - 1:
            self.index += 1
            return self.memento_list[self.index]
        else:
            print("无法撤销悔棋")
            return None