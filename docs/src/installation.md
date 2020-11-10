# Installation

There are two primary ways to install Code Video Generator: use Docker or install everything into your host system
. The advantage of the Docker approach is there is nothing to install, but you may want the additional control of
 having the application run locally.
 
## Docker installation
 
To run Code Video Generator via Docker, you have two options:
 
1. Use the `codevidgen.sh` wrapper script
2. Run docker directly
 
### Using `codevidgen.sh`
 
1. Download the script and make it executable:
    
        wget https://raw.githubusercontent.com/sleuth-io/code-video-generator/master/bin/codevidgen.sh
        chmod 755 codevidgen.sh
        
1. Move the script to either a directory that is already in your path or add it to your path
1. You will now be able to invoke Code Video Generator via:
 
        codevidgen.sh myscene.py
         
### Using Docker run directly
 
If you don't want to use the wrapper script, you can poke around and see how it executes docker run, and run
 something similar to that.
 
## Local installation
 
Code Video Generator is a library for [Manim](https://github.com/manimcommunity/manim), and as such, the first
step is to follow their [installation buide](https://docs.manim.community/en/latest/installation.html).
 
Once Manim is installed, you can simply install code-video-generator using pip:

```
pip install code-video-generator
```

Note: You may need to install manimmc from source in order to get the [comment bug fix](https://github.com/ManimCommunity/manim/issues/638). 