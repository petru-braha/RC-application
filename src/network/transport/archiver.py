from structs import Dialogue, History

class Archiver:
    """
    Manages the history of dialogues (requests and responses).
    """
    
    def __init__(self) -> None:
        self.history = History()

    def archive(self, dialogue: Dialogue) -> None:
        """
        Adds a dialogue to the history.

        Parameters:
            dialogue (obj): The dialogue to add.
        """
        self.history.append(dialogue)
