from os.path import dirname

from manim import *

from code_video import CodeScene


def title_scene(scene):
    example_dir = dirname(__file__)
    scene.add_background(f"{example_dir}/images/blackboard.jpg")
    title = PangoText("How to use Manim and Code Videos", font="Helvetica")
    scene.play(ShowCreation(title))
    scene.play(FadeIn(PangoText("A code walkthrough", font="Helvetica").scale(.6).next_to(title, direction=DOWN,
                                                                                                buff=LARGE_BUFF)))

    scene.wait(3)
    scene.clear()


def overview(scene):
    title = PangoText("""
    Manim is a Python library used to generate videos, 
    and Code Videos provides a base scene that makes it easy 
    to generate code walkthrough videos
    ... in fact, it is what was used to generate this video!
    """, font="Helvetica", line_spacing=.5).scale(.7)
    scene.play(ShowCreation(title, run_time=10, rate_func=linear))
    scene.wait(3)
    sub = PangoText("""
        Here is an example:
        """, font="Helvetica").scale(.7).next_to(title, direction=DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
    scene.play(ShowCreation(sub))
    scene.wait(2)
    scene.clear()


def demo_highlighting(scene: CodeScene):
    example_dir = dirname(__file__)
    scene.add_background(f"{example_dir}/images/blackboard.jpg")
    title = PangoText("example/highlights.py", font="Helvetica").to_edge(edge=UP)
    scene.add(title)
    code_group = VGroup().next_to(title, direction=DOWN)
    scene.add(code_group)
    code = scene.animate_code_comments(
        f"{example_dir}/commented.py", keep_comments=True, start_line=7, end_line=20, reset_at_end=False,
    parent=code_group)

    scene.highlight_line(code, number=6, caption="These caption callouts are "
                                                "automatically generated from comments when "
                                                "using animate_code_comments()")
    scene.highlight_lines(code, start=9,
                         end=14,
                         caption="You can also highlight multiple "
                                 "lines by ending the block with '# "
                                 "end'")
    scene.highlight_none(code)
    scene.clear()


class Main(CodeScene):
    def construct(self):
        title_scene(self)
        overview(self)
        demo_highlighting(self)


