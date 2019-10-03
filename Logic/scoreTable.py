from PyQt5 import QtCore
from PyQt5.QtWidgets import QDesktopWidget, QPushButton, QDialog, \
    QGridLayout, QLineEdit, QLabel
from PyQt5.QtGui import QPainter, QColor, QFont, QPalette
import yaml
from copy import deepcopy
import sys
import os
from yaml.scanner import ScannerError

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from Logic import Game


class NameRequest(QDialog):

    def __init__(self, scores, score):
        super().__init__()
        self.scores = scores
        self.score = score

        q = QDesktopWidget().availableGeometry()
        self.resize(q.width() // 4, q.height() // 8)

        grid = QGridLayout()

        self.lbl_name = QLabel("Введите ваше имя", self)
        grid.addWidget(self.lbl_name, 0, 0)
        self.name_box = QLineEdit(self)
        self.name_box.setText("player")
        grid.addWidget(self.name_box, 1, 0)
        self.button = QPushButton('OK', self)
        grid.addWidget(self.button, 2, 0)
        self.button.clicked.connect(self.on_click)

        self.setLayout(grid)
        self.show()

    def on_click(self):
        self.name = self.name_box.text()

        if self.name != "":
            self.close()


class ResultPainter(QDialog):
    def __init__(self, name, score_table, score, mode):
        super().__init__()
        self.score = score
        self.name = name
        self.mode = mode
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.score_table = score_table
        q = QDesktopWidget().availableGeometry()
        self.resize(q.width() // 2, q.height() // 2)
        ScoresTable.add(self.name, self.score, mode,
                        deepcopy(self.score_table.score_table))
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.new_game_btn = QPushButton('NEW\nGAME', self)
        self.grid.addWidget(self.new_game_btn, 0, 2)
        self.new_game_btn.clicked.connect(self.new_game)

        self.show()

    def new_game(self):
        self.close()
        self.game = Game.GuiField(self.name)
        self.game.start_game()

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.draw_results(painter)
        painter.end()

    def draw_results(self, painter):
        results = []
        first = True
        for i in range(8):
            if self.score_table.score_table[self.mode][i]["score"] \
                    <= self.score and first:
                results.append((self.name, self.score))
                first = False
            name = self.score_table.score_table[self.mode][i]["name"]
            score = self.score_table.score_table[self.mode][i]["score"]
            results.append((name, score))
        if first:
            results.append((self.name, self.score))
        main_label = QLabel("SCORE TABLE", self)
        self.grid.addWidget(main_label, 0, 0)
        main_label.setFont(QFont("Times", 18, QFont.Bold))
        i = 1
        first = True
        for name, score in results:
            if name == "":
                break
            label_name = QLabel(name, self)
            label_score = QLabel(str(score), self)
            label_name.setFont(QFont("Times", 15))
            label_score.setFont(QFont("Times", 15))
            if name == self.name and score == self.score and first:
                first = False
                label_name.setStyleSheet("QLabel { color: red}")
                label_score.setStyleSheet("QLabel { color: red}")

            self.grid.addWidget(label_name, i, 0)
            self.grid.addWidget(label_score, i, 1)
            i += 1

        self.show()


class ScoresTable:
    SCORE_TABLE_FILE_NAME = './Data/scoreTable.yaml'
    TABLE_SIZE = 8

    def __init__(self):
        try:
            with open(self.SCORE_TABLE_FILE_NAME) as f:
                self.score_table = yaml.load(f)
        except (IOError, ScannerError):
            self.score_table = {'simple': [], 'zigzag': []}
            for key in self.score_table.keys():
                for _ in range(8):
                    line = {'name': '', 'score': 0}
                    self.score_table[key].append(line)
            try:
                with open(self.SCORE_TABLE_FILE_NAME, 'w') as f:
                    yaml.dump(self.score_table, f)
            except Exception:
                self.score_table = None

    @classmethod
    def add(self, name, score, mode, score_tbl):
        for i in range(self.TABLE_SIZE):
            if score_tbl[mode][i]["score"] <= score:
                score_tbl[mode].insert(i, {"name": name, "score": score})
                score_tbl[mode] = score_tbl[mode][:8]
                break
        with open(self.SCORE_TABLE_FILE_NAME, 'w') as f:
            yaml.dump(score_tbl, f)
