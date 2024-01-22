from ev3dev2.sound import Sound


class SoundPlayer:
    def __init__(self, filepath: str) -> None:
        self.spkr = Sound()
        self.filepath = filepath
        self._process = None

    def play(self) -> None:
        self._process = self.spkr.play_file(self.filepath, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)

    def stop(self) -> None:
        if self._process is not None:
            self._process.kill()
            self._process = None

