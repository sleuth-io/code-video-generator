from os.path import dirname

from code_video import CodeScene


# Use the CodeScene to get the extra helper methods
class CommentedScene(CodeScene):
    def construct(self):
        example_dir = dirname(__file__)

        # Add a full screen background image to make the video a bit more interesting
        self.add_background(f"{example_dir}/resources/blackboard.jpg")

        # Display the code and animate comments as highlighted lines. For more control, use
        # highlight_line(s) directly.
        self.animate_code_comments(f"{example_dir}/commented.py", keep_comments=True, start_line=5, end_line=16)
        # end

        self.wait(5)
