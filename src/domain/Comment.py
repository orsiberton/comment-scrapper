class Comment:
    def __init__(self, text: str, time_spent: float = 0.0):
        self._text = text
        self._time_spent = time_spent

    def get_text(self) -> str:
        return self._text

    def get_time_spent(self) -> float:
        return self._time_spent
