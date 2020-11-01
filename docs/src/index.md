# Code Video Generator

<iframe width="560" height="315" src="https://www.youtube.com/embed/Jn7ZJ-OAM1g" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Code Video Generator is a library for [Manim](https://github.com/manimcommunity/manim) that makes creating decent
 looking code walkthrough videos easy.  With a few comments in your target source files and a bit of Python, you can
  generate a code walk through video with animations, code formatting, automatic callouts, and even synchronized sound.

## Features

* **Automatic callout-style walkthroughs** - Turn your existing code comments into an animated, colorful walkthrough
* **Synchronized music** - Add not just music, but music that is automatically synchronized to walkthrough steps
* **Completely free** - Apache v2 license

## Quickstart

1. [Install](installation.html) Manim and code-video-generator
1. Create a simple scene to show a file, say `simple.py`:
```
from code_video import CodeScene

class MyScene(CodeScene):
    def construct(self):
        # This does the actual code display and animation
        self.animate_code_comments("simple.py")
    
        # Wait 5 seconds before finishing
        self.wait(5)
```
1. Render the video in low quality (faster) and with an automatic preview:
```
manim video.py -ql -p
```

It should look something like this:

<iframe width="560" height="315" src="https://www.youtube.com/embed/I-Y__IJ_y90" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


## Get involved

If you'd like to contribute, feel free to fork or better yet, submit improvements as pull requests or report issues
 at [sleuth-io/code-video-generator](https://github.com/sleuth-io/code-video-generator).

