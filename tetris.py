from Logic.Game import GuiField
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QDesktopWidget
import sys
import argparse


class GameStart():

    def __init__(self, zig_zag):
        super().__init__()
        self.Game = GuiField(None, zig_zag)
        self.Game.show()


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-z', '--zigzag', required=False,
                        action='store_const', const=True,
                        help='This argument activates zigzag mode')
    namespace = parser.parse_args(args)

    zigzag = False
    if namespace.zigzag:
        zigzag = True

    a = QApplication([])
    game = GameStart(zigzag)
    game.Game.start_game()
    sys.exit(a.exec_())


if __name__ == '__main__':
    main(sys.argv[1:])
