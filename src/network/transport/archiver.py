from structs import Dialogue, History

class Archiver:
    def __init__(self) -> None:
        self.history = History()

    def archive(self, dialogue: Dialogue) -> None:
        self.history.append(dialogue)
