from __future__ import annotations

from typing import Dict
from typing import List
from typing import Optional

from manim import Arrow
from manim import DashedLine
from manim import DOWN
from manim import DR
from manim import LEFT
from manim import Rectangle
from manim import Scene
from manim import ShowCreation
from manim import Text
from manim import UP
from manim import VGroup


class Actor(VGroup):
    def __init__(self, diagram: SequenceDiagram, title: str):
        super().__init__()
        self.diagram = diagram
        box_height = Text("Q").get_height()
        self.title = title
        title = Text(title)
        rect = Rectangle(height=box_height + 0.5)
        title.move_to(rect)

        line = DashedLine(
            start=rect.get_edge_center(DOWN),
            end=[rect.get_center()[0], rect.get_center()[1] - self.get_height() - 5, 0],
            stroke_style="dashed",
        )
        self.add(rect, title, line)

    def text(self, value):
        self.diagram.interactions[-1].label = value
        return self

    def ret(self, value):
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
    def __init__(self, source: Actor, **kwargs):
        super().__init__(**kwargs)
        self.source = source
        self.target: Optional[Actor] = None
        self.label: str = ""

    def finish(self, target: Actor):
        self.target = target

        line = Arrow(start=[self.source.get_center()[0], 0, 0], end=[self.target.get_center()[0], 0, 0], buff=0)
        self.add(line)
        text = Text(self.label).scale(0.6).next_to(line, direction=UP, buff=0)
        self.add(text)


class SequenceDiagram(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.actors: Dict[str, Actor] = {}
        self.interactions: List[Interaction] = []

    def add_objects(self, *object_names: str):
        for name in object_names:
            actor = Actor(self, name)
            if not self.actors:
                actor.to_edge(LEFT)
            else:
                actor.next_to(list(self.actors.values())[-1], direction=DR)
            actor.to_edge(UP)
            self.actors[name] = actor
            self.add(actor)
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
        return interaction

    def animate(self, scene: Scene):
        scene.play(ShowCreation(self))
        start_y = self.get_edge_center(UP)[1] - 2
        last: Interaction = None
        for interaction in [item for item in self.interactions if item.target]:
            if not last:
                interaction.set_y(start_y)
            else:
                interaction.set_y(last.get_y(DOWN) - 0.5)
            scene.play(ShowCreation(interaction))
            last = interaction
