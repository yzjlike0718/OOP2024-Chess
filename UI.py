from abc import ABC, abstractmethod
import pygame
import sys
from commons import *
from chessboard import *

# 抽象产品&UI模板
class UITemplate(ABC):
    
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        self.FONT = pygame.font.SysFont(None, 40)
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Chess Game Platform")
        self.background_image = pygame.transform.scale(pygame.image.load("pics/backgroud.jpeg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        
    def detect_event(self): # 检查鼠标/键盘事件
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
        button = pygame.Rect(left, top, width, height)
        pygame.draw.rect(self.screen, bg_color, button)
        text_rendered = self.FONT.render(text, True, text_color)
        self.screen.blit(text_rendered, (left + (width - text_rendered.get_width()) // 2, top + (height - text_rendered.get_height()) // 2))
        
        if update:
            pygame.display.flip()
        
        return button
    
    
    def display_message(self, text, color=RED, left=None, top=None):
        message = self.FONT.render(text, True, color)
        if left is None:
            left = SCREEN_WIDTH // 2 - message.get_width() // 2
        if top is None:
            top = SCREEN_HEIGHT // 3
        self.screen.blit(message, (left, top))


    def choose_game(self):
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
        button_choose_size = self.draw_button("Choose board size", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 150, bg_color=BLACK, text_color=WHITE)
        display_options = False
        size_options = [str(i) for i in range(8, 20)]
        
        while True:
            self.screen.fill(BLACK)
  
            button_choose_size = self.draw_button("Choose board size", SCREEN_WIDTH // 2 - 1.5 * BUTTON_WIDTH // 2, 150, width=1.5 * BUTTON_WIDTH, update=False)
            
            if display_options:
                for index, option in enumerate(size_options):
                    self.draw_button(option, SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 220 + (index * (OPTION_HEIGHT + 5)), height=OPTION_HEIGHT, update=False)
            
            pygame.display.flip()
            
            event = self.detect_event()
            if event is not None:
                event_type, event_val = event
                if event_type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event_val
                    
                    if button_choose_size.collidepoint(mouse_pos):
                        display_options = not display_options
                        
                    if display_options:
                        for index, option in enumerate(size_options):
                            button_option = self.draw_button(option, SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 220 + (index * (OPTION_HEIGHT + 5)), update=False)
                            if button_option.collidepoint(mouse_pos):
                                return int(option)
                            
    def show_winner(self, winner: str):
        self.screen.fill(BLACK)
        self.display_message(f"{winner.upper()} win! Press ENTER to continue." if winner else "Draw!") # 输入 Enter 键继续游戏

        button_new_game = button_end_game = None
        
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
        self.screen.blit(self.background_image, (0, 0))

        for row in range(1, chessboard.get_size() + 1):
            pygame.draw.line(self.screen, BLACK, (GRID_SIZE, GRID_SIZE * row),
                            (GRID_SIZE * chessboard.get_size(), GRID_SIZE * row), LINE_WIDTH)
            pygame.draw.line(self.screen, BLACK, (GRID_SIZE * row, GRID_SIZE),
                            (GRID_SIZE * row, GRID_SIZE * chessboard.get_size()), LINE_WIDTH)

        for row in range(chessboard.get_size()):
            for col in range(chessboard.get_size()):
                curr_chess = chessboard.get_chess(row=row, col=col)
                if curr_chess == "BLACK":
                    pygame.draw.circle(self.screen, BLACK, (GRID_SIZE * (col + 1), GRID_SIZE * (row + 1)), CHESS_RADIUS)
                elif curr_chess == "WHITE":
                    pygame.draw.circle(self.screen, WHITE, (GRID_SIZE * (col + 1), GRID_SIZE * (row + 1)), CHESS_RADIUS)
                    
        message_turn = self.display_message(f"{turn}'s Turn.", left=COMMON_BUTTON_LEFT, top=GRID_SIZE, color=WHITE if turn=="WHITE" else BLACK)
                    
        self.button_admit_defeat = self.draw_button("Admit Defeat", COMMON_BUTTON_LEFT, GRID_SIZE + BUTTON_INTERVAL, update=False)
        
        self.button_restart = self.draw_button("Restart", COMMON_BUTTON_LEFT, GRID_SIZE + 2 * BUTTON_INTERVAL, update=False)
        
        self.button_undo = self.draw_button("undo", COMMON_BUTTON_LEFT, GRID_SIZE + 3 * BUTTON_INTERVAL, update=False)
                
        pygame.display.flip()
        
    def admit_defeat(self, mouse_pos: tuple[int, int]):
        return self.button_admit_defeat.collidepoint(mouse_pos)
    
    def restart(self, mouse_pos: tuple[int, int]):
        return self.button_restart.collidepoint(mouse_pos)
    
    def undo(self, mouse_pos: tuple[int, int]):
        return self.button_undo.collidepoint(mouse_pos)
                    

# 具体产品（五子棋UI）
class GomokuUI(UITemplate):
    def __init__(self) -> None:
        super().__init__()
    

# 具体产品（围棋UI）
class GoUI(UITemplate):
    def __init__(self) -> None:
        super().__init__()
        