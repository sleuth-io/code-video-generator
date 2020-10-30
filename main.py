from textwrap import wrap
from typing import Optional

from manim import *


class CodeScene(MovingCameraScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.caption = None

    def highlight_lines(
        self, tex: Code, start: int = 1, end: int = -1, caption: Optional[str] = None
    ):
        if end == -1:
            end = len(tex.line_numbers) + 1

        def in_range(number: int):
            return start <= number <= end

        pre_actions = []
        actions = []
        post_actions = []

        if caption:
            caption = "\n".join(wrap(caption, 10))
            if self.caption:
                pre_actions.append(FadeOut(self.caption))
                self.caption = PangoText(caption, font="Arial", size=0.7)
                self.caption.next_to(tex, RIGHT)
                actions.append(FadeIn(self.caption))
            else:
                pre_actions += [tex.shift, LEFT]
                self.caption = PangoText(caption, font="Arial", size=0.7)
                self.caption.next_to(tex, RIGHT)
                self.caption.shift(LEFT)
                actions.append(FadeIn(self.caption))

        elif self.caption:
            pre_actions.append(FadeOut(self.caption))
            post_actions += [tex.shift, RIGHT]
            self.caption = None

        # highlight code lines
        actions += [
            ApplyMethod(
                tex.code[line_no].set_opacity,
                1 if in_range(line_no + 1) else 0.3,
            )
            for line_no in range(len(tex.code))
        ]

        # highlight line numbers
        actions += [
            ApplyMethod(
                tex.line_numbers[line_no].set_opacity,
                1 if in_range(line_no + 1) else 0.3,
            )
            for line_no in range(len(tex.code))
        ]

        self.play(*pre_actions)
        self.play(*actions)
        self.play(*post_actions)

    def highlight_line(
        self, tex: Code, number: int = -1, caption: Optional[str] = None
    ):
        return self.highlight_lines(tex, number, number, caption=caption)

    def highlight_none(self, tex: Code):
        return self.highlight_lines(tex, 1, len(tex.code) + 1, caption=None)


class HelloLaTeX(CodeScene):
    def construct(self):
        self.camera_frame.save_state()
        tex = Code("code.py", font='Monospac821 BT')
        self.play(ShowCreation(tex, lag_ratio=5))
        # self.play(self.camera_frame.scale, 0.5)

        self.highlight_lines(
            tex, 2, 4, caption="Blah this is a really long line that overflows"
        )
        self.wait()
        self.highlight_line(tex, 5, caption="Foo")
        self.wait()
        self.highlight_none(tex)
        # self.play(Restore(self.camera_frame))
        self.wait(5)
