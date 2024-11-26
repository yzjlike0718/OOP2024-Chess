from commons import GRID_SIZE
import unittest
import asyncio
import pygame
from client import Client

class TestGomokuGame(unittest.TestCase):
    async def simulate_moves(self, client, moves):
        """异步模拟棋子落子"""
        for row, col, color in moves:
            x = col * GRID_SIZE + GRID_SIZE
            y = row * GRID_SIZE + GRID_SIZE
            event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (x, y), 'button': 1})
            pygame.event.post(event)
            await asyncio.sleep(0.1)

    async def test_black_diagonal_win(self):
        """异步测试黑棋斜线获胜"""
        client = Client()
        client.play_game()

        # 模拟棋局（黑棋斜线五连）
        moves = [
            (7, 7, "BLACK"), (6, 7, "WHITE"),
            (8, 8, "BLACK"), (6, 8, "WHITE"),
            (9, 9, "BLACK"), (6, 9, "WHITE"),
            (10, 10, "BLACK"), (6, 10, "WHITE"),
            (11, 11, "BLACK")  # 黑棋完成斜线五连
        ]
        await self.simulate_moves(client, moves)

        # 检查胜利条件
        self.assertEqual(client.winner, "BLACK")

    async def test_white_horizontal_win(self):
        """异步测试白棋水平获胜"""
        client = Client()
        client.play_game()

        # 模拟棋局（白棋水平五连）
        moves = [
            (5, 5, "BLACK"), (6, 5, "WHITE"),
            (5, 6, "BLACK"), (6, 6, "WHITE"),
            (5, 7, "BLACK"), (6, 7, "WHITE"),
            (5, 8, "BLACK"), (6, 8, "WHITE"),
            (5, 9, "BLACK"), (6, 9, "WHITE")  # 白棋完成水平五连
        ]
        await self.simulate_moves(client, moves)

        # 检查胜利条件
        self.assertEqual(client.winner, "WHITE")

    async def test_draw(self):
        """异步测试平局"""
        client = Client()
        client.play_game()

        # 模拟棋局（填满棋盘，无五连胜）
        moves = [
            # 填充棋盘前两行
            *[(0, col, "BLACK" if col % 2 == 0 else "WHITE") for col in range(15)],
            *[(1, col, "WHITE" if col % 2 == 0 else "BLACK") for col in range(15)],
            # 填充棋盘剩余部分
            *[(row, col, "BLACK" if (row + col) % 2 == 0 else "WHITE") for row in range(2, 15) for col in range(15)]
        ]
        await self.simulate_moves(client, moves)

        # 检查平局条件
        self.assertIsNone(client.winner)

if __name__ == "__main__":
    pygame.init()
    asyncio.run(unittest.main())
