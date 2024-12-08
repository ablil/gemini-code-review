#!usr/bin/env python3
import logging

from ai import Gemini
from gh import GithubClient
from utils import assert_env_variable, get_files_from_gitignore, get_env_variable_or_default

logging.basicConfig(level=logging.DEBUG)

logging.getLogger('urllib3').setLevel(logging.WARN)

if __name__ == '__main__':
    # verify all needed env variables
    gemini_api_key = assert_env_variable('GEMINI_API_KEY')
    repository_name = assert_env_variable('GITHUB_REPOSITORY')
    github_token = assert_env_variable('GITHUB_TOKEN')
    excluded_filenames = get_env_variable_or_default('EXCLUDE_FILENAMES')
    ref_name = assert_env_variable('GITHUB_REF_NAME')

    github = GithubClient(github_token)
    gemini = Gemini(gemini_api_key)

    pull_request = github.get_pull_request(repository_name, int(ref_name.split('/')[0]))
    diffs = github.extract_diffs(pull_request, set(excluded_filenames.split(',')) if excluded_filenames else get_files_from_gitignore('.gitignore'))

    for diff in diffs:
        try:
            github.comment(pull_request, gemini.review(diff.diff), diff.filename)
        except Exception as e:
            logging.error(e)
