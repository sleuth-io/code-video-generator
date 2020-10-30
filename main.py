from manim import *
from code_video import CodeScene


class CodeSceneDemo(CodeScene):
    def construct(self):
        tex = self.create_code("main.py")
        self.play(ShowCreation(tex, lag_ratio=5))
        self.highlight_line(
            tex,
            5,
            caption="Use the CodeScene to get extra helper methods such as "
            "highlight_line",
        )
        self.wait()
        self.highlight_lines(
            tex,
            16,
            22,
            caption="Highlight code with a caption to give extra information. A wait is"
            " automatically added for a time based on the length of the caption",
        )
        self.wait()
        self.highlight_line(tex, 26, caption="Reset highlighting and positioning")
        self.wait()
        self.highlight_none(tex)
        self.wait(5)
