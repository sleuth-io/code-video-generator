import hashlib
from textwrap import wrap
from typing import Callable

from manim import BLACK
from manim import DR
from manim import Polygon
from manim import Rectangle
from manim import Text
from manim import VGroup
from manim import WHITE

from code_video.library import _get_text_height

SHADOW_COLOR = BLACK

SHADOW_OPACITY = 0.3

SHADOW_SHIFT = 0.07

ROUNDED_RADIUS = 0.05

VERTICAL_ARROW_LABEL_BUFF = 0.2


class TextBox(VGroup):
    CONFIG = {
        "text_attrs": {},
        "wrap_at": 30,
        "rounded": False,
        "shadow": True,
        "bg_color": "random",
        "border_color": WHITE,
        "border_padding": 0.5,
        "color_palette": ["#00F6F6", "#F6A300", "#7BF600"],
    }

    def __init__(self, text: str, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self._box(
            text=text,
            border_builder=lambda title: Rectangle(
                height=_get_text_height(title) + self.border_padding, width=title.get_width() + self.border_padding
            ),
        )

    def _box(
        self,
        text,
        border_builder: Callable[[Text], Polygon],
    ):

        if self.wrap_at:
            text = "\n".join(wrap(text, self.wrap_at))
        title = Text(text, **self.text_attrs)

        border = border_builder(title)
        border.set_color(self.border_color)
        bg_color, bg_opacity = self._color_and_opacity(self.bg_color, text)
        border.set_fill(color=bg_color, opacity=bg_opacity)
        if self.rounded:
            border.round_corners(ROUNDED_RADIUS)
        title.move_to(border)
        self.add(border, title)
        if self.shadow and bg_opacity:
            s_rect = border.copy()
            s_rect.set_color(SHADOW_COLOR)
            shadow_opacity = SHADOW_OPACITY
            s_rect.set_stroke(width=0)
            s_rect.set_background_stroke(width=0)
            s_rect.set_fill(opacity=shadow_opacity)
            s_rect.scale(1 + SHADOW_SHIFT)
            s_rect.shift(SHADOW_SHIFT * DR)
            self.add_to_back(s_rect)

    def _color_and_opacity(self, value: str, text: str):
        palette = self.CONFIG["color_palette"]
        if value == "random":
            text_hash = int(hashlib.sha1(text.encode()).hexdigest(), 16)
            return palette[text_hash % len(palette)], 0.2

        if value.startswith("#"):
            if len(value) == 7:
                return value, 1
            elif len(value) == 9:
                return value[:7], int(value[-2:], 16) / 255
        raise ValueError
