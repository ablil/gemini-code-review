#!usr/bin/env python3

import logging

from ai import Gemini
from gh import GithubClient
from utils import assert_env_variable, get_files_from_gitignore, get_env_variable_or_default, create_logger, get_extra_prompt

logger = create_logger(__name__)

logging.getLogger('urllib3').setLevel(logging.WARN)

def main(github_client: GithubClient, gemini_client: Gemini, repo: str, pr_no: int):
    pull_request = github.get_pull_request(repository_name, pr_no)

    excluded_filenames = get_env_variable_or_default('EXCLUDE_FILENAMES')
    if excluded_filenames:
        excluded_filenames = set(excluded_filenames.split(','))
    else:
        excluded_filenames = get_files_from_gitignore('.gitignore')

    diffs = github.extract_diffs(pull_request, excluded_filenames)

    for diff in diffs:
        try:
            github.comment(pull_request, gemini.review(diff.diff), diff.filename)
        except Exception as e:
            logger.error(e)

if __name__ == '__main__':
    # verify all needed env variables
    gemini_api_key = assert_env_variable('GEMINI_API_KEY')
    repository_name = assert_env_variable('GITHUB_REPOSITORY')
    github_token = assert_env_variable('GITHUB_TOKEN')
    ref_name = assert_env_variable('GITHUB_REF_NAME')
    extra_prompt = get_extra_prompt()

    github = GithubClient(github_token, dry_run = get_env_variable_or_default('DRY_RUN', 'false').lower() in ['1', 'true'])
    gemini = Gemini(gemini_api_key, extra_prompt)

    # run
    main(github, gemini, repository_name, int(ref_name.split('/')[0]))
