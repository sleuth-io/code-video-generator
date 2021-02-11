from __future__ import annotations

import os
from typing import Optional
from typing import Union

from manim import ApplyMethod
from manim import Code
from manim import DEFAULT_WAIT_TIME
from manim import DOWN
from manim import FadeIn
from manim import FadeOut
from manim import ImageMobject
from manim import LEFT
from manim import MovingCameraScene
from manim import RIGHT
from manim import ShowCreation
from manim import Text
from manim import UP
from manim import WHITE

from code_video import comment_parser
from code_video.autoscale import AutoScaled
from code_video.code_walkthrough import HighlightLines
from code_video.code_walkthrough import HighlightNone
from code_video.code_walkthrough import PartialCode
from code_video.layout import ColumnLayout
from code_video.music import BackgroundMusic
from code_video.music import fit_audio
from code_video.widgets import DEFAULT_FONT
from code_video.widgets import TextBox
from code_video_cli import config


class CodeScene(MovingCameraScene):
    """
    This class serves as a convenience class for animating code walkthroughs in as
    little work as possible. For more control, use `Code` or `PartialCode`
    with the `HighlightLines` and `HighlightNone` transitions directly.
    """

    def __init__(
        self,
        *args,
        code_font="Ubuntu Mono",
        text_font="Helvetica",
        code_theme="fruity",
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.caption = None
        self.code_font = code_font
        self.text_font = text_font
        self.code_theme = code_theme
        self.col_width = None
        self.music: Optional[BackgroundMusic] = None
        self.pauses = {}

    def setup(self):
        super().setup()
        self.col_width = self.camera_frame.get_width() / 3

    def add_background_music(self, path: str) -> CodeScene:
        """
        Adds background music for the video. Can be combined with
        `wait_util_beat` or
        `wait_until_measure` to automatically time
        animations

        Args:
            path: The file path of the music file, usually an mp3 file.

        """
        self.music = BackgroundMusic(path)
        return self

    def tear_down(self):
        super().tear_down()
        if self.music:
            file = fit_audio(self.music.file, self.renderer.time + 2)
            old = self.renderer.skip_animations
            try:
                self.renderer.skip_animations = False
                self.add_sound(file, time_offset=-1 * self.renderer.time)
            finally:
                self.renderer.skip_animations = old
            os.remove(file)

        if self.pauses:
            config["slide_videos"] = self.renderer.file_writer.partial_movie_files[:]
            config["slide_stops"].update(self.pauses)
            config["movie_file_path"] = self.renderer.file_writer.movie_file_path

    def wait(self, duration=DEFAULT_WAIT_TIME, stop_condition=None):
        """
        Either waits like normal or if the codevidgen script is used and the "--slides" flag is used,
        it will treat these calls as breaks between slides
        """
        if config.get("show_slides"):
            print("In slide mode, skipping wait")
            super().wait(0.5)
            index = len(self.renderer.file_writer.partial_movie_files) - 1
            self.pauses[index] = []
        else:
            super().wait(duration, stop_condition)

    def play_movie(self, path: str):
        if config.get("show_slides"):
            index = len(self.renderer.file_writer.partial_movie_files) - 1
            self.pauses[index].append(path)

    def wait_until_beat(self, wait_time: Union[float, int]):
        """
        Waits until the next music beat, only works with `add_background_music`
        """
        if self.music:
            adjusted_delay = self.music.next_beat(self.renderer.time + wait_time) - self.renderer.time
            self.wait(adjusted_delay)
        else:
            self.wait(wait_time)

    def wait_until_measure(self, wait_time: Union[float, int], post: Union[float, int] = 0):
        """
        Waits until the next music measure, only works with `add_background_music`
        """
        if self.music:
            adjusted_delay = self.music.next_measure(self.renderer.time + wait_time) - self.renderer.time
            adjusted_delay += post
            self.wait(adjusted_delay)

        else:
            self.wait(wait_time)

    def add_background(self, path: str) -> ImageMobject:
        """
        Adds a full screen background image. The image will be stretched to the full width.

        Args:
            path: The file path of the image file
        """

        background = ImageMobject(path, height=self.camera_frame.get_height())
        background.stretch_to_fit_width(self.camera_frame.get_width())
        self.add(background)
        return background

    def animate_code_comments(
        self,
        path: str,
        title: str = None,
        keep_comments: bool = False,
        start_line: int = 1,
        end_line: Optional[int] = None,
        reset_at_end: bool = True,
    ) -> Code:
        """
        Parses a code file, displays it or a section of it, and animates comments

        Args:
            path: The source code file path
            title: The title or file path if not provided
            keep_comments: Whether to keep comments or strip them when displaying
            start_line: The start line number, used for displaying only a partial file
            end_line: The end line number, defaults to the end of the file
            reset_at_end: Whether to reset the code to full screen at the end or not
        """
        code, comments = comment_parser.parse(
            path, keep_comments=keep_comments, start_line=start_line, end_line=end_line
        )

        tex = AutoScaled(PartialCode(code=code, start_line=start_line, style=self.code_theme))
        if title is None:
            title = path

        title = Text(title, color=WHITE).to_edge(edge=UP)
        self.add(title)
        tex.next_to(title, DOWN)

        self.play(ShowCreation(tex))
        self.wait()

        for comment in comments:
            self.highlight_lines(tex, comment.start, comment.end, comment.caption)

        if self.caption:
            self.play(FadeOut(self.caption))
            self.caption = None

        if reset_at_end:
            self.play(HighlightNone(tex))
            self.play(ApplyMethod(tex.full_size))
        return tex

    def highlight_lines(self, code: Code, start: int = 1, end: int = -1, caption: Optional[str] = None):
        """
        Convenience method for animating a code object.

        Args:
            code: The code object, must be wrapped in `AutoScaled`
            start: The start line number
            end: The end line number, defaults to the end of the file
            caption: The text to display with the highlight
        """

        if end == -1:
            end = len(code.line_numbers) + code.line_no_from

        layout = ColumnLayout(columns=3)

        actions = []
        if caption and not self.caption:
            self.play(
                ApplyMethod(
                    code.fill_between_x,
                    layout.get_x(1, span=2, direction=LEFT),
                    layout.get_x(1, span=2, direction=RIGHT),
                )
            )

        if self.caption:
            actions.append(FadeOut(self.caption))
            self.caption = None

        if not caption:
            self.play(ApplyMethod(code.full_size))
        else:
            callout = TextBox(caption, text_attrs=dict(size=0.4, font=DEFAULT_FONT))
            callout.align_to(code.line_numbers[start - code.line_no_from], UP)
            callout.set_x(layout.get_x(3), LEFT)
            actions += [HighlightLines(code, start, end), FadeIn(callout)]
            self.caption = callout

        self.play(*actions)

        if not self.caption:
            self.play(ApplyMethod(code.full_size))
        else:
            wait_time = len(self.caption.text) / (200 * 5 / 60)
            self.wait_until_measure(wait_time, -1.5)

    def highlight_line(self, code: Code, number: int = -1, caption: Optional[str] = None):
        """
        Convenience method for highlighting a single line

        Args:
            code: The code object, must be wrapped in `AutoScaled`
            number: The line number
            caption: The text to display with the highlight
        """
        return self.highlight_lines(code, number, number, caption=caption)

    def highlight_none(self, code: Code):
        """
        Convenience method for resetting any existing highlighting.

        Args:
            code: The code object, must be wrapped in `AutoScaled`
        """
        if self.caption:
            self.play(FadeOut(self.caption), HighlightNone(code))
            self.caption = None

        self.play(ApplyMethod(code.full_size))

    def create_code(self, path: str, **kwargs) -> Code:
        """
        Convenience method for creating an autoscaled code object.

        Args:
            path: The source code file path
        """
        return AutoScaled(Code(path, font=self.code_font, style=self.code_theme, **kwargs))
