import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--slides",
        action="store_const",
        const=True,
        help="Automatically open the videos as fullscreen slides once its done",
    )
    args, extra = parser.parse_known_args(sys.argv[1:])
    sys.argv = [sys.argv[0].replace("codevidgen", "manim")] + extra

    from manim.__main__ import main as manim_main
    from manim import config
    config["show_slides"] = args.slides
    config["slide_stops"] = []
    manim_main()
    if args.slides:
        from code_video.player import VideoPlayer
        partial_files = config["slide_videos"]
        pauses = config["slide_stops"]
        movie_file_path = config["movie_file_path"]
        player = VideoPlayer(clip_file_pattern=movie_file_path[:-4] + "-{index}.mp4")
        clip = []

        for idx, partial_file in enumerate([f for f in partial_files if f is not None]):
            clip.append(partial_file)
            if idx in pauses:
                if clip:
                    player.add_movies(*clip)
                    clip.clear()

        if clip:
            player.add_movies(*clip)
        player.play()


if __name__ == '__main__':
    main()