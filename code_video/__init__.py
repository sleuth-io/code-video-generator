from tempfile import NamedTemporaryFile
from textwrap import wrap
from typing import Optional, Callable, List

from manim import *

from code_video import comment_parser


class CodeScene(MovingCameraScene):
    def __init__(self, code_font: str = "Ubuntu Mono", text_font: str = "Helvetica", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.caption = None
        self.code_font = code_font
        self.text_font = text_font
        self.col_width = self.camera_frame.get_width() / 3

    def add_background(self, path: str) -> ImageMobject:
        background = ImageMobject(path, height=self.camera_frame.get_height())
        background.stretch_to_fit_width(self.camera_frame.get_width())
        self.add(background)
        return background

    def animate_code_comments(self, path: str, keep_comments: bool = False, start_line: int = 1, end_line: Optional[
        int] = None, reset_at_end: bool = True, parent: Optional[Mobject] = None) -> Code:

        code, comments = comment_parser.parse(path, keep_comments=keep_comments, start_line=start_line,
                                              end_line=end_line)

        with NamedTemporaryFile(suffix=f".{path.split('.')[-1]}") as f:
            f.writelines([line.encode() for line in code])
            f.flush()
            tex = self.create_code(f.name, line_no_from=start_line)
            if parent:
                parent.add(tex)
        self.play(ShowCreation(tex))

        for comment in comments:
            self.highlight_lines(tex, comment.start, comment.end, comment.caption)

        if reset_at_end:
            self.highlight_none(tex)
        return tex

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
                caption, font=self.text_font, size=self.col_width / 10 * 0.9
            ).add_background_rectangle(buff=MED_SMALL_BUFF)
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

    def highlight_line(
        self, tex: Code, number: int = -1, caption: Optional[str] = None
    ):
        return self.highlight_lines(tex, number, number, caption=caption)

    def highlight_none(self, tex: Code):
        return self.highlight_lines(tex, 1, len(tex.code) + 1, caption=None)

    def create_code(self, path: str, **kwargs) -> Code:
        tex = Code(path, font=self.code_font, style="paraiso-dark", **kwargs)
        x_scale = (self.col_width * 2) / tex.get_width()
        y_scale = self.camera_frame.get_height() * 0.95 / tex.get_height()
        tex.scale(min(x_scale, y_scale))
        return tex
