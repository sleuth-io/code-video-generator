[![Introduction video](http://img.youtube.com/vi/Jn7ZJ-OAM1g/0.jpg)](http://www.youtube.com/watch?v=Jn7ZJ-OAM1g "Introduction")

Code Video Generator is a library that uses the [Manim](https://github.com/manimcommunity/manim) animation engine
 to automatically generate code walkthrough videos. In fact, the source for the video above is at [examples/intro.py](https://github.com/sleuth-io/code-video-generator/tree/master/examples/intro.py).

## Installation

Code Video Generator needs Manim and a few other dependencies. Please visit
the
[documentation](https://code-video-generator.readthedocs.io/en/latest/installation.html).

## Usage

Here is an example video script that creates a video of itself:

```python
from code_video import CodeScene


class MyScene(CodeScene):
    def construct(self):
        # This does the actual code display and animation
        self.animate_code_comments("simple.py")
    
        # Wait 5 seconds before finishing
        self.wait(5)
```

Save this code in a file called `simple.py`. Now open your terminal in the
folder where you saved the file and execute

```sh
manim video.py -ql -p
```

You should see your video player pop up and play a simple walkthrough of `video.py`. You can find some more simple
 examples in the
[GitHub repository](https://github.com/sleuth-io/code-video-generator/tree/master/examples).

For more information on Manim, see their [ReadTheDocs](https://manimce.readthedocs.io/en/latest/).

## Contributing

If you'd like to contribute, feel free to fork or better yet, submit improvements as pull requests or report issues.

## License

The software is licensed under the Apache Public License v2, with copyright
by [Sleuth Enterprises](https://sleuth.io).