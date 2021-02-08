from __future__ import annotations

from textwrap import wrap
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional

from manim import Arrow
from manim import DashedLine
from manim import DEFAULT_STROKE_WIDTH
from manim import DOWN
from manim import ITALIC
from manim import LEFT
from manim import MED_LARGE_BUFF
from manim import MED_SMALL_BUFF
from manim import RIGHT
from manim import Text
from manim import UP
from manim import VGroup
from manim import WHITE
from manim.mobject.geometry import DEFAULT_DASH_LENGTH
from manim.mobject.geometry import Polygon
from numba import np

from code_video.widgets import DEFAULT_FONT
from code_video.widgets import NoteBox
from code_video.widgets import TextBox

ARROW_STROKE_WIDTH = DEFAULT_STROKE_WIDTH * 1.2


class Actor(VGroup):
    """
    A sequence diagram actor that can be interacted with
    """

    def __init__(self, diagram: SequenceDiagram, title: str, font=DEFAULT_FONT):
        super().__init__()
        self.diagram = diagram
        self.font = font

        self.title = title

        self.block = TextBox(title, font=self.font, shadow=True, rounded=True)

        self.line = DashedLine(
            start=self.block.get_edge_center(DOWN),
            end=[self.block.get_center()[0], self.block.get_bottom()[1], 0],
            stroke_style="dashed",
            dash_length=DEFAULT_DASH_LENGTH * 2,
            stroke_width=DEFAULT_STROKE_WIDTH / 2,
            positive_space_ratio=0.5,
        )
        self.bblock = self.block.copy()
        self.bblock.next_to(self.line, direction=DOWN, buff=0)
        self.add(self.block, self.line, self.bblock)

    def stretch(self, middle_height: float):
        self.remove(self.line, self.bblock)
        self.line = DashedLine(
            start=self.block.get_edge_center(DOWN),
            end=[self.block.get_center()[0], self.block.get_bottom()[1] - middle_height, 0],
            stroke_style="dashed",
            dash_length=DEFAULT_DASH_LENGTH * 2,
            stroke_width=DEFAULT_STROKE_WIDTH / 2,
            positive_space_ratio=0.5,
        )
        self.bblock = self.block.copy()
        self.bblock.next_to(self.line, direction=DOWN, buff=0)
        self.add(self.line, self.bblock)

    def to(self, target: Actor, message: Optional[str] = None):
        """
        Adds an arrow to the next target. If the next target is the same as the source,
        render a self arrow

        Args:
            target: The target actor
            message: The arrow text
        """

        if self == target:
            interaction = SelfArrow(self, message)
        else:
            interaction = ActorArrow(self, target, message if message else "")
        self.diagram.add_interaction(interaction)
        return self

    def note(self, message: str):
        """
        Adds a note to the right of the actor

        Args:
            message: The text of the note
        """
        note_interaction = Note(self, message, RIGHT)
        self.diagram.add_interaction(note_interaction)
        return self

    def __str__(self):
        return f"Actor ({self.title})"


class Interaction(VGroup):
    def __init__(self, source, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.source = source


class ActorArrow(Interaction):
    """
    An interaction that can be displayed on the screen
    """

    def __init__(self, source: Actor, target: Actor, label: str = "", font=DEFAULT_FONT, **kwargs):
        super().__init__(source, font=font, **kwargs)
        self.target = target
        self.label = label
        self.font = font

        line = Arrow(
            start=[self.source.get_center()[0], 0, 0],
            end=[self.target.get_center()[0], 0, 0],
            buff=0,
            stroke_width=ARROW_STROKE_WIDTH,
        )
        text = Text(self.label, font=self.font, size=0.5, slant=ITALIC)
        text.next_to(line, direction=UP, buff=0)
        self.add(line, text)

    def scale(self, scale_factor, **kwargs):
        super().scale(scale_factor, **kwargs)
        self.submobjects[0].align_to(
            self.source.get_center(),
            direction=LEFT if self.source.get_center()[0] < self.target.get_center()[0] else RIGHT,
        )
        self.submobjects[1].next_to(self.submobjects[0], direction=UP, buff=0)
        return self

    def __str__(self):
        result = f"Interaction ({self.source.title}->{self.target.title if self.target else '?'})"
        if self.label:
            result += f" - {self.label}"
        return result


class Note(Interaction):
    def __init__(self, source: Actor, label: str, direction: np.array):
        super().__init__(source)
        self.label = label
        self.direction = direction

        block = NoteBox(
            self.label,
            font=source.font,
            text_attrs={"size": 0.5, "font": source.font},
            color=WHITE,
            border_color=WHITE,
            bg_color="#FFFFFF00",
            shadow=False,
        )
        block.next_to(source.get_center(), direction)
        self.add(block)

    def scale(self, scale_factor, **kwargs):
        for obj in self.submobjects:
            obj.scale(scale_factor, **kwargs)
            obj.next_to(self.source.get_center(), direction=self.direction)
        return self


class SelfArrow(Interaction):
    def __init__(self, source: Actor, label: str):
        super().__init__(source)
        self.label = "\n".join(wrap(label, 30))

        line_block = VGroup()

        spacing = 0.4
        distance = 0.8
        center_x = source.get_center()[0]
        line = Polygon(
            [center_x, spacing, 0],
            [center_x + distance, spacing, 0],
            [center_x + distance, -1 * spacing, 0],
            [center_x + distance / 2, -1 * spacing, 0],
            [center_x + distance, -1 * spacing, 0],
            [center_x + distance, spacing, 0],
            [center_x, spacing, 0],
            color=WHITE,
        )
        line.set_stroke(width=ARROW_STROKE_WIDTH)

        arrow = Arrow(
            start=[center_x + distance, -1 * spacing, 0],
            end=[center_x, -1 * spacing, 0],
            buff=0,
            stroke_width=ARROW_STROKE_WIDTH,
        )
        line_block.add(line, arrow)

        title = Text(self.label, font=self.source.font, size=0.5, slant=ITALIC)
        title.next_to(line_block)

        block = VGroup()
        block.add(line_block, title)
        block.next_to(source.get_center(), RIGHT)
        self.add(block)

    def scale(self, scale_factor, **kwargs):
        for obj in self.submobjects:
            obj.scale(scale_factor, **kwargs)
            obj.next_to(self.source.get_center(), direction=RIGHT, buff=0)
        return self


class SequenceDiagram(VGroup):
    """
    A sequence diagram built using a DSL
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.actors: Dict[str, Actor] = {}
        self.interactions: List[Interaction] = []

    def add_objects(self, *names: str) -> List[Actor]:
        """
        Add objects to draw interactions between

        Args:
            names: A list of display names for the actor objects
        """
        for name in names:
            actor = Actor(self, name)
            if not self.actors:
                actor.to_edge(LEFT)
            else:
                actor.next_to(list(self.actors.values())[-1])
            actor.to_edge(UP)
            self.actors[name] = actor
            self.add(actor)

        start_x = list(self.actors.values())[0].get_x(LEFT)
        actor_width = max(max(actor.get_width() + 0.5 for actor in self.actors.values()), 5)
        for idx, actor in enumerate(self.actors.values()):
            left_x = start_x + actor_width * idx
            actor.set_x(left_x + (actor_width - actor.get_width()) / 2, LEFT)

        return self.actors.values()

    def add_interaction(self, interaction: Interaction):
        self.interactions.append(interaction)

        for actor in self.actors.values():
            actor.stretch(sum(item.get_height() + 0.5 for item in self.interactions))

        return interaction

    def get_interactions(self) -> Iterable[Interaction]:
        """
        Gets the pre-programmed interactions for display
        """
        scale = getattr(self, "_overall_scale_factor", 1)
        last: Interaction = None
        for interaction in [item for item in self.interactions]:
            interaction.scale(scale)
            if not last:
                interaction.set_y(list(self.actors.values())[0].block.get_y(DOWN) - MED_SMALL_BUFF, direction=UP)
            else:
                interaction.set_y(last.get_y(DOWN) - MED_LARGE_BUFF * scale, direction=UP)

            yield interaction
            last = interaction
