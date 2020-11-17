from os.path import dirname

from manim import ShowCreation, DOWN, Text, UP, ORIGIN

from code_video import CodeScene
from code_video import SequenceDiagram
from code_video.autoscale import AutoScaled


class SequenceDiagramsScene(CodeScene):
    def construct(self):
        example_dir = dirname(__file__)
        self.add_background(f"{example_dir}/resources/blackboard.jpg")
        diagram = AutoScaled(SequenceDiagram())
        browser, web, app = diagram.add_objects("Browser", "Web", "App")
        with browser:
            with web.text("Make a request"):
                web.to_target("Do a quick thing", app)
                with app.text("Retrieve a json object"):
                    app.to_self("Calls itself")
                    app.note("Do lots and lots and lots of thinking")
                    app.ret("Value from db")
                web.ret("HTML response")

        title = Text("hi")
        title.to_edge(UP)
        self.add(title)
        diagram.next_to(title, DOWN)
        self.play(ShowCreation(diagram))
        for interaction in diagram.get_interactions(diagram._overall_scale_factor):
            self.play(ShowCreation(interaction))
        # diagram.animate(self)

        title = Text("hi")
        title.to_edge(UP)
        self.add(title)
        diagram.next_to(title, DOWN)

        self.wait(5)
