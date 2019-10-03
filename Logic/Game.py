from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QPushButton, QDialog
import PyQt5
import PyQt5.QtCore
from PyQt5.QtCore import QBasicTimer
from Logic.Field import Logic
from copy import deepcopy
from Logic.scoreTable import NameRequest, ScoresTable, ResultPainter


class GuiField(QMainWindow):
    BACKGROUND = 0xFFFFFF
    COLOR_TABLE = [0x0000FF, 0x00FF00,
                   0xFF0000, 0xFFDD00,
                   0xFF00FF, 0x00FFFF]
    INIT_PAUSE = 400
    PAUSE = 400
    WIDTH = 9
    HEIGHT = 20

    def __init__(self, name=None, zig_zag=False):
        super().__init__()

        self.name = name

        q = QDesktopWidget().availableGeometry()
        self.cell_size = min(q.width() // self.WIDTH,
                             q.height() // (2 + self.HEIGHT))
        self.resize((self.WIDTH + 10) * self.cell_size, q.height())
        self.next_game_mode = zig_zag
        self.init_game()

        self.pause_btn = QPushButton('PAUSE', self)
        self.pause_btn.move(self.cell_size * (2 + self.WIDTH),
                            9 * self.cell_size)
        self.pause_btn.resize(2 * self.cell_size, 2 * self.cell_size)
        self.pause_btn.clicked.connect(self.pause)
        self.pause_btn.setToolTip('<b>Ctrl+P</b>')

        self.new_game_btn = QPushButton('NEW\nGAME', self)
        self.new_game_btn.move(self.cell_size * (2 + self.WIDTH),
                               11 * self.cell_size)
        self.new_game_btn.resize(2 * self.cell_size, 2 * self.cell_size)
        self.new_game_btn.clicked.connect(self.new_game)
        self.new_game_btn.setToolTip('<b>Ctrl+N</b>')

        self.game_mode_btn = QPushButton('ZIGZAG\nMODE', self)
        self.game_mode_btn.move(self.cell_size * (2 + self.WIDTH),
                                13 * self.cell_size)
        self.game_mode_btn.resize(2 * self.cell_size, 2 * self.cell_size)
        self.game_mode_btn.clicked.connect(self.change_mode)
        self.game_mode_btn.setStyleSheet(
            'QPushButton {background-color: #FF0000;}')
        self.game_mode_btn.setToolTip('<b>Ctrl+Z</b>')

        self.setFocus()

        self.show()

    def init_game(self):
        self.logic = Logic(len(self.COLOR_TABLE), self.next_game_mode)

        self.is_started = False
        self.timer = QBasicTimer()
        self.setFocusPolicy(PyQt5.QtCore.Qt.StrongFocus)
        self.scores = ScoresTable()
        if self.scores.score_table is None:
            self.statusBar().showMessage('Score file is damaged')
        self.acceleration = False
        self.is_paused = False

    def change_mode(self):
        if self.next_game_mode:
            self.game_mode_btn.setStyleSheet(
                'QPushButton {background-color: #FF0000;}')
            self.next_game_mode = False
        else:
            self.game_mode_btn.setStyleSheet(
                'QPushButton {background-color: #00FF00;}')
            self.next_game_mode = True

    def paintEvent(self, event):
        painter = QPainter(self)
        for i in range(self.WIDTH):
            for j in range(4, 4 + self.HEIGHT):
                x = i * self.cell_size
                y = (j - 4) * self.cell_size
                if self.logic.board[j][i] == -1:
                    continue
                if self.logic.board[j][i] == 0:
                    painter.fillRect(x, y,
                                     self.cell_size - 5,
                                     self.cell_size - 5,
                                     QColor(self.BACKGROUND))
                else:
                    color = \
                        QColor(self.COLOR_TABLE[self.logic.board[j][i] - 1])
                    painter.fillRect(x, y,
                                     self.cell_size - 5,
                                     self.cell_size - 5,
                                     color)
        painter.setFont(QFont('Decorative', self.cell_size // 3))
        painter.drawText((2 + self.WIDTH) * self.cell_size, 2 * self.cell_size,
                         'Score: ' + str(self.logic.score))
        mode = "simple"
        if self.logic.zig_zag:
            mode = "zigzag"
        if self.scores.score_table is not None:
            painter.drawText((2 + self.WIDTH) * self.cell_size,
                             3 * self.cell_size,
                             'Best score: ' + str(
                                 self.scores.score_table[mode][0]["score"]))
        self.update()

        for i in range(4):
            for j in range(4):
                x = (i + self.WIDTH + 2) * self.cell_size
                y = (j + 4) * self.cell_size
                if self.logic.next_figure.BLOCKS[j][i]:
                    color = QColor(self.COLOR_TABLE[self.logic.next_color - 1])
                    painter.fillRect(x, y,
                                     self.cell_size - 5,
                                     self.cell_size - 5,
                                     color)
                else:
                    painter.fillRect(x, y,
                                     self.cell_size - 5,
                                     self.cell_size - 5,
                                     QColor(self.BACKGROUND))
        self.update()

    def keyPressEvent(self, event):
        key = event.key()
        if int(event.modifiers()) == (PyQt5.QtCore.Qt.ControlModifier):
            if key == PyQt5.QtCore.Qt.Key_P:
                self.pause()
            elif key == PyQt5.QtCore.Qt.Key_N:
                self.new_game()
            if not self.is_started or self.is_paused:
                return
            if key == PyQt5.QtCore.Qt.Key_Z:
                self.change_mode()
        if not self.is_started or self.is_paused:
            return
        if key == PyQt5.QtCore.Qt.Key_Left:
            self.logic.shift_left()
        elif key == PyQt5.QtCore.Qt.Key_Right:
            self.logic.shift_right()
        elif key == PyQt5.QtCore.Qt.Key_Up:
            self.logic.rotate_right()
        elif key == PyQt5.QtCore.Qt.Key_Down:
            self.acceleration = True
        elif key == PyQt5.QtCore.Qt.Key_Space:
            self.logic.fall()
        self.update()

    def keyReleaseEvent(self, event):
        if not self.is_started or self.is_paused:
            return
        key = event.key()
        if key == PyQt5.QtCore.Qt.Key_Down:
            self.acceleration = False
        self.update()

    def timerEvent(self, event):
        if not self.logic.is_started:
            if not self.logic.is_started:
                self.is_started = False
                self.timer.stop()
                self.close()
                if self.name is None and self.scores.score_table is not None:
                    self.name_request = NameRequest(deepcopy(self.scores),
                                                    self.logic.score)
                    self.name_request.show()
                    self.name_request.exec_()
                    try:
                        self.name = self.name_request.name
                    except AttributeError:
                        self.name = None
                    self.name_request.close()
                mode = "simple"
                if self.logic.zig_zag:
                    mode = "zigzag"
                if self.scores.score_table is not None \
                        and self.name is not None:
                    self.res = ResultPainter(self.name, self.scores,
                                             self.logic.score, mode)
                    self.res.show()
                return
        else:
            if self.logic.is_free():
                self.logic.move()
            else:
                if self.logic.zig_zag:
                    lines = self.logic.find_full_lines()
                    self.logic.delete_zigzag_lines(lines)
                else:
                    self.logic.delete_lines(self.logic.find_full_lines())
                self.logic.set_next_figure()
                if self.logic.score % 5 == 0:
                    level = self.logic.score // 5
                    self.PAUSE = self.INIT_PAUSE * \
                        (1 - level / 10 ** len(str(level)))
                    self.timer.stop()
                    self.timer.start(self.PAUSE, self)
            if self.acceleration:
                self.timer.stop()
                self.timer.start((self.PAUSE * 0.5) // 1, self)
            else:
                self.timer.stop()
                self.timer.start(self.PAUSE, self)
        self.update()

    def start_game(self):
        self.is_started = True
        self.timer.start(self.PAUSE, self)
        self.setFocus()

    def pause(self):
        if self.is_paused:
            self.is_paused = False
            self.timer.start(self.PAUSE, self)
            self.setFocus()
        else:
            self.is_paused = True
            self.timer.stop()

    def new_game(self):
        self.pause()
        if self.name is None and self.scores.score_table is not None:
            self.name_request = NameRequest(deepcopy(self.scores),
                                            self.logic.score)
            self.name_request.show()
            self.name_request.exec_()
            try:
                self.name = self.name_request.name
            except AttributeError:
                self.name = None
            self.name_request.close()
        mode = "simple"
        if self.logic.zig_zag:
            mode = "zigzag"
        if self.name is not None:
            ScoresTable.add(self.name, self.logic.score,
                            mode, self.scores.score_table)
        self.timer.stop()
        self.init_game()

        self.start_game()
