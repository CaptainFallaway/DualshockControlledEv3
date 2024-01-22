from ev3dev2.sound import Sound


class SoundPlayer:
    def __init__(self, filepath: str) -> None:
        self.spkr = Sound()

        self.filepath = filepath
        self._process = None

    @property
    def playing(self) -> bool:
        return self._process is not None

    def play(self) -> None:
        print("Playing", self.filepath)
        self._process = self.spkr.play_file(self.filepath, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)

    def stop(self) -> None:
        if self._process is not None:
            print("Stopping", self.filepath)
            self._process.kill()
            self._process = None

