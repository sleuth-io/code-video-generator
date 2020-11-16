from importlib.metadata import PackageNotFoundError
from importlib.metadata import version
from os.path import dirname

from manim import DOWN
from manim import FadeIn
from manim import FadeOut
from manim import LARGE_BUFF
from manim import LEFT
from manim import linear
from manim import MED_LARGE_BUFF
from manim import PangoText
from manim import RIGHT
from manim import ShowCreation
from manim import Text
from manim import UP

from code_video import CodeScene
from code_video import SequenceDiagram
from code_video.library import Library

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    __version__ = "0.3-dev"

example_dir = dirname(__file__)


def title_scene(scene):

    scene.add_background(f"{example_dir}/resources/blackboard.jpg")
    title = PangoText("How to use Code Video Generator", font="Helvetica")
    scene.play(ShowCreation(title))
    scene.play(
        FadeIn(
            PangoText(f"Code and examples from version {__version__}", font="Helvetica")
            .scale(0.6)
            .next_to(title, direction=DOWN, buff=LARGE_BUFF)
        )
    )

    scene.wait(3)
    scene.clear()


def overview(scene):
    title = PangoText(
        """
    Manim is a Python library used to generate videos,
    and Code Video Generator extends it to make it easy
    to generate code-related videos
    ... in fact, it is what was used to generate this video!
    """,
        font="Helvetica",
        line_spacing=0.5,
    ).scale(0.7)
    scene.play(ShowCreation(title, run_time=10, rate_func=linear))
    scene.wait(3)
    sub = (
        PangoText(
            """
        Here is an example:
        """,
            font="Helvetica",
        )
        .scale(0.7)
        .next_to(title, direction=DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
    )
    scene.play(ShowCreation(sub))
    scene.wait(2)
    scene.clear()


def demo_commenting(scene: CodeScene):
    scene.add_background(f"{example_dir}/resources/blackboard.jpg")

    code = scene.animate_code_comments(
        title="examples/commented.py",
        path=f"{example_dir}/commented.py",
        keep_comments=True,
        start_line=6,
        end_line=19,
        reset_at_end=False,
    )

    scene.highlight_line(
        code,
        number=6,
        caption="These caption callouts are "
        "automatically generated from comments when "
        "using animate_code_comments()",
    )
    scene.highlight_lines(
        code,
        start=14,
        end=18,
        caption="You can also highlight multiple " "lines by ending the block with '# " "end'",
    )
    scene.highlight_none(code)
    scene.play(FadeOut(code))
    scene.clear()


def demo_render_self(scene: CodeScene):
    scene.add_background(f"{example_dir}/resources/blackboard.jpg")

    # Here is the code rendering this video you are watching now!
    code = scene.animate_code_comments(
        title="examples/intro.py",
        path=f"{example_dir}/intro.py",
        keep_comments=True,
        start_line=93,
        end_line=109,
        reset_at_end=False,
    )
    # end
    scene.wait(2)

    scene.play(FadeOut(code))
    scene.clear()


def demo_sequence(scene: CodeScene):
    title = PangoText(
        """
        You can use Code Video Generator to also illustrate
        high-level concepts through sequence diagrams, or
        if you want more control, your own block diagrams:
        """,
        font="Helvetica",
        line_spacing=0.5,
    ).scale(0.7)
    scene.play(ShowCreation(title, run_time=4, rate_func=linear))
    scene.wait(3)
    scene.clear()

    scene.add_background(f"{example_dir}/resources/blackboard.jpg")

    title = Text("examples/boxes.py")
    title.to_edge(UP)
    scene.add(title)

    diagram = SequenceDiagram(max_y=title.get_y(DOWN) - 1)
    browser, web, app = diagram.add_objects("Browser", "Web", "App")
    with browser:
        with web.text("Make a request"):
            web.to_target("Request with no response", app)
            with app.text("Retrieve a json object"):
                app.to_self("Calls itself")
                app.note("Do lots and lots and lots of thinking")
                app.ret("Value from db")
            web.ret("HTML response")

    diagram.animate(scene)
    scene.wait(3)
    scene.play(FadeOut(diagram))
    scene.clear()


def demo_boxes(scene: CodeScene):
    scene.add_background(f"{example_dir}/resources/blackboard.jpg")
    lib = Library()

    title = Text("examples/boxes.py")
    title.to_edge(UP)
    scene.add(title)
    comp1 = lib.text_box("Component A", shadow=False)
    comp2 = lib.text_box("Component B", shadow=False)
    comp3 = lib.text_box("Component C", shadow=False)
    comp1.next_to(title, DOWN, buff=2)
    comp1.to_edge(LEFT)
    comp2.next_to(comp1, DOWN, buff=1)
    comp3.next_to(comp1, RIGHT, buff=4)
    arrow1 = lib.connect(comp2, comp1, "Do something")
    arrow2 = lib.connect(comp1, comp3, "Do another thing")

    scene.play(FadeIn(comp2))
    scene.wait_until_beat(1)
    scene.play(ShowCreation(arrow1))
    scene.play(FadeIn(comp1))
    scene.wait_until_beat(1)
    scene.play(ShowCreation(arrow2))
    scene.play(FadeIn(comp3))

    scene.wait_until_beat(4)
    scene.clear()


def goodbye(scene: CodeScene):
    title = PangoText(
        """
        Try Code Video Generator today at:

          https://github.com/sleuth-io/code-video-generator

        Thanks for watching!""",
        font="Helvetica",
        line_spacing=0.5,
    ).scale(0.7)
    scene.play(ShowCreation(title, run_time=4, rate_func=linear))
    scene.wait(5)
    scene.play(FadeOut(title))


class Main(CodeScene):
    def construct(self):
        # self.add_background_music(f"{example_dir}/resources/Pure Magic - Chris Haugen.mp3")
        # title_scene(self)
        # overview(self)
        demo_commenting(self)
        # demo_sequence(self)
        # demo_boxes(self)
        # # demo_render_self(self)
        # goodbye(self)
