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

from code_video.widgets import NoteBox
from code_video.widgets import TextBox

ARROW_STROKE_WIDTH = DEFAULT_STROKE_WIDTH * 1.2


class Actor(VGroup):
    """
    A sequence diagram actor that can be interacted with
    """

    CONFIG = {"font": ""}

    def __init__(self, diagram: SequenceDiagram, title: str):
        super().__init__()
        self.diagram = diagram

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

    def text(self, value):
        self.diagram.interactions[-1].label = value
        return self

    def note(self, value: str):
        """
        Adds a note to the right of the actor

        Args:
            value: The text of the note
        """
        note_interaction = Note(self, value, RIGHT)
        interaction = self.diagram.interactions[-1]
        if not interaction.target:
            self.diagram.interactions.insert(-1, note_interaction)
        else:
            self.diagram.interactions.append(note_interaction)

    def to_self(self, value: str):
        """
        Adds an arrow to itself with a label

        Args:
            value: The label text
        """
        note_interaction = SelfArrow(self, value)
        interaction = self.diagram.interactions[-1]
        if not interaction.target:
            self.diagram.interactions.insert(-1, note_interaction)
        else:
            self.diagram.interactions.append(note_interaction)

    def to_target(self, value: str, target: Actor):
        """
        Adds an arrow to the next target

        Args:
            value: The arrow text
            target: The target actor
        """
        note_interaction = Interaction(source=self, label=value).finish(target)
        interaction = self.diagram.interactions[-1]
        if not interaction.target:
            self.diagram.interactions.insert(-1, note_interaction)
        else:
            self.diagram.interactions.append(note_interaction)

    def ret(self, value: str):
        """
        Sets the text on the return interaction

        Args:
            value: The label text
        """
        interaction = self.diagram.interactions[-1]
        if not interaction.target:
            interaction = self.diagram.start_interaction(self)
        interaction.label = value
        return self.cur_interaction

    def __enter__(self):
        interaction = self.diagram.start_interaction(self)
        self.cur_interaction = interaction
        return self.cur_interaction

    def __exit__(self, exc_type, exc_val, exc_tb):
        interaction = self.diagram.start_interaction(self)
        self.cur_interaction = interaction
        return self.cur_interaction


class Interaction(VGroup):
    """
    An interaction that can be displayed on the screen
    """

    CONFIG = {"font": ""}

    def __init__(self, source: Actor, label: str = "", target: Optional[Actor] = None, **kwargs):
        super().__init__(**kwargs)
        self.source = source
        self.target = target
        self.label = label

    def finish(self, target: Actor):
        self.target = target

        line = Arrow(
            start=[self.source.get_center()[0], 0, 0],
            end=[self.target.get_center()[0], 0, 0],
            buff=0,
            stroke_width=ARROW_STROKE_WIDTH,
        )
        text = Text(self.label, font=self.font, size=0.7, slant=ITALIC)
        text.next_to(line, direction=UP, buff=0)
        self.add(line, text)
        return self

    def scale(self, scale_factor, **kwargs):
        super().scale(scale_factor, **kwargs)
        self.submobjects[0].align_to(
            self.source.get_center(),
            direction=LEFT if self.source.get_center()[0] < self.target.get_center()[0] else RIGHT,
        )
        self.submobjects[1].next_to(self.submobjects[0], direction=UP, buff=0)
        return self


class Note(Interaction):
    def __init__(self, target: Actor, label: str, direction: np.array):
        super().__init__(target)
        self.target = target
        self.label = label
        self.direction = direction

        block = NoteBox(
            self.label,
            font=target.font,
            text_attrs={"size": 0.7},
            color=WHITE,
            border_color=WHITE,
            bg_color="#FFFFFF00",
            shadow=False,
        )
        block.next_to(target.get_center(), direction)
        self.add(block)

    def scale(self, scale_factor, **kwargs):
        for obj in self.submobjects:
            obj.scale(scale_factor, **kwargs)
            obj.next_to(self.source.get_center(), direction=self.direction)
        return self

    def finish(self, target: Actor):
        raise NotImplementedError()


class SelfArrow(Interaction):
    def __init__(self, target: Actor, label: str):
        super().__init__(target)
        self.target = target
        self.label = "\n".join(wrap(label, 30))

        line_block = VGroup()

        spacing = 0.4
        distance = 0.8
        line = Polygon(
            [target.get_center()[0], spacing, 0],
            [target.get_center()[0] + distance, spacing, 0],
            [target.get_center()[0] + distance, -1 * spacing, 0],
            [target.get_center()[0] + distance / 2, -1 * spacing, 0],
            [target.get_center()[0] + distance, -1 * spacing, 0],
            [target.get_center()[0] + distance, spacing, 0],
            [target.get_center()[0], spacing, 0],
            color=WHITE,
        )
        line.set_stroke(width=ARROW_STROKE_WIDTH)

        arrow = Arrow(
            start=[target.get_center()[0] + distance, -1 * spacing, 0],
            end=[target.get_center()[0], -1 * spacing, 0],
            buff=0,
            stroke_width=ARROW_STROKE_WIDTH,
        )
        line_block.add(line, arrow)

        title = Text(self.label, font="Helvetica", size=0.7, slant=ITALIC)
        title.next_to(line_block)

        block = VGroup()
        block.add(line_block, title)
        block.next_to(target.get_center(), RIGHT)
        self.add(block)

    def scale(self, scale_factor, **kwargs):
        for obj in self.submobjects:
            obj.scale(scale_factor, **kwargs)
            obj.next_to(self.source.get_center(), direction=RIGHT, buff=0)
        return self

    def finish(self, target: Actor):
        raise NotImplementedError()


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

    def start_interaction(self, actor: Actor):
        if self.interactions:
            last = self.interactions[-1]
            if last.source == actor:
                return last
            elif not last.target:
                last.finish(actor)
        interaction = Interaction(actor)
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
        for interaction in [item for item in self.interactions if item.target]:
            interaction.scale(scale)
            if not last:
                interaction.set_y(list(self.actors.values())[0].block.get_y(DOWN) - MED_SMALL_BUFF, direction=UP)
            else:
                interaction.set_y(last.get_y(DOWN) - MED_LARGE_BUFF * scale, direction=UP)

            yield interaction
            last = interaction
