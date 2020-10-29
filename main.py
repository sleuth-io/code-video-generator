from manim import *


class HelloLaTeX(MovingCameraScene):
    CONFIG = {
        "camera_config": {"background_color": "#475147"}
    }

    def highlight_line(self, tex: Code, number: int = -1):
        return [ApplyMethod(tex.code[line_no].set_opacity,
                     .3 if line_no != number and number != -1 else 1) for line_no
         in range(len(
            tex.code))]

    def construct(self):
        self.camera_frame.save_state()
        tex = Code("code.py")
        self.play(ShowCreation(tex, lag_ratio=5))
        self.play(self.camera_frame.scale, 0.5, self.camera_frame.move_to, tex.line_numbers[2], *self.highlight_line(
            tex, 2))
        self.wait()
        self.play(self.camera_frame.move_to, tex.line_numbers[4], *self.highlight_line(tex, 4))
        self.wait()
        self.play(Restore(self.camera_frame), *self.highlight_line(tex))
        self.wait(5)
