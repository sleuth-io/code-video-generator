import os
import sys
from dataclasses import dataclass
from tempfile import NamedTemporaryFile
from typing import List
from typing import Optional

import ffmpeg
import pyglet
from pyglet import gl
from pyglet.media.codecs.ffmpeg import FFmpegSource
from pyglet.window import key


@dataclass
class Clip:
    file: str
    source: FFmpegSource


class VideoPlayer:
    def __init__(self, clip_file_pattern: str):
        self._window = pyglet.window.Window(fullscreen=True)
        self._window.event(self.on_draw)
        self._window.event(self.on_key_press)
        self._player = pyglet.media.Player()
        self._clips: List[Clip] = []
        self._clip_file_pattern = clip_file_pattern
        self.video_y: Optional[int] = None

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

    def add_movies(self, *movie_paths):
        clip_file_name = self._clip_file_pattern.format(index=len(self._clips))
        # noinspection PyTypeChecker
        with NamedTemporaryFile(mode="w") as file:
            paths = "\n-  ".join(movie_paths)
            print(f"Concat movie files into {clip_file_name}: \n-{paths}")
            for path in movie_paths:
                line = f"file '{os.path.abspath(path)}'\n"
                file.write(line)
            file.flush()
            (
                ffmpeg.input(file.name, format="concat", safe=0)
                .output(clip_file_name, c="copy")
                .run(overwrite_output=True)
            )

        print(f"Created {clip_file_name}")

        clip: FFmpegSource = pyglet.media.load(clip_file_name)
        self._clips.append(Clip(source=clip, file=clip_file_name))

        if not self.video_y:
            ratio_y = self._window.height / clip.video_format.height
            ratio_x = self._window.width / clip.video_format.width
            ratio = min(ratio_x, ratio_y)
            gl.glScalef(ratio, ratio, ratio)

            if ratio_x == ratio:
                self.video_y = ((self._window.height - clip.video_format.height * ratio) / ratio) / 2
            else:
                self.video_y = 0

        return self

    def play(self):
        clip = self._clips.pop(0)
        self._player.queue(clip.source)
        self._player.play()
        pyglet.app.run()
        return [video.file for video in self._clips]

    def on_draw(self):
        if self._player.source and self._player.source.video_format:
            self._player.texture.blit(0, self.video_y)

        if not self._player.playing:
            print("Paused")

    def on_key_press(self, symbol, modifiers):
        if symbol == key.Q:
            print("Q pressed!")
            self._window.close()

        if symbol in (key.SPACE, key.PAGEDOWN, key.RIGHT):
            if not self._clips:
                self._window.close()
                return
            print("Next video")
            self._player.pause()
            self.play()


if __name__ == "__main__":
    VideoPlayer("clip-{index}.mp4").add_movies(*sys.argv[1:-1]).add_movies(*sys.argv[-1:]).play()
