from os.path import dirname

from code_video import CodeScene
from code_video import SequenceDiagram


class SequenceDiagramsScene(CodeScene):
    def construct(self):
        example_dir = dirname(__file__)
        self.add_background(f"{example_dir}/resources/blackboard.jpg")
        diagram = SequenceDiagram()
        browser, web, app = diagram.add_objects("Browser", "Web", "App")
        with browser:
            with web.text("Make a request"):
                web.to_target("Do a quick thing", app)
                with app.text("Retrieve a json object"):
                    app.to_self("Calls itself")
                    app.note("Do lots and lots and lots of thinking")
                    app.ret("Value from db")
                web.ret("HTML response")

        diagram.animate(self)

        self.wait(5)
