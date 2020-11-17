from os.path import dirname

from manim import DOWN
from manim import ShowCreation
from manim import Text
from manim import UP

from code_video import AutoScaled
from code_video import CodeScene
from code_video import SequenceDiagram


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

        title = Text("Sequence Diagram")
        title.to_edge(UP)
        self.add(title)
        diagram.next_to(title, DOWN)

        self.play(ShowCreation(diagram))
        for interaction in diagram.get_interactions():
            self.play(ShowCreation(interaction))

        self.wait(5)
