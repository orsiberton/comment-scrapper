from .Comment import Comment


class CategorizedComment:
    def __init__(self, comment: Comment, category: str):
        self._comment = comment
        self._category = category

    def get_comment(self) -> Comment:
        return self._comment

    def get_category(self) -> str:
        return self._category

    def to_dict(self) -> dict:
        return {
            'comment': self._comment.get_text(),
            'category': self._category,
            'time_spent': self._comment.get_time_spent()
        }
