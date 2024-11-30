import json
import os
from abc import ABC, abstractmethod
from player import *

class AccountManager(ABC):
    """
    抽象账户管理类，定义账户操作接口。
    """

    @abstractmethod
    def register(self, username: str, password: str) -> tuple[bool, str]:
        """
        注册新用户。
        :param username: 用户名
        :param password: 密码
        :return: 注册是否成功，信息
        """
        pass

    @abstractmethod
    def login(self, username: str, password: str) -> tuple[bool, str]:
        """
        登录账户。
        :param username: 用户名
        :param password: 密码
        :return: 登录是否成功，信息
        """
        pass

class RealAccountManager(AccountManager):
    """
    真实账户管理类，处理账户数据的实际存储与验证。
    """

    def __init__(self, filepath="accounts.json"):
        """
        初始化账户管理类，加载或创建账户存储文件。
        :param filepath: 账户存储文件路径
        """
        self.filepath = filepath
        self._load_accounts()

    def _load_accounts(self):
        """从文件加载账户数据，文件不存在时初始化为空。"""
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                self.accounts = json.load(f)
        else:
            self.accounts = {}

    def _save_accounts(self):
        """将账户数据保存到文件。"""
        with open(self.filepath, "w") as f:
            json.dump(self.accounts, f, indent=4)

    def register(self, username, password) -> tuple[bool, str, tuple[int, int]]:
        """
        注册新用户。
        """
        if username in self.accounts:
            return False, f"Username {username} already exists.", None
        self.accounts[username] = {"password": password, "games": 0, "wins": 0}
        self._save_accounts()
        return True, f"Registration successful. Welcome, {username}!", (self.accounts[username]["games"], self.accounts[username]["wins"])

    def login(self, username, password) -> tuple[bool, str, tuple[int, int]]:
        """
        登录账户。
        """
        if username not in self.accounts:
            return False, f"Username {username} does not exist.", None
        if self.accounts[username]["password"] != password:
            return False, "Incorrect password.", None
        return True, f"Login successful. Welcome back, {username}!", (self.accounts[username]["games"], self.accounts[username]["wins"])
    
    def update_account_info(self, username: str, games: int, wins: int):
        """
        更新登录玩家的战绩信息。
        :param username: 用户名
        :param games: 用户的对战场次
        :param wins: 用户的胜场
        """
        self.accounts[username]["games"] = games
        self.accounts[username]["wins"] = wins
        self._save_accounts()

class ProxyAccountManager(AccountManager):
    """
    代理账户管理类，对真实账户管理类进行代理。
    """

    def __init__(self, real_account_manager: RealAccountManager):
        """
        初始化代理账户管理类。
        :param real_account_manager: 真实账户管理类的实例
        """
        self.real_account_manager = real_account_manager
        self.logged_in_users = set()

    def register(self, username: str, password: str) -> bool:
        """
        代理注册功能，处理前端传入数据并调用真实账户管理类。
        :param username: 用户名
        :param password: 密码
        :return: 注册是否成功
        """
        if not username or not password:
            return False, "Username and password cannot be empty.", None
        return self.real_account_manager.register(username, password)

    def login(self, username: str, password: str) -> bool:
        """
        代理登录功能，处理前端传入数据并调用真实账户管理类。
        :param username: 用户名
        :param password: 密码
        :return: 登录是否成功
        """
        if not username or not password:
            return False, "Username and password cannot be empty.", None
        success, message, game_history = self.real_account_manager.login(username, password)
        if success:
            self.logged_in_users.add(username)
        return success, message, game_history

    def is_logged_in(self, username: str) -> bool:
        """
        检查用户是否已登录。
        :param username: 用户名
        :return: 用户是否已登录
        """
        return username in self.logged_in_users
    
    def update_account_info(self, player: Player):
        """
        更新登录玩家的战绩信息。
        :param player: 用户
        """
        self.real_account_manager.update_account_info(player.name, player.games, player.wins)
        
