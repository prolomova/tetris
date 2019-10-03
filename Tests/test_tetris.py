#!/usr/bin/env python3

import unittest
from copy import deepcopy
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

import Logic.Field as b
from Logic.Figures import FigureBase, SquareFigure


class Test(unittest.TestCase):

    def test_move(self):
        logic = b.Logic(4)
        for i in range(9):
            logic.move()
        for i in range(9):
            self.assertEqual(logic.board[i], [0] * 9)
        for i in range(14, 20):
            self.assertEqual(logic.board[i], [0] * 9)
        _sum = 0
        for i in range(9, 14):
            _sum += sum(logic.board[i])

        self.assertEqual(_sum != 0, True)

    def test_is_free(self):
        logic = b.Logic(4)
        for i in range(20):
            for j in range(9):
                logic.board[i][j] = 1
        self.assertEqual(logic.is_free(), False)

    def test_rotate_right(self):
        BLOCKS = [
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0]]

        self.assertEqual(FigureBase.rotate_right(BLOCKS), [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]])

    def test_find_full_lines(self):
        logic = b.Logic(4)
        for i in range(9):
            for j in range(9):
                logic.board[i][j] = 1
        self.assertEqual(set(logic.find_full_lines()), set(range(9)))

    def test_delete_full_lines(self):
        logic = b.Logic(4)
        for i in range(9):
            for j in range(9):
                logic.board[i][j] = 1
        logic.delete_lines(logic.find_full_lines())
        board = []
        for i in range(24):
            board.append(9 * [0])
        self.assertEqual(board, logic.board)

    def test_shift_right(self):
        logic = b.Logic(4)
        new_board = []
        for i in range(24):
            new_board.append([])
            for j in range(9):
                new_board[i] = deepcopy(logic.board[i])
                new_board[i].pop()
                new_board[i].insert(0, 0)
        logic.shift_right()
        self.assertEqual(new_board, logic.board)

    def test_shift_left(self):
        logic = b.Logic(4)
        new_board = []
        for i in range(24):
            new_board.append([])
            for j in range(9):
                new_board[i] = deepcopy(logic.board[i])
                new_board[i].pop(0)
                new_board[i].append(0)
        logic.shift_left()
        self.assertEqual(new_board, logic.board)

    def test_set_figure(self):
        logic = b.Logic(4)
        new_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 1, 0, 0, 0],
                     [0, 0, 0, 0, 1, 1, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        for i in range(20):
            new_board.append([0] * 9)

        logic.board = deepcopy(new_board)
        logic.next_figure = SquareFigure()
        logic.current_figure = SquareFigure()
        logic.next_color = 1
        logic.set_figure()
        self.assertEqual(new_board, logic.board)

    def test_zigzag(self):
        logic = b.Logic(1, True)
        for i in range(4, len(logic.board) - 2):
            self.assertEqual(logic.board[i][0], logic.board[i + 1][-1])

    def test_move_zigzag(self):
        logic = b.Logic(1, True)
        for i in range(len(logic.board[9]) - 3):
            if logic.board[9][i] != -1:
                logic.board[9][i] = 1
        board = deepcopy(logic.board)

        for i in range(len(logic.board[10])):
            if logic.board[10][i] != -1:
                logic.board[10][i] = 1
        for i in range(len(board[9])):
            if board[9][i] == 1:
                board[10][i] = 1
                board[9][i] = 0
        logic.delete_zigzag_lines([10])
        self.assertEqual(board[5:], logic.board[5:])

    def test_move_zigzag_last_line(self):
        logic = b.Logic(1, True)
        for i in range(len(logic.board[-1])):
            if logic.board[-1][i] != -1:
                logic.board[-1][i] = 1
        board = deepcopy(logic.board)

        for i in range(len(board[-1])):
            if board[-1][i] == 1:
                board[-1][i] = 0
        logic.delete_zigzag_lines([-1])
        self.assertEqual(board[4:], logic.board[4:])


if __name__ == '__main__':
    unittest.main()
