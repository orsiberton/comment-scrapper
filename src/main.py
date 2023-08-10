import argparse
import os

from scrapper.Analyzer import Analyzer
from scrapper.Categorizer import Categorizer
from scrapper.CommentExtractor import CommentExtractor


def scrap_comments(username, password, pr_links):
    comment_extractor = CommentExtractor(username, password)
    for pr_link in pr_links:
        comments = comment_extractor.get_pr_comments(pr_link)
        classify_comments(comments)


def classify_comments(comments):
    categorizer = Categorizer(os.getenv("API_KEY"), os.getenv("API_BASE"))

    categorized_comments = categorizer.categorize(comments)

    for item in categorized_comments:
        print(f"Comment: {item.get_comment().get_text()}\nCategory: {item.get_category()}\n")

    analyzer = Analyzer()
    analyzer.analyze(categorized_comments)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This script will receive a list of PR links that should be scrapped')
    parser.add_argument('-u', '--username', dest='username', type=str, help='Azure DevOps username')
    parser.add_argument('-p', '--password', dest='password', type=str, help='Azure DevOps password')
    parser.add_argument('-pr', '--prLink', dest='prLinks', type=str, nargs='+', help='PR links to be scrapped')
    args = parser.parse_args()
    scrap_comments(args.username, args.password, args.prLinks)
