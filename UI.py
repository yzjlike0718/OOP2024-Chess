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
        
        self.screen = pygame.display.set_mode((1100, 820))
        self.screen_width, self.screen_height = self.screen.get_width(), self.screen.get_height()
        pygame.display.set_caption("Chess Game Platform")
        self.background_image = pygame.transform.scale(pygame.image.load("pics/backgroud.jpeg"), (self.screen_width, self.screen_height))

        self.button_choose_size = None
    
    def draw_button(self, text, left, top, width, height, bg_color=WHITE, text_color=BLACK, update=True):
        button = pygame.Rect(left, top, width, height)
        pygame.draw.rect(self.screen, bg_color, button)
        text_rendered = self.FONT.render(text, True, text_color)
        self.screen.blit(text_rendered, (left + (width - text_rendered.get_width()) // 2, top + (height - text_rendered.get_height()) // 2))
        
        if update:
            pygame.display.flip()
        
        return button
    
    
    def display_message(self, text, color=RED):
        message = self.FONT.render(text, True, color)
        self.screen.blit(message, (self.screen_width // 2 - message.get_width() // 2, self.screen_height // 3))


    def choose_game(self):
        self.display_message("Choose a Game")
        
        while True:
            self.button_gomoku = self.draw_button("Gomoku", self.screen_width // 2 - BUTTON_WIDTH // 2, 330, BUTTON_WIDTH, BUTTON_HEIGHT)
            self.button_go = self.draw_button("Go", self.screen_width // 2 - BUTTON_WIDTH // 2, 400, BUTTON_WIDTH, BUTTON_HEIGHT)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.button_gomoku.collidepoint(mouse_pos):
                        return "Gomoku"
                    elif self.button_go.collidepoint(mouse_pos):
                        return "Go"
                    
    def choose_board_size(self):
        self.button_choose_size = self.draw_button("Choose board size", self.screen_width // 2 - BUTTON_WIDTH // 2, 150, BUTTON_WIDTH, BUTTON_HEIGHT, bg_color=BLACK, text_color=WHITE)
        display_options = False
        size_options = [str(i) for i in range(8, 20)]
        
        while True:
            self.screen.fill(BLACK)
  
            self.button_choose_size = self.draw_button("Choose board size", self.screen_width // 2 - 1.5 * BUTTON_WIDTH // 2, 150, 1.5 * BUTTON_WIDTH, BUTTON_HEIGHT, update=False)
            
            if display_options:
                for index, option in enumerate(size_options):
                    self.draw_button(option, self.screen_width // 2 - BUTTON_WIDTH // 2, 220 + (index * (OPTION_HEIGHT + 5)), BUTTON_WIDTH, OPTION_HEIGHT, update=False)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if self.button_choose_size.collidepoint(mouse_pos):
                        display_options = not display_options
                        
                    if display_options:
                        for index, option in enumerate(size_options):
                            button_option = self.draw_button(option, self.screen_width // 2 - BUTTON_WIDTH // 2, 220 + (index * (OPTION_HEIGHT + 5)), BUTTON_WIDTH, OPTION_HEIGHT, update=False)
                            if button_option.collidepoint(mouse_pos):
                                return int(option)
                            
    def show_winner(self, winner: str):
        self.screen.fill(BLACK)
        self.display_message(f"{winner.upper()} win! Press ENTER to continue." if winner else "Draw!") # 输入 Enter 键继续游戏

        button_new_game = button_end_game = None
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
                if event.type == pygame.KEYDOWN:
                    # 检测 Enter 键
                    if event.key == pygame.K_RETURN:
                        button_new_game = self.draw_button("New Game", self.screen_width // 2 - BUTTON_WIDTH // 2, 400, BUTTON_WIDTH, BUTTON_HEIGHT, WHITE)
                        button_end_game = self.draw_button("Exit", self.screen_width // 2 - BUTTON_WIDTH // 2, 470, BUTTON_WIDTH, BUTTON_HEIGHT, WHITE)
                        
                        # pygame.display.flip()
                
                if button_new_game is not None and button_end_game is not None:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()

                        if button_new_game.collidepoint(mouse_pos):
                            button_new_game_disabled = self.draw_button("", self.screen_width // 2 - BUTTON_WIDTH // 2, 400, BUTTON_WIDTH, BUTTON_HEIGHT, BLACK)
                            button_end_game_disabled = self.draw_button("", self.screen_width // 2 - BUTTON_WIDTH // 2, 470, BUTTON_WIDTH, BUTTON_HEIGHT, BLACK)
                            massage_disabled = self.display_message(f"{winner.upper()} win! Press ENTER to continue." if winner else "Draw!", color=BLACK)
                            return 
                        elif button_end_game.collidepoint(mouse_pos):
                            pygame.quit()
                            exit()
            pygame.display.flip()      
                
    def display_chessboard(self, chessboard: Chessboard):
        self.screen.blit(self.background_image, (0, 0))

        for row in range(1, chessboard.get_size() + 1):
            pygame.draw.line(self.screen, BLACK, (GRID_SIZE, GRID_SIZE * row),
                            (GRID_SIZE * chessboard.get_size(), GRID_SIZE * row), LINE_WIDTH)
            pygame.draw.line(self.screen, BLACK, (GRID_SIZE * row, GRID_SIZE),
                            (GRID_SIZE * row, GRID_SIZE * chessboard.get_size()), LINE_WIDTH)

        for row in range(chessboard.get_size()):
            for col in range(chessboard.get_size()):
                curr_chess = chessboard.get_chess(row=row, col=col)
                if curr_chess == "BALCK":
                    pygame.draw.circle(self.screen, BLACK, (GRID_SIZE * (col + 1), GRID_SIZE * (row + 1)), CHESS_RADIUS)
                elif curr_chess == "WHITE":
                    pygame.draw.circle(self.screen, WHITE, (GRID_SIZE * (col + 1), GRID_SIZE * (row + 1)), CHESS_RADIUS)
                
        pygame.display.flip()
                    
    # @abstractmethod
    # def detect_event(self):
    #     pass
    

# 具体产品（五子棋UI）
class GomokuUI(UITemplate):
    def __init__(self) -> None:
        super().__init__()
    

# 具体产品（围棋UI）
class GoUI(UITemplate):
    def __init__(self) -> None:
        super().__init__()
        