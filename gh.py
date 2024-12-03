#!/usr/bin/env python
import dataclasses
import fnmatch
import logging
from typing import List

from github import Auth
from github import Github, PullRequest

from utils import assert_env_variable

logging.basicConfig(level=logging.DEBUG)


@dataclasses.dataclass
class GitDiff:
    filename: str
    diff: str


class GithubClient:
    def __init__(self, github_token: str):
        self.client = Github(auth=Auth.Token(github_token))
        logging.info("created Github client successfully")

    def get_pull_request(self, repo: str, pr_no: int) -> PullRequest:
        logging.info(f"Fetching pull request #{pr_no} from repository ${repo}")
        return self.client.get_repo(repo).get_pull(pr_no)

    def extract_diffs(self, pull_request: PullRequest, exclude_patterns: set[str]) -> List[GitDiff]:
        all_files = list(pull_request.get_files())
        filtered_files = list(filter(lambda filename: not  self.__should_exclude(filename.filename, exclude_patterns), all_files))
        logging.info(
            f"PR #{pull_request.number} has total of {len(all_files)} file, extracting diffs from {len(filtered_files)} files only")
        return list(GitDiff(filename=file.filename, diff=file.raw_data['patch']) for file in filtered_files)

    def comment(self, pr: PullRequest, body: str, filename: str):
        assert len(body), 'Blank github comment body provided'
        assert len(filename), 'Blank filename'

        try:
            last_commit = pr.get_commits()[pr.commits - 1]
            pr.create_comment(body, last_commit, filename, 1)
            logging.info(f"Added comment to PR #{pr.number}: body: {body[:50]}")
        except Exception as e:
            logging.error(f"Failed to add comment to PR #{pr.number}: {e}")

    def __should_exclude(self, filename: str, patterns: set[str]) -> bool:
        return any(fnmatch.fnmatch(filename, pat) for pat in patterns)

if __name__ == '__main__':
    token = assert_env_variable('GITHUB_TOKEN')
    exclude_patterns = assert_env_variable('EXCLUDE_FILENAMES', '*.txt,*.md')

    print(exclude_patterns)
    client = GithubClient(token)
    pr = client.get_pull_request('ablil/gemini-code-review', 5)
    diffs = client.extract_diffs(pr, set(exclude_patterns.split(',')))
