import hashlib
from textwrap import wrap
from typing import Callable
from typing import Optional

from manim import Arrow
from manim import BLACK
from manim import DOWN
from manim import DR
from manim import ITALIC
from manim import LEFT
from manim import Mobject
from manim import Polygon
from manim import Rectangle
from manim import RIGHT
from manim import Text
from manim import UP
from manim import VGroup
from manim import WHITE

SHADOW_COLOR = BLACK

SHADOW_OPACITY = 0.3

SHADOW_SHIFT = 0.07

ROUNDED_RADIUS = 0.05

VERTICAL_ARROW_LABEL_BUFF = 0.2


class BoxBase(VGroup):
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


class TextBox(BoxBase):
    """
    A text with a box around it
    """

    def __init__(self, text: str, **kwargs):
        """
        Args:
            text: The text to display
        """
        super().__init__(text, **kwargs)
        self._box(
            text=text,
            border_builder=lambda title: Rectangle(
                height=_get_text_height(title) + self.border_padding, width=title.get_width() + self.border_padding
            ),
        )


class NoteBox(BoxBase):
    """
    Text with a note box around it
    """

    def __init__(self, text: str, **kwargs):
        """
        Args:
            text: The text to display
        """
        super().__init__(text, **kwargs)

        def build_border(title: Text):
            ear_size = title.get_width() * 0.05
            w = title.get_width() + 0.3 * 2
            h = title.get_height() + 0.3
            return Polygon((0, h, 0), (w - ear_size, h, 0), (w, h - ear_size, 0), (w, 0, 0), (0, 0, 0), (0, h, 0))

        self._box(text=text, border_builder=build_border)


class Connection(VGroup):
    """
    An arrow connection between two objects
    """

    CONFIG = {"font": ""}

    def __init__(self, source: Mobject, target: Mobject, label: Optional[str] = None, **kwargs):
        """
        Args:
            source: The source object
            target: The target object
            label: The optional label text to put over the arrow
        """
        super().__init__(**kwargs)
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

        self.add(arrow)
        if label:
            text = Text(label, font=self.font, size=0.7, slant=ITALIC)
            text.next_to(arrow, direction=label_direction, buff=label_buff)
            self.add(text)


def _get_text_height(text: Text) -> float:
    return max(Text("Ay", font=text.font).get_height(), text.get_height())
