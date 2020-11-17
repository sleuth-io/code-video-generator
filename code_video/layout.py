from manim import config
from manim import LEFT
from manim import np
from manim import RIGHT
from manim import SMALL_BUFF


class ColumnLayout:
    """
    Helper to determine X values for a column layout
    """

    def __init__(self, columns=2, buff=SMALL_BUFF):
        self.columns = [None] * columns
        self.buff = buff
        self.left_x = config["frame_x_radius"] * -1
        self.column_width = (config["frame_x_radius"] * 2) / columns

    def get_x(self, column: int, span=1, direction=LEFT) -> float:
        """
        Gets the x value for a given column and span.

        Args:
            column: The column number, with 1 as the first column
            span: The number of columns to span
            direction: The direction of the X value, `LEFT` or `RIGHT`
        """
        col = column - 1

        x_left = self.left_x + col * self.column_width + self.buff
        x_right = self.left_x + (col + span) * self.column_width - self.buff

        if np.all(direction == LEFT):
            return x_left
        elif np.all(direction == RIGHT):
            return x_right
        else:
            raise ValueError
