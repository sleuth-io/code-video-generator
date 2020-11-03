from __future__ import annotations

from manim import Scene

from code_video import SequenceDiagram


class SequenceDiagramsScene(Scene):
    def construct(self):

        diagram = SequenceDiagram()
        browser, web, app = diagram.add_objects("Browser", "Web", "App")
        with browser:
            with web.text("Make a request"):
                with app.text("Retrieve a json object"):
                    app.ret("Value from db")
                web.ret("HTML response")

        diagram.animate(self)

        self.wait(5)
