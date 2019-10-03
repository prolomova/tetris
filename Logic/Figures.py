import random


class FigureBase:
    BLOCKS = [[]]

    @staticmethod
    def rotate_right(BLOCKS):
        for i in range(4):
            for j in range(i):
                BLOCKS[i][j], BLOCKS[j][i] = BLOCKS[j][i], BLOCKS[i][j]

        for i in range(len(BLOCKS)):
            BLOCKS[i].reverse()
        return BLOCKS

    @staticmethod
    def get_random():
        figures = FigureBase.__subclasses__()
        for i in figures:
            for figure in i.__subclasses__():
                figures.append(figure)
        return random.choice(figures)


class SquareFigure(FigureBase):
    BLOCKS = [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]]


class LineFigure(FigureBase):
    BLOCKS = [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0]]


class TFigure(FigureBase):
    BLOCKS = [
        [0, 0, 0, 0],
        [1, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0]]


class ZFigure(FigureBase):
    BLOCKS = [
        [0, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]]


class SFigure(FigureBase):
    BLOCKS = [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0]]


class JFigure(FigureBase):
    BLOCKS = [
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]]


class LFigure(FigureBase):
    BLOCKS = [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]]
