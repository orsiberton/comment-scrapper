import argparse
import os

from config.Logger import logger
from scrapper.Analyzer import Analyzer
from scrapper.Categorizer import Categorizer
from scrapper.CommentExtractor import CommentExtractor


def scrap_comments(username, password, pr_links):
    comment_extractor = CommentExtractor(username, password)

    logger.info('Starting to scrap comments')
    for pr_link in pr_links:
        logger.info(f'Scrapping comments from {pr_link}')
        comments = comment_extractor.get_pr_comments(pr_link)
        classify_comments(comments)

    logger.info('Finished scrapping comments')


def classify_comments(comments):
    categorizer = Categorizer(os.getenv("API_KEY"), os.getenv("API_BASE"))

    logger.info('Classifying comments')
    categorized_comments = categorizer.categorize(comments)

    logger.info('Finished classifying comments')

    logger.info('Analyzing comments')
    analyze_comments(categorized_comments)


def analyze_comments(categorized_comments):
    path = 'src/charts'
    if not os.path.exists(path):
        os.mkdir(path)
        logger.info(f'Folder {path} created!')
    else:
        logger.info(f'Folder {path} already exists')

    analyzer = Analyzer(path)
    analyzer.analyze(categorized_comments)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This script will receive a list of PR links that should be scrapped')
    parser.add_argument('-u', '--username', dest='username', type=str, help='Azure DevOps username')
    parser.add_argument('-p', '--password', dest='password', type=str, help='Azure DevOps password')
    parser.add_argument('-pr', '--prLink', dest='prLinks', type=str, nargs='+', help='PR links to be scrapped')
    args = parser.parse_args()
    scrap_comments(args.username, args.password, args.prLinks)
