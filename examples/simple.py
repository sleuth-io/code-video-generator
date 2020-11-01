from code_video import CodeScene


class MyScene(CodeScene):
    def construct(self):
        # This does the actual code display and animation
        self.animate_code_comments("simple.py")

        # Wait 5 seconds before finishing
        self.wait(5)
