class Player():
    def __init__(self, is_guest: bool, is_AI: bool, name: str, color: str, games: int=None, wins: int=None) -> None:
        self.is_guest = is_guest
        self.is_AI = is_AI
        self.name = name
        self.color = color
        self.games = games
        self.wins = wins

    def show_info(self):
        print(f"type: {type(self)}, is_guest: {self.is_guest}, is_AI: {self.is_AI}, name: {self.name}, color: {self.color}")
        