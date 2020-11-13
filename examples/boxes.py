from manim import DOWN
from manim import FadeIn
from manim import LEFT
from manim import RIGHT
from manim import Scene
from manim import ShowCreation

from code_video.library import Library


class BoxesScene(Scene):
    def construct(self):

        lib = Library()

        comp1 = lib.text_box("Component A", shadow=False)
        comp2 = lib.text_box("Component B", shadow=False)
        comp3 = lib.text_box("Component C", shadow=False)
        comp1.to_edge(LEFT)
        comp2.next_to(comp1, DOWN, buff=1)
        comp3.next_to(comp1, RIGHT, buff=4)
        arrow1 = lib.connect(comp2, comp1, "Do something")
        arrow2 = lib.connect(comp1, comp3, "Do another thing")

        self.play(FadeIn(comp2))
        self.play(ShowCreation(arrow1))
        self.play(FadeIn(comp1))
        self.play(ShowCreation(arrow2))
        self.play(FadeIn(comp3))

        self.wait(5)
