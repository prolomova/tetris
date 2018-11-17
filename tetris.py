#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import random
import PyQt5
from PyQt5 import QtWidgets


class Cube():
    colorTable = [0x228800, 0x66CC00, 0x7788BB, 0x9977AA,
                  0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00,
                  0xBB0000, 0x99CCDD, 0x00DDFF, 0x77FF00,
                  0xFF0000, 0x00FF00, 0x0000FF, 0x114466]
    figure_quantity = 7
    coordinatesTable = {
        "empty": ((0, 0), (0, 0), (0, 0), (0, 0)),
        "line": ((0, -1), (0, 0), (0, 1), (0, 2)),
        "t": ((-1, 0), (0, 0), (1, 0), (0, 1)),
        "square": ((0, 0), (1, 0), (0, 1), (1, 1)),
        "l": ((-1, -1), (0, -1), (0, 0), (0, 1)),
        "z": ((0, -1), (0, 0), (-1, 0), (-1, 1)),
        "s": ((0, -1), (0, 0), (1, 0), (1, 1)),
        "j": ((1, -1), (0, -1), (0, 0), (0, 1))}

    def __init__(self):
        self.next_figure = "empty"
        self.current_figure = "empty"
        self.coordinates = [[0, 0], [0, 0], [0, 0], [0, 0]]
        self.color = 0x000000

    def copy(self):
        rotated = Cube()
        rotated.color = self.color
        rotated.current_figure = self.current_figure
        for i in range(4):
            rotated.set_x(i, self.coordinates[i][0])
            rotated.set_y(i, self.coordinates[i][1])
        return rotated

    def rotate_left(self):
        rotated = self.copy()
        for i in range(4):
            t = rotated.coordinates[i][0]
            rotated.set_x(i, -rotated.coordinates[i][1])
            rotated.set_y(i, t)
        return rotated

    def rotate_right(self):
        rotated = self.copy()
        for i in range(4):
            t = rotated.coordinates[i][0]
            rotated.set_x(i, rotated.coordinates[i][1])
            rotated.set_y(i, -t)
        return rotated

    def set_random_color(self):
        self.color = PyQt5.QtGui.QColor(
            self.colorTable[random.randint(0, 6)])

    def set_color(self, color):
        self.color = PyQt5.QtGui.QColor(color)

    def set_figure(self, figure):
        self.current_figure = figure
        self.coordinates = Cube.coordinatesTable[figure]

    def set_random_figure(self):
        figures = ["t", "line", "square", "l", "j", "s", "z"]
        self.current_figure = random.choice(figures)
        self.coordinates = Cube.coordinatesTable[self.current_figure]

    def set_x(self, i, x):
        self.coordinates[i][0] = x

    def set_y(self, i, y):
        self.coordinates[i][1] = y


class Game(PyQt5.QtWidgets.QMainWindow):

    def __init__(self, width, height):
        super().__init__()
        self.GuiField = GuiField(width, height)
        self.setCentralWidget(self.GuiField)
        self.resize(720, 1280)
        self.show()


class Cell():
    def __init__(self, figure, color):
        self.color = color
        self.figure = figure


class GuiField(PyQt5.QtWidgets.QFrame):
    pause = 500
    is_started = False

    def __init__(self, width, height):
        super().__init__()
        self.height = height
        self.width = width
        self.board = []
        self.set_empty()
        self.timer = PyQt5.QtCore.QBasicTimer()
        self.is_fallen = True
        self.coordinates = (0, 0)
        self.score = 0
        self.setFocusPolicy(PyQt5.QtCore.Qt.StrongFocus)

    def set_empty(self):
        for i in range(self.height):
            self.board.append([])
            for j in range(self.width):
                self.board[i].append(Cell("empty", 0x000000))
                    
    def start_game(self):
        self.is_started = True
        self.set_empty()
        self.get_next_cube()
        self.timer.start(GuiField.pause, self)
        
    def get_next_cube(self):
        self.current_figure = Cube()
        self.current_figure.set_random_figure()
        self.current_figure.set_random_color()
        cube_height = self.current_figure.coordinates[0][1]
        for i in range(4):
            if cube_height > self.current_figure.coordinates[i][1]:
                cube_height = self.current_figure.coordinates[i][1]
        self.coordinates = (self.width // 2 + 1, self.height - 1 + cube_height)
        if not self.is_free(self.current_figure, self.coordinates):
            print("Score: ", self.score)
            self.timer.stop()
        else:
            self.move(self.current_figure, self.coordinates)

    def get_color(self, x, y):
        return self.board[x][y].color

    def set_color(self, x, y, color):
        self.board[x][y].color = color

    def get_figure(self, x, y):
        return self.board[x][y].figure

    def set_figure(self, x, y, figure):
        self.board[x][y].figure = figure

    def move_line(self, painter, content, top):
        width_coeff = 720 // self.width
        height_coeff = 1280 // self.height
        for i in range(4):
            x = content.left() + \
                (self.coordinates[0] + self.current_figure.coordinates[i][0]) * \
                width_coeff
            y = top + (self.height -
                       (self.coordinates[1] - self.current_figure.coordinates[i][1]) - 1) * \
                height_coeff
            color = self.current_figure.color
            painter.fillRect(x, y,
                             width_coeff - 10,
                             height_coeff - 10,
                             color)

    def paintEvent(self, event):
        painter = PyQt5.QtGui.QPainter(self)
        width_coeff = 720 // self.width
        height_coeff = 1280 // self.height
        top = self.contentsRect().bottom() - self.contentsRect().height()
        for i in range(self.height):
            for j in range(self.width):
                x = self.contentsRect().left() + j * width_coeff
                y = top + i * height_coeff
                color = self.get_color(j, self.height - (i + 1))
                painter.fillRect(x, y,
                                 width_coeff - 10,
                                 height_coeff - 10, color)
        self.move_line(painter, self.contentsRect(), top)
        
    def mousePressEvent(self, event):
        if not self.is_started or self.current_figure.current_figure == "empty":
            return
        if event.button() == PyQt5.QtCore.Qt.RightButton:
            if self.is_free(self.current_figure.rotate_right(), self.coordinates):
                self.move(self.current_figure.rotate_right(), self.coordinates)
        elif event.button() == PyQt5.QtCore.Qt.LeftButton:
            if self.is_free(self.current_figure.rotate_left(), self.coordinates):
                self.move(self.current_figure.rotate_left(), self.coordinates)

    def keyPressEvent(self, event):
        if not self.is_started or self.current_figure.current_figure == "empty":
            return
        key = event.key()
        if key == PyQt5.QtCore.Qt.Key_Left:
            if self.is_free(self.current_figure,
                            (self.coordinates[0] - 1, self.coordinates[1])):
                self.move(self.current_figure,
                            (self.coordinates[0] - 1, self.coordinates[1]))
        elif key == PyQt5.QtCore.Qt.Key_Right:
            if self.is_free(self.current_figure,
                         (self.coordinates[0] + 1, self.coordinates[1])):
                self.move(self.current_figure,
                         (self.coordinates[0] + 1, self.coordinates[1]))

    def timerEvent(self, event):
        if self.is_fallen:
            if not self.is_free(self.current_figure,
                                (self.coordinates[0],
                                 self.coordinates[1] - 1)):
                self.fall_figure()
            else:
                self.move(self.current_figure,
                          (self.coordinates[0],
                           self.coordinates[1] - 1))
        else:
            self.is_fallen = True
            self.get_next_cube()

    def fall_figure(self):
        for i in range(4):
            x = self.coordinates[0] + self.current_figure.coordinates[i][0]
            y = self.coordinates[1] - self.current_figure.coordinates[i][1]
            self.set_figure(x, y, self.current_figure.current_figure)
            self.set_color(x, y, self.current_figure.color)
        self.delete_full_lines(self.find_full_lines())
        if self.is_fallen:
            self.get_next_cube()

    def find_full_lines(self):
        full_lines = []
        for i in range(self.height):
            occupied = 0
            for j in range(self.width):
                if not self.get_figure(j, i) == "empty":
                    occupied += 1
            if occupied == self.width:
                full_lines.append(i)
        full_lines.reverse()
        return full_lines

    def delete_full_lines(self, full_lines):
        full_lines_count = len(full_lines)
        for line in full_lines:
            for i in range(line, self.height - 1):
                for j in range(self.width):
                    self.set_figure(j, i, self.get_figure(j, i + 1))
                    self.set_color(j, i, self.get_color(j, i + 1))
        self.score += full_lines_count

    def move(self, next_cube, coordinates):
        self.current_figure = next_cube
        self.coordinates = coordinates
        self.update()

    def is_free(self, next_cube, coordinates):
        for i in range(4):
            x = coordinates[0] + next_cube.coordinates[i][0]
            y = coordinates[1] - next_cube.coordinates[i][1]
            if x < 0 or x >= self.width \
                    or y < 0 or y >= self.height \
                    or self.get_figure(x, y) != "empty":
                return False
        return True


WIDTH = 10
HEIGHT = 20


def main():
    a = PyQt5.QtWidgets.QApplication([])
    game = Game(WIDTH, HEIGHT)
    game.GuiField.start_game()
    sys.exit(a.exec_())


if __name__ == '__main__':
    main()
