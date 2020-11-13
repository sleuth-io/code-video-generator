from __future__ import annotations

import hashlib
from textwrap import wrap
from typing import Callable
from typing import Dict
from typing import Optional

from manim import Arrow
from manim import BLACK
from manim import DOWN
from manim import DR
from manim import GREEN
from manim import ITALIC
from manim import LEFT
from manim import Mobject
from manim import Polygon
from manim import Rectangle
from manim import RIGHT
from manim import Text
from manim import UP
from manim import VGroup

SHADOW_COLOR = BLACK

SHADOW_OPACITY = 0.3

SHADOW_SHIFT = 0.07

ROUNDED_RADIUS = 0.05

VERTICAL_ARROW_LABEL_BUFF = 0.2


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

    def bordered_group(
        self,
        *children: Mobject,
        border_attrs: Optional[Dict] = None,
        title: Optional[str] = None,
        title_attrs: Optional[Dict] = None,
    ):
        group = VGroup(*children)

        width = (
            abs(max(child.get_x(RIGHT) for child in children) - min(child.get_x(LEFT) for child in children)) + 1.2
        )
        height = abs(max(child.get_y(UP) for child in children) - min(child.get_y(DOWN) for child in children)) + 1.2

        rect = Rectangle(**_merge(border_attrs, width=width, height=height))
        rect.move_to(group.get_center_of_mass())
        group.add_to_back(rect)
        if title:
            label = self.text_box(
                title, **_merge(title_attrs, bg_color=BLACK, border_color=BLACK, rounded=False, shadow=False)
            )
            label.scale(0.8)
            label.move_to(group.get_top())
            group.add(label)
        return group

    def connect(self, source: Mobject, target: Mobject, label: Optional[str] = None) -> Connection:

        result = Connection()
        label_direction = UP
        label_buff = 0

        arrow: Optional[Arrow] = None
        if source.get_x(RIGHT) <= target.get_x(LEFT):
            arrow = Arrow(start=source.get_edge_center(RIGHT), end=target.get_edge_center(LEFT), buff=0)
            label_direction = UP
        elif source.get_x(LEFT) >= target.get_x(RIGHT):
            arrow = Arrow(start=source.get_edge_center(LEFT), end=target.get_edge_center(RIGHT), buff=0)
            label_direction = UP
        elif source.get_y(DOWN) >= target.get_y(UP):
            arrow = Arrow(start=source.get_edge_center(DOWN), end=target.get_edge_center(UP), buff=0)
            label_direction = RIGHT
            label_buff = VERTICAL_ARROW_LABEL_BUFF
        elif source.get_y(UP) <= target.get_y(DOWN):
            arrow = Arrow(start=source.get_edge_center(UP), end=target.get_edge_center(DOWN), buff=0)
            label_direction = RIGHT
            label_buff = VERTICAL_ARROW_LABEL_BUFF

        if not arrow:
            raise ValueError("Unable to connect")

        result.add(arrow)
        if label:
            text = Text(label, font=self.text_font, size=0.7, slant=ITALIC)
            text.next_to(arrow, direction=label_direction, buff=label_buff)
            result.add(text)

        return result

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
        border_padding=0.5,
    ) -> TextBox:
        return self._box(
            TextBox(),
            text=text,
            wrap_at=wrap_at,
            rounded=rounded,
            shadow=shadow,
            color=color,
            border_color=border_color,
            text_attrs=text_attrs,
            bg_color=bg_color,
            border_builder=lambda title: Rectangle(
                height=_get_text_height(title) + border_padding, width=title.get_width() + border_padding
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
    ) -> NoteBox:
        def build_border(title: Text):
            ear_size = title.get_width() * 0.05
            w = title.get_width() + 0.3 * 2
            h = title.get_height() + 0.3
            return Polygon((0, h, 0), (w - ear_size, h, 0), (w, h - ear_size, 0), (w, 0, 0), (0, 0, 0), (0, h, 0))

        return self._box(
            NoteBox(),
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
        parent: VGroup,
        bg_color,
        color,
        rounded,
        shadow,
        text,
        wrap_at,
        border_color,
        text_attrs: Optional[dict],
        border_builder: Callable[[Text], Polygon],
    ) -> VGroup:
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
        parent.add(border, title)
        if shadow and bg_opacity:
            s_rect = border.copy()
            s_rect.set_color(SHADOW_COLOR)
            shadow_opacity = SHADOW_OPACITY
            s_rect.set_stroke(width=0)
            s_rect.set_background_stroke(color=GREEN, opacity=shadow_opacity, width=0)
            s_rect.set_fill(opacity=shadow_opacity)
            s_rect.scale(1 + SHADOW_SHIFT)
            s_rect.shift(SHADOW_SHIFT * DR)
            parent.add_to_back(s_rect)
        return parent

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


class TextBox(VGroup):
    pass


class NoteBox(VGroup):
    pass


class Connection(VGroup):
    pass


def _merge(extra_args: Optional[Dict] = None, **kwargs):
    if extra_args:
        kwargs.update(extra_args)

    return kwargs


def _get_text_height(text: Text) -> float:
    return max(Text("Ay", font=text.font).get_height(), text.get_height())
