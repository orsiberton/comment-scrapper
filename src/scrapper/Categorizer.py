import openai

from config.Logger import logger
from domain.CategorizedComment import CategorizedComment
from domain.Comment import Comment


class Categorizer:
    PROMPT = """
    Classify the comment into one of the following categories(return only the category name):
    Code Complexity
    Naming Convention
    Code Duplication
    Code Readability
    Logic Incorrectly
        
    Comment: {comment}
    Category:
    """

    def __init__(self, api_key: str, api_base: str):
        self.api_key = api_key
        self.api_base = api_base
        self.api_type = 'azure'
        self.api_version = '2023-05-15'

    def categorize(self, comments: list[Comment]) -> list[CategorizedComment]:
        # Authenticate with OpenAI API
        openai.api_key = self.api_key
        openai.api_base = self.api_base
        openai.api_type = "azure"
        openai.api_version = "2023-05-15"

        # Classify comments using OpenAI API
        categorized_comments = []
        for comment in comments:
            logger.info(f'Classifying comment: {comment.get_text()}')
            response = openai.Completion.create(
                engine="gpt-35-turbo",
                prompt=self.PROMPT.format(comment=comment.get_text()),
                temperature=0,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=["\n"]
            )
            category = response.choices[0].text.strip()

            logger.info(f'Comment classified as: {category}')

            categorized_comments.append(CategorizedComment(comment, category))

        return categorized_comments
