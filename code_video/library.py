import hashlib
from textwrap import wrap
from typing import Callable
from typing import Optional

from manim import BLACK
from manim import DR
from manim import GREEN
from manim import Polygon
from manim import Rectangle
from manim import Text
from manim import VGroup

SHADOW_COLOR = BLACK

SHADOW_OPACITY = 0.3

SHADOW_SHIFT = 0.07

ROUNDED_RADIUS = 0.05


class Library:
    def __init__(
        self,
        text_font="Helvetica",
        code_font="Ubuntu Mono",
        code_theme="fruity",
        color_palette=None,
    ):
        if color_palette is None:
            color_palette = ["#00F6F6", "#F6A300", "#7BF600"]
        self.text_font = text_font
        self.code_font = code_font
        self.code_theme = code_theme
        self.color_palette = color_palette

    def text_box(
        self,
        text: str,
        text_attrs: Optional[dict] = None,
        wrap_at=30,
        rounded=False,
        shadow=True,
        color="#FFFFFF",
        bg_color="random",
        border_color="#FFFFFF",
    ):
        return self._box(
            text=text,
            wrap_at=wrap_at,
            rounded=rounded,
            shadow=shadow,
            color=color,
            border_color=border_color,
            text_attrs=text_attrs,
            bg_color=bg_color,
            border_builder=lambda title: Rectangle(
                height=_get_text_height(title) + 0.5, width=title.get_width() + 0.5
            ),
        )

    def note_box(
        self,
        text: str,
        text_attrs: Optional[dict] = None,
        wrap_at=30,
        shadow=True,
        color="#FFFFFF",
        bg_color="#FFFFFFFF",
        border_color="#FFFFFF",
    ):
        def build_border(title: Text):
            ear_size = title.get_width() * 0.05
            w = title.get_width() + 0.3 * 2
            h = title.get_height() + 0.3
            return Polygon((0, h, 0), (w - ear_size, h, 0), (w, h - ear_size, 0), (w, 0, 0), (0, 0, 0), (0, h, 0))

        return self._box(
            text=text,
            wrap_at=wrap_at,
            rounded=False,
            shadow=shadow,
            color=color,
            text_attrs=text_attrs,
            bg_color=bg_color,
            border_color=border_color,
            border_builder=build_border,
        )

    def _box(
        self,
        bg_color,
        color,
        rounded,
        shadow,
        text,
        wrap_at,
        border_color,
        text_attrs: Optional[dict],
        border_builder: Callable[[Text], Polygon],
    ):
        tblock = VGroup()
        if wrap_at:
            text = "\n".join(wrap(text, wrap_at))
        title = Text(text, font=self.text_font, color=color, **(text_attrs if text_attrs else {}))

        border = border_builder(title)
        border.set_color(border_color)
        bg_color, bg_opacity = self._color_and_opacity(bg_color, text)
        border.set_fill(color=bg_color, opacity=bg_opacity)
        if rounded:
            border.round_corners(ROUNDED_RADIUS)
        title.move_to(border)
        tblock.add(border, title)
        if shadow and bg_opacity:
            s_rect = border.copy()
            s_rect.set_color(SHADOW_COLOR)
            shadow_opacity = SHADOW_OPACITY
            s_rect.set_stroke(width=0)
            s_rect.set_background_stroke(color=GREEN, opacity=shadow_opacity, width=0)
            s_rect.set_fill(opacity=shadow_opacity)
            s_rect.scale(1 + SHADOW_SHIFT)
            s_rect.shift(SHADOW_SHIFT * DR)
            tblock.add_to_back(s_rect)
        return tblock

    def _color_and_opacity(self, value: str, text: str):
        if value == "random":
            text_hash = int(hashlib.sha1(text.encode()).hexdigest(), 16)
            return self.color_palette[text_hash % len(self.color_palette)], 0.2

        if value.startswith("#"):
            if len(value) == 7:
                return value, 1
            elif len(value) == 9:
                return value[:7], int(value[-2:], 16) / 255
        raise ValueError


def _get_text_height(text: Text) -> float:
    return max(Text("Ay", font=text.font).get_height(), text.get_height())
