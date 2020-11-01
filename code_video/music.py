from tempfile import NamedTemporaryFile

import librosa
from pydub import AudioSegment


class BackgroundMusic:
    def __init__(self, file: str):
        self.file = file
        x, sr = librosa.load(file)
        _, self.beat_times = librosa.beat.beat_track(x, sr=sr, start_bpm=60, units="time")
        self.beat_times = [0] + self.beat_times.tolist()
        self.off_beat_times = []
        for idx, time in enumerate(self.beat_times[::2]):
            if len(self.beat_times) >= idx:
                self.off_beat_times.append((self.beat_times[idx] + self.beat_times[idx + 1]) / 2)
        self.measure_times = self.off_beat_times[::2]

    def next_beat(self, time):
        for item in self.beat_times:
            if item >= time:
                return time + item - time
        raise ValueError("No more music")

    def next_measure(self, time):
        for item in self.measure_times:
            if item >= time:
                return item
        return time


def fit_audio(file: str, length: float) -> str:
    extension = file.split(".")[-1]
    segment = AudioSegment.from_file(file, extension)[: length * 1000].fade_out(1000)
    tmp = NamedTemporaryFile(suffix=f".{extension}", delete=False)
    segment.export(tmp.name, format=extension)
    return tmp.name
