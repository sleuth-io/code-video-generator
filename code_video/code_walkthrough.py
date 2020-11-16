from tempfile import NamedTemporaryFile
from typing import List
from typing import Optional
from typing import Tuple

from attr import dataclass
from manim import Code
from manim import Polygon
from manim import Transform
from manim.animation.fading import DEFAULT_FADE_LAG_RATIO


class HighlightLines(Transform):
    CONFIG = {
        "lag_ratio": DEFAULT_FADE_LAG_RATIO,
    }

    def __init__(self, mobject, start: int = 1, end: int = -1, target_mobject=None, **kwargs):
        super().__init__(mobject, target_mobject=target_mobject, **kwargs)
        self.start_line_number = start
        self.end_line_number = end

    def create_target(self):
        target = self.mobject.copy()
        if self.end_line_number == -1:
            self.end_line_number = len(target.line_numbers) + self.mobject.line_no_from

        self.start_line_number -= self.mobject.line_no_from - 1
        self.end_line_number -= self.mobject.line_no_from - 1

        def in_range(number: int):
            return self.start_line_number <= number <= self.end_line_number

        # highlight code lines
        for line_no in range(len(self.mobject.code)):
            target.code[line_no].set_opacity(1 if in_range(line_no + 1) else 0.3)
            target.line_numbers[line_no].set_opacity(1 if in_range(line_no + 1) else 0.3)
        return target


class HighlightLine(HighlightLines):
    def __init__(self, mobject, line_number, target_mobject=None, **kwargs):
        super().__init__(mobject, start=line_number, end=line_number, target_mobject=target_mobject, **kwargs)


class HighlightNone(HighlightLines):
    def __init__(self, mobject, target_mobject=None, **kwargs):
        super().__init__(mobject, start=mobject.line_no_from, target_mobject=target_mobject, **kwargs)


class PartialCode(Code):
    def __init__(self, file_name=None, code: Optional[List[str]] = None, extension="py", **kwargs):

        if not code and not file_name:
            raise ValueError("Must define file_name or code")

        if code and not extension:
            raise ValueError("Must define the extension with the code")

        if not extension:
            extension = file_name.split(".")[-1]

        if file_name:
            with open(file_name, "r") as f:
                code = f.readlines()

        with NamedTemporaryFile(suffix=f".{extension}") as f:
            f.writelines([line.encode() for line in code])
            f.flush()
            super().__init__(f.name, **kwargs)


@dataclass
class Bounds:
    ul: Tuple[float, float, float] = None
    ur: Tuple[float, float, float] = None
    dr: Tuple[float, float, float] = None
    dl: Tuple[float, float, float] = None

    @property
    def width(self):
        return abs(self.ul[0] - self.ur[0])

    @property
    def height(self):
        return abs(self.ur[1] - self.dr[1])

    def as_mobject(self) -> Polygon:
        return Polygon(self.ul, self.ur, self.dr, self.dl)
