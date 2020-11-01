from os.path import dirname

from manim import *

from code_video import CodeScene


class HighlightScene(CodeScene):
    def construct(self):
        example_dir = dirname(__file__)
        tex = self.create_code(f"{example_dir}/highlights.py")
        self.play(ShowCreation(tex))
        self.highlight_lines(
            tex,
            12,
            18,
            caption="Highlight code with a caption to give extra information. A wait is"
            " automatically added for a time based on the length of the caption",
        )
        self.highlight_line(tex, 20, caption="Reset highlighting and positioning")
        self.highlight_none(tex)
        self.wait(5)
