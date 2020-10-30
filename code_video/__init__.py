from textwrap import wrap
from typing import Optional

from manim import *


class CodeScene(MovingCameraScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.caption = None
        self.col_width = self.camera_frame.get_width() / 3

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
            caption = "\n".join(wrap(caption, 25))
            if self.caption:
                pre_actions.append(FadeOut(self.caption))
            else:
                self.play(ApplyMethod(tex.to_edge))

            self.caption = PangoText(
                caption, font="Arial", size=self.col_width / 10 * 0.9
            )
            self.caption.next_to(tex, RIGHT)
            self.caption.align_to(tex.line_numbers[start - 1], UP)
            actions.append(FadeIn(self.caption))

        elif self.caption:
            actions.append(FadeOut(self.caption))
            post_actions += [ApplyMethod(tex.center)]
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

        if caption:
            wait_time = len(caption) / (200 * 5 / 60)
            self.wait(wait_time)
        self.play(*post_actions)

    def set_zoom_to_code(self, tex: Code):
        col_width = self.camera_frame.get_width() / 3
        self.camera_frame.scale(tex.get_width() / (col_width * 2))

    def play_zoom_to_code(self, tex: Code):
        col_width = self.camera_frame.get_width() / 3
        self.play(
            ApplyMethod(self.camera_frame.scale, tex.get_width() / (col_width * 2))
        )

    def play_zoom_to_code_and_caption(self, tex: Code):
        col_width = self.camera_frame.get_width() / 3
        self.play(
            ApplyMethod(self.camera_frame.scale, tex.get_width() / (col_width)),
            ApplyMethod(self.camera_frame.shift, tex.get_width() / (col_width) * LEFT),
        )

    def highlight_line(
        self, tex: Code, number: int = -1, caption: Optional[str] = None
    ):
        return self.highlight_lines(tex, number, number, caption=caption)

    def highlight_none(self, tex: Code):
        return self.highlight_lines(tex, 1, len(tex.code) + 1, caption=None)

    def create_code(self, path: str):
        tex = Code(path, font="Monospac821 BT")
        x_scale = (self.col_width * 2) / tex.get_width()
        y_scale = self.camera_frame.get_height() * 0.95 / tex.get_height()
        tex.scale(min(x_scale, y_scale))
        return tex
