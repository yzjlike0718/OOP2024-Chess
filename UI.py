import pygame
import sys
from commons import *
from chessboard import *

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
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 创建窗口
        pygame.display.set_caption("Chess Game Platform")  # 设置窗口标题
        self.background_image = pygame.transform.scale(pygame.image.load("pics/backgroud.jpeg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
        
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
                    
    def choose_board_size(self):
        """
        显示棋盘大小选择界面。
        :return: 用户选择的棋盘大小
        """
        button_choose_size = self.draw_button("Choose board size", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 150, bg_color=BLACK, text_color=WHITE)
        display_options = False  # 是否显示选项
        size_options = [str(i) for i in range(8, 20)]  # 棋盘大小选项
        
        while True:
            self.screen.fill(BLACK)
  
            button_choose_size = self.draw_button("Choose board size", SCREEN_WIDTH // 2 - 1.5 * BUTTON_WIDTH // 2, 150, width=1.5 * BUTTON_WIDTH, update=False)
            
            if display_options:
                # 绘制大小选项按钮
                for index, option in enumerate(size_options):
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
                        for index, option in enumerate(size_options):
                            button_option = self.draw_button(option, SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 220 + (index * (OPTION_HEIGHT + 5)), update=False)
                            if button_option.collidepoint(mouse_pos):
                                return int(option)

    def show_winner(self, winner: str):
        """
        显示获胜者信息，并提供重新开始和退出选项。
        :param winner: 获胜方的名称 ("BLACK" 或 "WHITE")，平局时为 None
        """
        self.screen.fill(BLACK)
        self.display_message(f"{winner.upper()} win! Press ENTER to continue." if winner else "Draw!")  # 显示获胜信息

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

    def display_chessboard(self, chessboard: Chessboard, turn: str):
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
                    
        self.display_right_sidebar(turn)

    def display_right_sidebar(self):
        """
        绘制右侧操作面板（具体实现由子类提供）。
        """
        pass
        
    def admit_defeat(self, mouse_pos: tuple[int, int]):
        """
        检查是否点击了认输按钮。
        :param mouse_pos: 鼠标点击位置
        :return: 是否点击了认输按钮
        """
        return self.button_admit_defeat.collidepoint(mouse_pos)
    
    def restart(self, mouse_pos: tuple[int, int]):
        return self.button_restart.collidepoint(mouse_pos)
    
    def undo(self, mouse_pos: tuple[int, int]):
        return self.button_undo.collidepoint(mouse_pos)
    
    def skip(self, mouse_pos: tuple[int, int]):
        print("skip!")
        return self.button_skip.collidepoint(mouse_pos)
                    
# 具体产品（五子棋UI）
class GomokuUI(UITemplate):
    """
    五子棋用户界面类，继承自 UITemplate。
    提供五子棋特有的右侧操作面板布局。
    """
    def __init__(self) -> None:
        super().__init__()
        
    def display_right_sidebar(self, turn):
        """
        绘制右侧操作面板，包含当前玩家的轮次信息和操作按钮。
        :param turn: 当前玩家的颜色 ("BLACK" 或 "WHITE")
        """
        # 显示当前玩家轮次信息
        message_turn = self.display_message(
            f"{turn}'s Turn.", 
            left=COMMON_BUTTON_LEFT, 
            top=GRID_SIZE, 
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
            "undo", 
            COMMON_BUTTON_LEFT, 
            GRID_SIZE + 3 * BUTTON_INTERVAL, 
            update=False
        )
                
        # 更新屏幕显示
        pygame.display.flip()
        
    def skip(self, mouse_pos: tuple[int, int]):
        """
        检查是否点击了 "跳过" 按钮（五子棋没有此功能，始终返回 False）。
        :param mouse_pos: 鼠标点击位置
        :return: False（五子棋无跳过操作）
        """
        return False
        
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
        
    def display_right_sidebar(self, turn):
        """
        绘制右侧操作面板，包含当前玩家的轮次信息和操作按钮。
        :param turn: 当前玩家的颜色 ("BLACK" 或 "WHITE")
        """
        # 显示当前玩家轮次信息
        message_turn = self.display_message(
            f"{turn}'s Turn.",
            left=COMMON_BUTTON_LEFT,
            top=GRID_SIZE,
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
            "undo",
            COMMON_BUTTON_LEFT,
            GRID_SIZE + 3 * BUTTON_INTERVAL,
            update=False
        )
        
        # 绘制 "跳过" 按钮
        self.button_skip = self.draw_button(
            "skip",
            COMMON_BUTTON_LEFT,
            GRID_SIZE + 4 * BUTTON_INTERVAL,
            update=False
        )
                
        # 更新屏幕显示
        pygame.display.flip()
        