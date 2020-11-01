from os.path import dirname

from manim import DOWN
from manim import FadeIn
from manim import FadeOut
from manim import LARGE_BUFF
from manim import LEFT
from manim import linear
from manim import MED_LARGE_BUFF
from manim import PangoText
from manim import ShowCreation

from code_video import CodeScene

example_dir = dirname(__file__)


def title_scene(scene):
    scene.add_background(f"{example_dir}/resources/blackboard.jpg")
    title = PangoText("How to use Code Video Generator", font="Helvetica")
    scene.play(ShowCreation(title))
    scene.play(
        FadeIn(
            PangoText("A code walkthrough", font="Helvetica")
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
    and Code Video Generator provides a base scene that makes it easy
    to generate code walkthrough videos
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
        end=17,
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
        start_line=92,
        end_line=108,
        reset_at_end=False,
    )
    # end
    scene.wait(2)

    scene.play(FadeOut(code))
    scene.clear()


def demo_highlighting(scene: CodeScene):
    title = PangoText(
        """
        If you want more control, you can create code blocks and
        highlight them manually.
        """,
        font="Helvetica",
        line_spacing=0.5,
    ).scale(0.7)
    scene.play(ShowCreation(title, run_time=3, rate_func=linear))
    scene.wait(2)
    scene.clear()

    scene.add_background(f"{example_dir}/resources/blackboard.jpg")
    tex = scene.create_code(f"{example_dir}/highlights.py")
    scene.play(ShowCreation(tex))
    scene.highlight_line(
        tex,
        11,
        caption="Create code blocks yourself and pass in any arguments the Code class supports to do things "
        "like change the theme or font",
    )
    scene.highlight_lines(
        tex,
        13,
        19,
        caption="Highlight code with a caption to give extra information. A wait is"
        " automatically added for a time based on the length of the caption",
    )
    scene.highlight_line(tex, 21, caption="Reset highlighting and positioning")
    scene.highlight_none(tex)
    scene.play(FadeOut(tex))
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
        self.add_background_music(f"{example_dir}/resources/Pure Magic - Chris Haugen.mp3")
        title_scene(self)
        overview(self)
        demo_commenting(self)
        demo_highlighting(self)
        demo_render_self(self)
        goodbye(self)
