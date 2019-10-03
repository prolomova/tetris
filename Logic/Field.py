import random
from Logic.Figures import FigureBase
from copy import deepcopy


class Logic:
    HEIGHT = 20
    WIDTH = 9
    BLOCK_SIZE = 4

    def __init__(self, color_number, zig_zag=False):
        self.zig_zag = zig_zag
        self.color_number = color_number
        self.current_figure = FigureBase.get_random()()
        self.next_figure = FigureBase.get_random()()
        self.BLOCKS = deepcopy(self.current_figure.BLOCKS)
        self.top_left_corner_cord = (0, 0)
        self.board = []
        self.next_color = self.get_random_color()
        for _ in range(self.HEIGHT + self.BLOCK_SIZE):
            self.board.append([0] * self.WIDTH)
        self.set_figure()
        self.is_started = True
        self.score = 0
        if self.zig_zag:
            self.start_zig_zag()

    def start_zig_zag(self):
        for i in range(0, 10, 2):
            self.board[-1][i] = -1
        for i in range(2, 21):
            if i % 2 == 1:
                self.board[-i][0] = -1
            else:
                self.board[-i][-1] = -1

    def fall(self):
        while self.is_free():
            self.move()

    def get_random_color(self):
        return random.randint(1, self.color_number)

    def rotate_right(self):
        old_blocks = deepcopy(self.BLOCKS)
        x = self.top_left_corner_cord[1]
        y = self.top_left_corner_cord[0]
        new_blocks = self.current_figure.rotate_right(deepcopy(self.BLOCKS))
        color = 0
        for i in range(self.BLOCK_SIZE):
            for j in range(self.BLOCK_SIZE):
                if self.BLOCKS[i][j]:
                    if i + self.top_left_corner_cord[1] < 0 \
                            or j + self.top_left_corner_cord[0] < 0:
                        continue
                    color = self.board[x + i][y + j]
                    self.board[x + i][y + j] = 0

        self.BLOCKS = deepcopy(new_blocks)
        if not self.in_boundaries():
            self.BLOCKS = deepcopy(old_blocks)
        for i in range(self.BLOCK_SIZE):
            for j in range(self.BLOCK_SIZE):
                if self.BLOCKS[i][j]:
                    if i + self.top_left_corner_cord[1] < 0 \
                            or j + self.top_left_corner_cord[0] < 0:
                        continue
                    self.board[x + i][y + j] = color

    def in_boundaries(self):
        x = self.top_left_corner_cord[1]
        y = self.top_left_corner_cord[0]
        for i in range(self.BLOCK_SIZE):
            for j in range(self.BLOCK_SIZE):
                if self.BLOCKS[i][j]:
                    if y + j <= -1 or y + j >= self.WIDTH:
                        return False
                    if x + i <= -1:
                        return False
                    if x + i >= self.BLOCK_SIZE + self.HEIGHT or \
                            self.board[x + i][y + j] != 0:
                        return False
        return True

    def set_figure(self):
        self.top_left_corner_cord = (self.WIDTH // 2 - 1, 0)
        x = self.top_left_corner_cord[0]
        y = self.top_left_corner_cord[1]
        color = self.next_color
        self.next_color = self.get_random_color()
        self.BLOCKS = self.current_figure.BLOCKS
        for i in range(self.BLOCK_SIZE):
            for j in range(self.BLOCK_SIZE):
                if self.BLOCKS[i][j]:
                    if i + y < 0 \
                            or j + x < 0:
                        continue
                    if self.board[i + y][j + x] != 0:
                        self.is_started = False
                    self.board[i + y][j + x] = color

    def is_free(self):
        x = self.top_left_corner_cord[1]
        y = self.top_left_corner_cord[0]
        for i in range(self.BLOCK_SIZE):
            for j in range(self.BLOCK_SIZE):
                if self.BLOCKS[i][j] and (i == self.BLOCK_SIZE - 1
                                          or self.BLOCKS[i + 1][j] == 0):
                    if i + self.top_left_corner_cord[1] < 0 \
                            or j + self.top_left_corner_cord[0] < 0:
                        continue
                    if x + i + 1 >= self.BLOCK_SIZE + self.HEIGHT \
                            or self.board[x + i + 1][y + j] != 0:
                        return False
        return True

    def move(self):
        x = self.top_left_corner_cord[1]
        y = self.top_left_corner_cord[0]
        color = 0
        for i in range(self.BLOCK_SIZE):
            for j in range(self.BLOCK_SIZE):
                if self.BLOCKS[i][j]:
                    if i + self.top_left_corner_cord[1] < 0 \
                            or j + self.top_left_corner_cord[0] < 0:
                        continue
                    color = self.board[x + i][y + j]
                    self.board[x + i][y + j] = 0
        x += 1
        for i in range(self.BLOCK_SIZE):
            for j in range(self.BLOCK_SIZE):
                if self.BLOCKS[i][j]:
                    if i + self.top_left_corner_cord[1] < 0 \
                            or j + self.top_left_corner_cord[0] < 0:
                        continue
                    self.board[x + i][y + j] = color
        self.top_left_corner_cord = (y, x)

    def find_full_lines(self):
        full_lines = []
        for i in range(len(self.board) - 1, -1, -1):
            if 0 not in self.board[i]:
                full_lines.append(i)
        return full_lines

    def delete_lines(self, lines):
        self.score += len(lines) * (self.score // 5 + 1)
        for line in sorted(lines):
            self.board.pop(line)
            self.board.insert(0, [0] * self.WIDTH)

    def delete_zigzag_lines(self, lines):
        self.score += len(lines) * (self.score // 5 + 1)
        for line in sorted(lines):
            for i in range(len(self.board[line])):
                if self.board[line][i] != -1:
                    self.board[line][i] = 0
        for full_line in sorted(lines):
            if full_line != self.HEIGHT + self.BLOCK_SIZE - 1:
                for line in range(full_line, 0, -1):
                    for i in range(1, 8):
                        t = self.board[line][i]
                        self.board[line][i] = self.board[line - 1][i]
                        self.board[line - 1][i] = t
            else:
                for line in range(full_line, 0, -1):
                    for i in range(1, 9, 2):
                        t = self.board[line][i]
                        self.board[line][i] = self.board[line - 1][i]
                        self.board[line - 1][i] = t

    def set_next_figure(self):
        self.current_figure, self.next_figure = \
            self.next_figure, FigureBase.get_random()()
        self.top_left_corner_cord = (0, 0)
        self.set_figure()

    def shift_left(self):
        if not self.is_left_free():
            return
        x = self.top_left_corner_cord[1]
        y = self.top_left_corner_cord[0]
        for i in range(self.BLOCK_SIZE):
            for j in range(self.BLOCK_SIZE):
                if self.BLOCKS[i][j]:
                    if i + self.top_left_corner_cord[1] < 0 \
                            or j + self.top_left_corner_cord[0] < 0:
                        continue
                    self.board[x + i][y + j], \
                        self.board[x + i][y + j - 1] = \
                        self.board[x + i][y + j - 1], \
                        self.board[x + i][y + j]
        self.top_left_corner_cord = (y - 1, x)

    def is_left_free(self):
        x = self.top_left_corner_cord[1]
        y = self.top_left_corner_cord[0]
        for i in range(self.BLOCK_SIZE):
            for j in range(self.BLOCK_SIZE):
                if self.BLOCKS[i][j]:
                    if i + self.top_left_corner_cord[1] < 0 \
                            or j + self.top_left_corner_cord[0] < 0:
                        continue
                    if y + j - 1 <= -1:
                        return False
                    if (j == 0 or self.BLOCKS[i][j - 1] == 0) \
                            and self.board[x + i][y + j - 1] != 0:
                        return False
                    continue
        return True

    def is_right_free(self):
        x = self.top_left_corner_cord[1]
        y = self.top_left_corner_cord[0]
        for i in range(self.BLOCK_SIZE):
            for j in range(self.BLOCK_SIZE - 1, -1, -1):
                if self.BLOCKS[i][j]:
                    if i + self.top_left_corner_cord[1] < 0 \
                            or j + self.top_left_corner_cord[0] < 0:
                        continue
                    if y + j + 1 >= self.WIDTH:
                        return False
                    if (j == self.BLOCK_SIZE - 1
                        or self.BLOCKS[i][j + 1] == 0) \
                            and self.board[x + i][y + j + 1] != 0:
                        return False
                    continue
        return True

    def shift_right(self):
        if not self.is_right_free():
            return
        x = self.top_left_corner_cord[1]
        y = self.top_left_corner_cord[0]
        for i in range(self.BLOCK_SIZE):
            for j in range(self.BLOCK_SIZE - 1, -1, -1):
                if self.BLOCKS[i][j]:
                    if i + self.top_left_corner_cord[1] < 0 \
                            or j + self.top_left_corner_cord[0] < 0:
                        continue
                    self.board[x + i][y + j], \
                        self.board[x + i][y + j + 1] = \
                        self.board[x + i][y + j + 1], \
                        self.board[x + i][y + j]
        self.top_left_corner_cord = (y + 1, x)
