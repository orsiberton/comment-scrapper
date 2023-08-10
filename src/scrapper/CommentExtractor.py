import base64
from datetime import datetime, timezone

import requests
from domain.Comment import Comment


class CommentExtractor:
    def __init__(self, username, password):
        self.token = f'Basic {self._encode_base64_credentials(username, password)}'

    def get_pr_comments(self, pr_link: str) -> list[Comment]:
        response = self._get_pr_data(pr_link)

        comment_list = []
        for field in response['value']:
            for comment in field['comments']:
                if comment['commentType'] == 'text' and not field['isDeleted'] and '[issue]' in comment['content']:
                    comment_list.append(
                        Comment(text=comment['content'].replace('[issue]', '').strip(),
                                time_spent=self._sanitize_time_spent(field['status'],
                                                                     field['publishedDate'],
                                                                     field['lastUpdatedDate']))
                    )

        return comment_list

    @staticmethod
    def _sanitize_time_spent(status: str, published_date: str, last_updated_date: str) -> float:
        d1 = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        if status != 'fixed':
            d2 = datetime.now().astimezone(tz=timezone.utc).replace(tzinfo=None)
        else:
            d2 = datetime.strptime(last_updated_date, "%Y-%m-%dT%H:%M:%S.%fZ")

        delta = d2 - d1

        # get difference in hours
        sec = delta.total_seconds()
        hours = sec / (60 * 60)

        return round(hours, 2)

    def _get_pr_data(self, pr_link) -> dict:
        headers = {
            'Authorization': self.token,
            'Accept': 'application/json'
        }

        split_link = pr_link.split('/')
        repository_name = split_link[-3]
        pr_number = split_link[-1]
        url = f'https://dev.azure.com/ab-inbev/GHQ_B2B_Delta/_apis/git/repositories/{repository_name}' \
              f'/pullRequests/{pr_number}/threads?api-version=7.1-preview.1'

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f'Error while getting PR comments. Status code: {response.status_code}')

        return response.json()

    @staticmethod
    def _encode_base64_credentials(username: str, password: str) -> str:
        return base64.b64encode((username + ':' + password).encode('utf-8')).decode('utf-8')
