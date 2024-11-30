import pygame
import sys
from commons import *
from chessboard import *
import os
import string
from abc import abstractmethod

# UI模板
class UITemplate():
    """
    游戏用户界面的模板类，提供通用功能，包括事件检测、按钮绘制、消息显示和棋盘绘制。
    """

    def __init__(self):
        """
        初始化 UI 模板，包括窗口设置、字体加载和背景图片加载。
        """
        pygame.init()
        pygame.font.init()
        
        self.FONT = pygame.font.SysFont(None, 40)  # 设置字体大小
        self.SMALLFONT = pygame.font.SysFont(None, 30)  # 设置字体大小
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 创建窗口
        pygame.display.set_caption("Chess Game Platform")  # 设置窗口标题
        self.background_image = pygame.transform.scale(pygame.image.load("pics/backgroud.jpeg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.popup_width, self.popup_height = 600, 400
        self.popup_surface = pygame.Surface((self.popup_width, self.popup_height))
        self.popup_rect = self.popup_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.popup_surface.fill(WHITE)
        
        self.button_admit_defeat = None  # "认输" 按钮
        self.button_restart = None  # "重新开始" 按钮
        self.button_undo = None  # "悔棋" 按钮
        self.button_store_state = None  # "存储局面" 按钮
        self.button_load_state = None  # "加载局面" 按钮
        self.button_capture = None  # "提子" 按钮
        self.button_end_turn = None  # "结束回合" 按钮
        self.button_hint = None  # "提示" 按钮
        
        self.AI_available = False  # 是否提供 AI 玩家
        self.valid_chessboard_size: list[str] = None  # 可选的棋盘大小
        
    def detect_event(self):
        """
        检测鼠标或键盘事件。
        :return: 返回事件类型及相关数据，如果是退出事件则退出程序。
        """
        event = pygame.event.get()
        if len(event) > 0:
            event = event[0]
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return pygame.KEYDOWN, event.key
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return pygame.MOUSEBUTTONDOWN, pygame.mouse.get_pos()
             
    def draw_button(self, text, left, top, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, bg_color=WHITE, text_color=BLACK, update=True) -> pygame.Rect:
        """
        绘制一个按钮。
        :param text: 按钮显示的文本内容
        :param left: 按钮的左边位置
        :param top: 按钮的顶部位置
        :param width: 按钮宽度
        :param height: 按钮高度
        :param bg_color: 按钮背景颜色
        :param text_color: 按钮文字颜色
        :param update: 是否立即更新显示
        :return: 按钮的矩形对象
        """
        button = pygame.Rect(left, top, width, height)  # 创建按钮矩形
        pygame.draw.rect(self.screen, bg_color, button)  # 绘制按钮背景
        text_rendered = self.FONT.render(text, True, text_color)  # 渲染按钮文字
        # 将文字居中显示在按钮上
        self.screen.blit(text_rendered, (left + (width - text_rendered.get_width()) // 2, top + (height - text_rendered.get_height()) // 2))
        
        if update:
            pygame.display.flip()
        
        return button
    
    def display_message(self, text, color=RED, left=None, top=None):
        """
        在屏幕上显示消息。
        :param text: 显示的消息内容
        :param color: 消息文字颜色
        :param left: 消息左边位置（默认居中）
        :param top: 消息顶部位置（默认在屏幕顶部1/3处）
        """
        message = self.FONT.render(text, True, color)  # 渲染消息文字
        if left is None:
            left = SCREEN_WIDTH // 2 - message.get_width() // 2
        if top is None:
            top = SCREEN_HEIGHT // 3
        self.screen.blit(message, (left, top))

    def choose_game(self):
        """
        显示游戏选择界面，允许用户选择五子棋或围棋。
        :return: 用户选择的游戏名称 ("Gomoku" 或 "Go")
        """
        self.screen.fill(BLACK)
        self.display_message("Choose a Game")
        
        while True:
            button_gomoku = self.draw_button("Gomoku", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, BUTTON_TOP, BUTTON_WIDTH, BUTTON_HEIGHT)
            button_go = self.draw_button("Go", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, BUTTON_TOP + BUTTON_INTERVAL, BUTTON_WIDTH, BUTTON_HEIGHT)
            button_othello = self.draw_button("Othello", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, BUTTON_TOP + 2 * BUTTON_INTERVAL, BUTTON_WIDTH, BUTTON_HEIGHT)
            pygame.display.flip()
            
            event = self.detect_event()
            if event is not None:
                event_type, event_val = event
                if event_type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event_val
                    if button_gomoku.collidepoint(mouse_pos):
                        return "Gomoku"
                    elif button_go.collidepoint(mouse_pos):
                        return "Go"
                    elif button_othello.collidepoint(mouse_pos):
                        return "Othello"
                    
    def choose_board_size(self):
        """
        显示棋盘大小选择界面。
        :return: 用户选择的棋盘大小
        """
        button_choose_size = self.draw_button("Choose board size", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 150, bg_color=BLACK, text_color=WHITE)
        display_options = False  # 是否显示选项
        
        while True:
            self.screen.fill(BLACK)
  
            button_choose_size = self.draw_button("Choose board size", SCREEN_WIDTH // 2 - 1.5 * BUTTON_WIDTH // 2, 150, width=1.5 * BUTTON_WIDTH, update=False)
            
            if display_options:
                # 绘制大小选项按钮
                for index, option in enumerate(self.valid_chessboard_size):
                    self.draw_button(option, SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 220 + (index * (OPTION_HEIGHT + 5)), height=OPTION_HEIGHT, update=False)
            
            pygame.display.flip()
            
            event = self.detect_event()
            if event is not None:
                event_type, event_val = event
                if event_type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event_val
                    
                    if button_choose_size.collidepoint(mouse_pos):
                        display_options = not display_options  # 切换选项显示状态
                        
                    if display_options:
                        for index, option in enumerate(self.valid_chessboard_size):
                            button_option = self.draw_button(option, SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 220 + (index * (OPTION_HEIGHT + 5)), update=False)
                            if button_option.collidepoint(mouse_pos):
                                return int(option)

    def show_winner(self, winner: str):
        """
        显示获胜者信息，并提供重新开始和退出选项。
        :param winner: 获胜方的名称 ("BLACK" 或 "WHITE")，平局时为 None
        """
        self.screen.fill(BLACK)
        self.display_message(f"{winner} win! Press ENTER to continue." if winner else "Draw!")  # 显示获胜信息

        button_new_game = button_end_game = None  # 按钮初始化
        
        while True:
            event = self.detect_event()
            if event is not None:
                event_type, event_val = event
                if event_type == pygame.KEYDOWN:
                    key = event_val
                    if key == pygame.K_RETURN:
                        button_new_game = self.draw_button("New Game", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, BUTTON_TOP)
                        button_end_game = self.draw_button("Exit", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, BUTTON_TOP + BUTTON_INTERVAL)
                
                if button_new_game is not None and button_end_game is not None:
                    if event_type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event_val
                        if button_new_game.collidepoint(mouse_pos):
                            button_new_game_disabled = self.draw_button("", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, BUTTON_TOP, bg_color=BLACK)
                            button_end_game_disabled = self.draw_button("", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, BUTTON_TOP + BUTTON_INTERVAL, bg_color=BLACK)
                            return 
                        elif button_end_game.collidepoint(mouse_pos):
                            pygame.quit()
                            exit()
            pygame.display.flip()

    def display_chessboard(self, chessboard: Chessboard, turn: str, player_name: str, games: int=None, wins: int=None):
        """
        绘制棋盘和当前状态。
        :param chessboard: 当前的棋盘对象
        :param turn: 当前玩家的颜色 ("BLACK" 或 "WHITE")
        """
        self.screen.blit(self.background_image, (0, 0))

        # 绘制棋盘网格
        for row in range(1, chessboard.get_size() + 1):
            pygame.draw.line(self.screen, BLACK, (GRID_SIZE, GRID_SIZE * row),
                             (GRID_SIZE * chessboard.get_size(), GRID_SIZE * row), LINE_WIDTH)
            pygame.draw.line(self.screen, BLACK, (GRID_SIZE * row, GRID_SIZE),
                             (GRID_SIZE * row, GRID_SIZE * chessboard.get_size()), LINE_WIDTH)

        # 绘制棋子
        for row in range(chessboard.get_size()):
            for col in range(chessboard.get_size()):
                curr_chess = chessboard.get_chess(row=row, col=col)
                if curr_chess == "BLACK":
                    pygame.draw.circle(self.screen, BLACK, (GRID_SIZE * (col + 1), GRID_SIZE * (row + 1)), CHESS_RADIUS)
                elif curr_chess == "WHITE":
                    pygame.draw.circle(self.screen, WHITE, (GRID_SIZE * (col + 1), GRID_SIZE * (row + 1)), CHESS_RADIUS)
                    
        self.display_right_sidebar(turn, player_name, games, wins)

    @ abstractmethod
    def display_right_sidebar(self):
        """
        绘制右侧操作面板（具体实现由子类提供）。
        """
        pass
        
    def choose_player(self):
        """
        弹窗1：
            选择玩家类型（已注册用户，未注册用户，游客，AI）。
        弹窗2：
            已注册用户：输入账号、密码。
            未注册用户：输入账号、密码。
            AI：选择AI等级（一级， 二级， 三级）。
            确认键：关闭两个弹窗。
        :return: is_guest, is_AI, is_registered_user, username, password, ai_level
        """
        pygame.draw.rect(self.popup_surface, BLACK, self.popup_surface.get_rect(), 2)

        # 初始化选项
        player_type = None  # 玩家类型
        username, password, ai_level = "", "", None
        is_guest, is_AI, is_registered_user = False, False, False
        input_active = {"username": False, "password": False}

        # 按钮定义
        button_registered = pygame.Rect(50, 50, 300, 40)
        button_unregistered = pygame.Rect(50, 100, 300, 40)
        button_guest = pygame.Rect(50, 150, 300, 40)
        button_AI = pygame.Rect(50, 200, 300, 40)
        button_confirm = pygame.Rect(250, 350, 100, 40)
        confirm_text = self.SMALLFONT.render("Confirm", True, WHITE)

        # 输入框定义
        input_username = pygame.Rect(50, 50, 300, 40)
        input_password = pygame.Rect(50, 130, 300, 40)
        input_texts = {"username": "", "password": ""}

        # AI等级选项
        ai_buttons = [
            pygame.Rect(50, 50, 200, 40),
            pygame.Rect(50, 100, 200, 40),
        ]
        ai_texts = ["Level 1", "Level 2"]

        running = True
        while running:
            self.popup_surface.fill(WHITE)
            pygame.draw.rect(self.popup_surface, BLACK, self.popup_surface.get_rect(), 2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # 鼠标点击事件
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    mouse_x, mouse_y = event.pos
                    mouse_pos = (mouse_x - self.popup_rect.x, mouse_y - self.popup_rect.y)

                    # 第一弹窗选择玩家类型
                    if player_type is None:
                        if button_registered.collidepoint(mouse_pos):
                            player_type = "registered"
                            is_registered_user = True
                        elif button_unregistered.collidepoint(mouse_pos):
                            player_type = "unregistered"
                        elif button_guest.collidepoint(mouse_pos):
                            player_type = "guest"
                            is_guest = True
                            running = False
                        elif self.AI_available and button_AI.collidepoint(mouse_pos):
                            player_type = "AI"

                    # 第二弹窗输入信息
                    elif player_type in ["registered", "unregistered"]:
                        if input_username.collidepoint(mouse_pos):
                            input_active["username"] = True
                            input_active["password"] = False
                        elif input_password.collidepoint(mouse_pos):
                            input_active["username"] = False
                            input_active["password"] = True
                        else:
                            input_active = {"username": False, "password": False}
                        # 点击确认键退出
                        if button_confirm.collidepoint(mouse_pos):
                            username = input_texts["username"]
                            password = input_texts["password"]
                            running = False

                    elif player_type == "AI":
                        for i, button in enumerate(ai_buttons):
                            if button.collidepoint(mouse_pos):
                                ai_level = i + 1
                                is_AI = True
                                running = False

                # 键盘输入事件
                if event.type == pygame.KEYDOWN and player_type in ["registered", "unregistered"]:
                    if input_active["username"]:
                        if event.key == pygame.K_BACKSPACE:
                            input_texts["username"] = input_texts["username"][:-1]
                        else:
                            input_texts["username"] += event.unicode
                    elif input_active["password"]:
                        if event.key == pygame.K_BACKSPACE:
                            input_texts["password"] = input_texts["password"][:-1]
                        else:
                            input_texts["password"] += event.unicode

            # 第一弹窗：选择玩家类型
            if player_type is None:
                pygame.draw.rect(self.popup_surface, GRAY, button_registered)
                pygame.draw.rect(self.popup_surface, GRAY, button_unregistered)
                pygame.draw.rect(self.popup_surface, GRAY, button_guest)
                if self.AI_available:
                    pygame.draw.rect(self.popup_surface, GRAY, button_AI)

                self.popup_surface.blit(self.FONT.render("Registered User", True, BLACK), (60, 55))
                self.popup_surface.blit(self.FONT.render("Unregistered User", True, BLACK), (60, 105))
                self.popup_surface.blit(self.FONT.render("Guest", True, BLACK), (60, 155))
                if self.AI_available:
                    self.popup_surface.blit(self.FONT.render("AI", True, BLACK), (60, 205))

            # 第二弹窗：已注册或未注册用户
            elif player_type in ["registered", "unregistered"]:
                if input_active["username"]:
                    pygame.draw.rect(self.popup_surface, BLUE, input_username)
                    username_color = WHITE
                else:
                    pygame.draw.rect(self.popup_surface, GRAY, input_username)
                    username_color = BLACK
                if input_active["password"]:
                    pygame.draw.rect(self.popup_surface, BLUE, input_password)
                    password_color = WHITE
                else:
                    pygame.draw.rect(self.popup_surface, GRAY, input_password)
                    password_color = BLACK

                pygame.draw.rect(self.popup_surface, BLUE, button_confirm)
                self.popup_surface.blit(confirm_text, (button_confirm.x + (button_confirm.width - confirm_text.get_width()) // 2,
                                            button_confirm.y + (button_confirm.height - confirm_text.get_height()) // 2))


                self.popup_surface.blit(self.FONT.render("Username:", True, BLACK), (50, 20))
                self.popup_surface.blit(self.FONT.render(input_texts["username"], True, username_color), (55, 55))
                self.popup_surface.blit(self.FONT.render("Password:", True, BLACK), (50, 100))
                self.popup_surface.blit(self.FONT.render(input_texts["password"], True, password_color), (55, 135))

            # 第二弹窗：AI选择等级
            elif player_type == "AI":
                for i, button in enumerate(ai_buttons):
                    pygame.draw.rect(self.popup_surface, GRAY, button)
                    self.popup_surface.blit(self.FONT.render(ai_texts[i], True, BLACK), (button.x + 10, button.y + 5))

            self.screen.blit(self.popup_surface, self.popup_rect.topleft)
            pygame.display.flip()

        return is_guest, is_AI, is_registered_user, username, password, ai_level
        
    def admit_defeat(self, mouse_pos: tuple[int, int]):
        """
        检查是否点击了认输按钮。
        :param mouse_pos: 鼠标点击位置
        :return: 是否点击了认输按钮
        """
        return self.button_admit_defeat.collidepoint(mouse_pos)
    
    def restart(self, mouse_pos: tuple[int, int]) -> bool:
        """
        判断是否点击了“重新开始”按钮。
        :param mouse_pos (tuple[int, int]): 鼠标的 (x, y) 坐标位置。
        :returnbool: 如果鼠标位置与“重新开始”按钮发生碰撞，则返回 True；否则返回 False。
        """
        return self.button_restart.collidepoint(mouse_pos)

    def undo(self, mouse_pos: tuple[int, int]) -> bool:
        """
        判断是否点击了“撤销”按钮。
        :param mouse_pos (tuple[int, int]): 鼠标的 (x, y) 坐标位置。
        :return bool: 如果鼠标位置与“撤销”按钮发生碰撞，则返回 True；否则返回 False。
        """
        return self.button_undo.collidepoint(mouse_pos)

    def store_state(self, mouse_pos: tuple[int, int]) -> bool:
        """
        判断是否点击了“存储局面”按钮，并打印跳过的提示。
        :param mouse_pos (tuple[int, int]): 鼠标的 (x, y) 坐标位置。
        :return bool: 如果鼠标位置与“存储局面”按钮发生碰撞，则返回 True；否则返回 False。
        """
        return self.button_store_state.collidepoint(mouse_pos)
    
    def load_state(self, mouse_pos: tuple[int, int]) -> bool:
        """
        判断是否点击了“加载局面”按钮，并打印跳过的提示。
        :param mouse_pos (tuple[int, int]): 鼠标的 (x, y) 坐标位置。
        :return bool: 如果鼠标位置与“加载局面”按钮发生碰撞，则返回 True；否则返回 False。
        """
        return self.button_load_state.collidepoint(mouse_pos)
    
    def capture(self, mouse_pos: tuple[int, int]) -> bool:
        """
        判断是否点击了“提子”按钮。
        :param mouse_pos (tuple[int, int]): 鼠标的 (x, y) 坐标位置。
        :return bool: 如果鼠标位置与“提子”按钮发生碰撞，则返回 True；否则返回 False。
        """
        if self.button_capture is None:
            return False
        return self.button_capture.collidepoint(mouse_pos)

    def end_turn(self, mouse_pos: tuple[int, int]) -> bool:
        """
        判断是否点击了“结束回合”按钮。
        :param mouse_pos (tuple[int, int]): 鼠标的 (x, y) 坐标位置。
        :return bool: 如果鼠标位置与“结束回合”按钮发生碰撞，则返回 True；否则返回 False。
        """
        if self.button_end_turn is None:
            return False
        return self.button_end_turn.collidepoint(mouse_pos)
    
    def view_hints(self, mouse_pos: tuple[int, int]) -> bool:
        """
        判断是否点击了“提示”按钮。
        :param mouse_pos (tuple[int, int]): 鼠标的 (x, y) 坐标位置。
        :return bool: 如果鼠标位置与“提示”按钮发生碰撞，则返回 True；否则返回 False。
        """
        return self.button_hint.collidepoint(mouse_pos)
    
    def pop_message(self, message: str, text_color=RED):
        if message is None:
            return
        # 界面参数
        self.popup_surface.fill(WHITE)
        pygame.draw.rect(self.popup_surface, BLACK, self.popup_surface.get_rect(), 2)
        
        # 按钮
        button_rect = pygame.Rect(250, 350, 100, 40)
        button_color = BLUE
        button_text = self.SMALLFONT.render("Got it", True, WHITE)
        
        # 文本显示相关
        text_margin = 20
        text_width = self.popup_width - 2 * text_margin  # 文本区域的最大宽度
        line_height = 20  # 每行文本的高度
        y_offset = 50  # 文本从顶部偏移的初始位置

        # 将信息按行分割（自动换行）
        words = message.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            test_surface = self.SMALLFONT.render(test_line, True, text_color)
            if test_surface.get_width() > text_width:
                lines.append(current_line.strip())
                current_line = word + " "
            else:
                current_line = test_line

        # 添加最后一行
        if current_line:
            lines.append(current_line.strip())

        running = True

        while running:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if self.popup_rect.collidepoint(event.pos):
                        rel_x, rel_y = mouse_x - self.popup_rect.x, mouse_y - self.popup_rect.y
                        
                        # 点击确认按钮
                        if button_rect.collidepoint(rel_x, rel_y):
                            running = False

            # 绘制背景覆盖主界面
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # 半透明黑色
            self.screen.blit(overlay, (0, 0))

            # 绘制浮窗
            self.popup_surface.fill(WHITE)
            pygame.draw.rect(self.popup_surface, BLACK, self.popup_surface.get_rect(), 2)

            # 绘制信息
            if len(lines) == 1:
                # 居中绘制
                message_text = self.SMALLFONT.render(message, True, text_color)
                self.popup_surface.blit(message_text, ((self.popup_surface.get_width() - message_text.get_width()) // 2, (self.popup_surface.get_height() - message_text.get_height()) // 2))
            else:
                current_y = y_offset
                for line in lines:
                    line_surface = self.SMALLFONT.render(line, True, text_color)
                    self.popup_surface.blit(line_surface, (text_margin, current_y))
                    current_y += line_height

            
            # 绘制确认按钮
            pygame.draw.rect(self.popup_surface, button_color, button_rect)
            self.popup_surface.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2,
                                            button_rect.y + (button_rect.height - button_text.get_height()) // 2))

            # 将浮窗绘制到主屏幕
            self.screen.blit(self.popup_surface, self.popup_rect.topleft)

            pygame.display.flip()
    
    def select_file(self, is_store: bool):
        """
        弹出新窗口，用户选择目录，并输入文件名以存储当前局面。
        :return: 用户选择的文件完整路径字符串，如果用户取消则返回空字符串。
        """
        current_dir = ('./states')

        # 界面参数
        self.popup_surface.fill(WHITE)
        pygame.draw.rect(self.popup_surface, BLACK, self.popup_surface.get_rect(), 2)

        # 输入框
        input_box_color = BLACK
        input_box = pygame.Rect(50, 300, 500, 40)
        input_text = ''
        active = False

        # 按钮
        button_rect = pygame.Rect(250, 350, 100, 40)
        button_color = BLUE
        button_text = self.SMALLFONT.render("Confirm", True, WHITE)
        cancel_button_rect = pygame.Rect(360, 350, 100, 40)
        cancel_button_color = GRAY
        cancel_button_text = self.SMALLFONT.render("Cancel", True, BLACK)

        running = True
        result_path = ''

        while running:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if self.popup_rect.collidepoint(event.pos):
                        rel_x, rel_y = mouse_x - self.popup_rect.x, mouse_y - self.popup_rect.y

                        # 点击输入框
                        if input_box.collidepoint(rel_x, rel_y):
                            input_box_color = BLUE
                            active = True
                        else:
                            input_box_color = BLACK
                            active = False

                        # 点击确认按钮
                        if button_rect.collidepoint(rel_x, rel_y):
                            input_text = input_text.strip()
                            if not input_text and is_store:
                                self.display_message("Please enter a valid file name!", color=(255, 0, 0),
                                                    left=self.popup_rect.x + 50, top=self.popup_rect.y + 250)
                            else:
                                result_path = os.path.join(current_dir, input_text) if input_text else current_dir
                                running = False

                        # 点击取消按钮
                        if cancel_button_rect.collidepoint(rel_x, rel_y):
                            return

                        # 点击目录项
                        entry_items = os.listdir(current_dir) if os.path.isdir(current_dir) else []
                        for i, entry in enumerate(entry_items):
                            entry_rect = pygame.Rect(50, 50 + i * 30, 500, 30)
                            if entry_rect.collidepoint(rel_x, rel_y):
                                selected_path = os.path.join(current_dir, entry)
                                if (os.path.isdir(selected_path) and is_store) or not is_store:
                                    current_dir = selected_path
                                break

                elif event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        elif event.key == pygame.K_RETURN:
                            active = False
                        else:
                            if event.unicode in string.printable:
                                input_text += event.unicode

            # 绘制背景覆盖主界面
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # 半透明黑色
            self.screen.blit(overlay, (0, 0))

            # 绘制浮窗
            self.popup_surface.fill(WHITE)
            pygame.draw.rect(self.popup_surface, BLACK, self.popup_surface.get_rect(), 2)

            # 标题
            title_text = self.SMALLFONT.render(f"Current Directory: {current_dir}", True, BLACK)
            self.popup_surface.blit(title_text, (50, 20))

            # 绘制目录内容
            entries = os.listdir(current_dir) if os.path.isdir(current_dir) else []
            for i, entry in enumerate(entries[:10]):  # 仅显示前10项，防止溢出
                entry_color = GRAY if os.path.isdir(os.path.join(current_dir, entry)) else LIGHT_GRAY
                entry_rect = pygame.Rect(50, 50 + i * 30, 500, 30)
                pygame.draw.rect(self.popup_surface, entry_color, entry_rect)
                entry_text = self.SMALLFONT.render(entry, True, BLACK)
                self.popup_surface.blit(entry_text, (entry_rect.x + 5, entry_rect.y + 5))

            # 绘制输入框
            pygame.draw.rect(self.popup_surface, WHITE, input_box)
            pygame.draw.rect(self.popup_surface, input_box_color, input_box, 2)
            input_surf = self.SMALLFONT.render(input_text, True, BLACK)
            self.popup_surface.blit(input_surf, (input_box.x + 5, input_box.y + 5))

            # 绘制确认按钮
            pygame.draw.rect(self.popup_surface, button_color, button_rect)
            self.popup_surface.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2,
                                            button_rect.y + (button_rect.height - button_text.get_height()) // 2))

            # 绘制取消按钮
            pygame.draw.rect(self.popup_surface, cancel_button_color, cancel_button_rect)
            self.popup_surface.blit(cancel_button_text, (cancel_button_rect.x + (cancel_button_rect.width - cancel_button_text.get_width()) // 2,
                                                    cancel_button_rect.y + (cancel_button_rect.height - cancel_button_text.get_height()) // 2))

            # 将浮窗绘制到主屏幕
            self.screen.blit(self.popup_surface, self.popup_rect.topleft)

            pygame.display.flip()

        return result_path
                    
# 具体产品（五子棋UI）
class GomokuUI(UITemplate):
    """
    五子棋用户界面类，继承自 UITemplate。
    提供五子棋特有的右侧操作面板布局。
    """
    def __init__(self) -> None:
        super().__init__()
        self.AI_available = True
        self.valid_chessboard_size = [str(i) for i in range(8, 20)]
        
    def display_right_sidebar(self, turn, player_name, games: int=None, wins: int=None):
        """
        绘制右侧操作面板，包含当前玩家的轮次信息和操作按钮。
        :param turn: 当前玩家的颜色 ("BLACK" 或 "WHITE")
        """
        # 显示当前玩家轮次信息
        message_turn = self.display_message(
            f"{player_name}'s Turn.", 
            left=COMMON_BUTTON_LEFT, 
            top=GRID_SIZE, 
            color=WHITE if turn == "WHITE" else BLACK
        )
        
        # 显示当前玩家对战场次信息
        if games is not None:
            assert wins is not None
            message_info = self.display_message(
                f"games: {games}, wins: {wins}", 
                left=COMMON_BUTTON_LEFT, 
                top=1.8 * GRID_SIZE, 
                color=WHITE if turn == "WHITE" else BLACK
            )
                    
        # 绘制 "认输" 按钮
        self.button_admit_defeat = self.draw_button(
            "Admit Defeat", 
            COMMON_BUTTON_LEFT, 
            GRID_SIZE + BUTTON_INTERVAL, 
            update=False
        )
        
        # 绘制 "重新开始" 按钮
        self.button_restart = self.draw_button(
            "Restart", 
            COMMON_BUTTON_LEFT, 
            GRID_SIZE + 2 * BUTTON_INTERVAL, 
            update=False
        )
        
        # 绘制 "悔棋" 按钮
        self.button_undo = self.draw_button(
            "Undo", 
            COMMON_BUTTON_LEFT, 
            GRID_SIZE + 3 * BUTTON_INTERVAL, 
            update=False
        )
        
        # 绘制 "存储局面" 按钮
        self.button_store_state = self.draw_button(
            "Store State", 
            COMMON_BUTTON_LEFT, 
            GRID_SIZE + 4 * BUTTON_INTERVAL, 
            update=False
        )
        
        # 绘制 "加载局面" 按钮
        self.button_load_state = self.draw_button(
            "Load State", 
            COMMON_BUTTON_LEFT, 
            GRID_SIZE + 5 * BUTTON_INTERVAL, 
            update=False
        )
        
        # 绘制 "提示" 按钮
        self.button_hint = self.draw_button(
            "View Hints", 
            COMMON_BUTTON_LEFT, 
            GRID_SIZE + 6 * BUTTON_INTERVAL, 
            update=False
        )
                
        # 更新屏幕显示
        pygame.display.flip()

          
# 具体产品（围棋UI）
class GoUI(UITemplate):
    """
    围棋用户界面类，继承自 UITemplate。
    提供围棋特有的右侧操作面板布局。
    """
    def __init__(self) -> None:
        """
        初始化围棋 UI 类，调用父类的初始化方法。
        """
        super().__init__()
        self.valid_chessboard_size = [str(i) for i in range(8, 20)]
        
    def display_right_sidebar(self, turn, player_name, games: int=None, wins: int=None):
        """
        绘制右侧操作面板，包含当前玩家的轮次信息和操作按钮。
        :param turn: 当前玩家的颜色 ("BLACK" 或 "WHITE")
        """
        # 显示当前玩家轮次信息
        message_turn = self.display_message(
            f"{player_name}'s Turn.",
            left=COMMON_BUTTON_LEFT,
            top=GRID_SIZE,
            color=WHITE if turn == "WHITE" else BLACK
        )
        
        # 显示当前玩家对战场次信息
        if games is not None:
            assert wins is not None
            message_info = self.display_message(
                f"games: {games}, wins: {wins}", 
                left=COMMON_BUTTON_LEFT, 
                top=1.8 * GRID_SIZE, 
                color=WHITE if turn == "WHITE" else BLACK
            )
                    
        # 绘制 "认输" 按钮
        self.button_admit_defeat = self.draw_button(
            "Admit Defeat",
            COMMON_BUTTON_LEFT,
            GRID_SIZE + BUTTON_INTERVAL,
            update=False
        )
        
        # 绘制 "重新开始" 按钮
        self.button_restart = self.draw_button(
            "Restart",
            COMMON_BUTTON_LEFT,
            GRID_SIZE + 2 * BUTTON_INTERVAL,
            update=False
        )
        
        # 绘制 "悔棋" 按钮
        self.button_undo = self.draw_button(
            "Undo",
            COMMON_BUTTON_LEFT,
            GRID_SIZE + 3 * BUTTON_INTERVAL,
            update=False
        )
        
        # 绘制 "存储局面" 按钮
        self.button_store_state = self.draw_button(
            "Store State", 
            COMMON_BUTTON_LEFT, 
            GRID_SIZE + 4 * BUTTON_INTERVAL, 
            update=False
        )
        
        # 绘制 "加载局面" 按钮
        self.button_load_state = self.draw_button(
            "Load State", 
            COMMON_BUTTON_LEFT, 
            GRID_SIZE + 5 * BUTTON_INTERVAL, 
            update=False
        )
        
        # 绘制 "提子" 按钮
        self.button_capture = self.draw_button(
            "Capture", 
            COMMON_BUTTON_LEFT, 
            GRID_SIZE + 6 * BUTTON_INTERVAL, 
            update=False
        )
        
        # 绘制 "结束回合" 按钮
        self.button_end_turn = self.draw_button(
            "End Turn", 
            COMMON_BUTTON_LEFT, 
            GRID_SIZE + 7 * BUTTON_INTERVAL, 
            update=False
        )
        
        # 绘制 "提示" 按钮
        self.button_hint = self.draw_button(
            "View Hints", 
            COMMON_BUTTON_LEFT, 
            GRID_SIZE + 8 * BUTTON_INTERVAL, 
            update=False
        )
                
        # 更新屏幕显示
        pygame.display.flip()

# 具体产品（黑白棋UI）
class OthelloUI(UITemplate):
    """
    黑白棋用户界面类，继承自 UITemplate。
    提供黑白棋特有的右侧操作面板布局。
    """
    def __init__(self) -> None:
        super().__init__()
        self.AI_available = True
        self.valid_chessboard_size = ['8']
        
    def display_right_sidebar(self, turn, player_name, games: int=None, wins: int=None):
        """
        绘制右侧操作面板，包含当前玩家的轮次信息和操作按钮。
        :param turn: 当前玩家的颜色 ("BLACK" 或 "WHITE")
        """
        # 显示当前玩家轮次信息
        message_turn = self.display_message(
            f"{player_name}'s Turn.", 
            left=COMMON_BUTTON_LEFT, 
            top=GRID_SIZE, 
            color=WHITE if turn == "WHITE" else BLACK
        )
        
        # 显示当前玩家对战场次信息
        if games is not None:
            assert wins is not None
            message_info = self.display_message(
                f"games: {games}, wins: {wins}", 
                left=COMMON_BUTTON_LEFT, 
                top=1.8 * GRID_SIZE, 
                color=WHITE if turn == "WHITE" else BLACK
            )
                    
        # 绘制 "认输" 按钮
        self.button_admit_defeat = self.draw_button(
            "Admit Defeat", 
            COMMON_BUTTON_LEFT, 
            GRID_SIZE + BUTTON_INTERVAL, 
            update=False
        )
        
        # 绘制 "重新开始" 按钮
        self.button_restart = self.draw_button(
            "Restart", 
            COMMON_BUTTON_LEFT, 
            GRID_SIZE + 2 * BUTTON_INTERVAL, 
            update=False
        )
        
        # 绘制 "悔棋" 按钮
        self.button_undo = self.draw_button(
            "Undo", 
            COMMON_BUTTON_LEFT, 
            GRID_SIZE + 3 * BUTTON_INTERVAL, 
            update=False
        )
        
        # 绘制 "存储局面" 按钮
        self.button_store_state = self.draw_button(
            "Store State", 
            COMMON_BUTTON_LEFT, 
            GRID_SIZE + 4 * BUTTON_INTERVAL, 
            update=False
        )
        
        # 绘制 "加载局面" 按钮
        self.button_load_state = self.draw_button(
            "Load State", 
            COMMON_BUTTON_LEFT, 
            GRID_SIZE + 5 * BUTTON_INTERVAL, 
            update=False
        )
        
        # 绘制 "提示" 按钮
        self.button_hint = self.draw_button(
            "View Hints", 
            COMMON_BUTTON_LEFT, 
            GRID_SIZE + 6 * BUTTON_INTERVAL, 
            update=False
        )
                
        # 更新屏幕显示
        pygame.display.flip()
        