from tempfile import NamedTemporaryFile
from typing import List
from typing import Optional

from manim import Code
from manim import Transform
from manim.animation.fading import DEFAULT_FADE_LAG_RATIO


class HighlightLines(Transform):
    """
    Highlights lines by reducing the opacity of all non-highlighted lines
    """

    CONFIG = {
        "lag_ratio": DEFAULT_FADE_LAG_RATIO,
    }

    def __init__(self, code: Code, start: int = 1, end: int = -1, **kwargs):
        """
        Args:
            code: The code instance to highlight
            start: The line number to start highlighting, inclusive
            end: The last line number to highlight
        """
        super().__init__(code, **kwargs)
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
    """
    Highlights a single line by reducing the opacity of all non-highlighted lines
    """

    def __init__(self, code: Code, line_number: int, **kwargs):
        """
        Args:
            code: The code instance to highlight
            line_number: The line number to highlight
        """
        super().__init__(code, start=line_number, end=line_number, **kwargs)


class HighlightNone(HighlightLines):
    """
    Resets any previous highlighting by returning all source code lines to full opacity
    """

    def __init__(self, code: Code, **kwargs):
        """
        Args:
            code: The code instance to reset
        """
        super().__init__(code, start=code.line_no_from, **kwargs)


class PartialCode(Code):
    """
    Renders source code files or strings in part, delineated by line numbers
    """

    def __init__(self, path: Optional[str] = None, code: Optional[List[str]] = None, extension: str = "py", **kwargs):
        """
        Args:
            path: The source code file path. Either this or `code` must be set
            code: A list of code lines as strings. Either this or `path` must be set
            extension: The code extension, required if using `code`
        """

        if not code and not path:
            raise ValueError("Must define file_name or code")

        if code and not extension:
            raise ValueError("Must define the extension with the code")

        if not extension:
            extension = path.split(".")[-1]

        if path:
            with open(path, "r") as f:
                code = f.readlines()

        with NamedTemporaryFile(suffix=f".{extension}") as f:
            f.writelines([line.encode() for line in code])
            f.flush()
            super().__init__(f.name, **kwargs)
