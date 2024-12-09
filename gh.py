#!/usr/bin/env python

import dataclasses
import fnmatch
from typing import List

from github import Auth
from github import Github, PullRequest

from utils import assert_env_variable, get_files_from_gitignore, create_logger

logger = create_logger(__name__)


@dataclasses.dataclass
class GitDiff:
    filename: str
    diff: str


class GithubClient:
    def __init__(self, github_token: str, dry_run: bool = False):
        self.dry_run = dry_run
        self.client = Github(auth=Auth.Token(github_token))
        logger.info("created Github client successfully")
        if self.dry_run:
            logger.info("running in dry-run mode")

    def get_pull_request(self, repo: str, pr_no: int) -> PullRequest:
        logger.info(f"Fetching pull request #{pr_no} from repository {repo}")
        return self.client.get_repo(repo).get_pull(pr_no)

    def extract_diffs(self, pull_request: PullRequest, exclude_patterns: set[str]) -> List[GitDiff]:
        all_files = list(pull_request.get_files())
        filtered_files = list(filter(lambda filename: not  self.__should_exclude(filename.filename, exclude_patterns), all_files))
        logger.info(f"total changed files {len(all_files)}, extracting diffs from {len(filtered_files)} files only")
        return list(GitDiff(filename=file.filename, diff=file.raw_data['patch']) for file in filtered_files)

    def comment(self, pr: PullRequest, body: str, filename: str):
        assert len(body), 'Blank github comment body provided'
        assert len(filename), 'Blank filename'

        try:
            last_commit = pr.get_commits()[pr.commits - 1]
            if self.dry_run:
                logger.info(f"[dry-run] commented on file {filename}")
            else:
                pr.create_comment(body, last_commit, filename, 1)
                logger.info(f"commented on file {filename}")
        except Exception as e:
            logger.error(f"failed to comment on file {filename}, {e}")

    def __should_exclude(self, filename: str, patterns: set[str]) -> bool:
        return any(fnmatch.fnmatch(filename, pat) for pat in patterns)

if __name__ == '__main__':
    token = assert_env_variable('GITHUB_TOKEN')
    exclude_patterns =  get_files_from_gitignore('.gitignore')
    client = GithubClient(token, dry_run = True)
    pr = client.get_pull_request('ablil/gemini-code-review', 5)
    diffs = client.extract_diffs(pr, exclude_patterns)
