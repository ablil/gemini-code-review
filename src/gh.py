#!/usr/bin/env python

import dataclasses
import fnmatch
from typing import List

from github import Auth
from github import Github, PullRequest

from utils import assert_env_variable, get_files_from_gitignore, create_logger
import re

logger = create_logger(__name__)



@dataclasses.dataclass
class GitDiff:
    filename: str
    diff: str
    positions: list[int]  # positions in the diff for changed lines


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

        result: List[GitDiff] = []
        for file in filtered_files:
            if not 'patch' in file.raw_data:
                logger.warning(f"key 'patch' NOT found in  {file.raw_data}")
                continue

            diff = file.raw_data['patch']
            # Find all positions of changed lines in the diff
            positions = []
            diff_lines = diff.splitlines()
            pos = 0
            for i, line in enumerate(diff_lines):
                if line.startswith('+') and not line.startswith('+++'):
                    positions.append(pos)
                if not line.startswith('-') or line.startswith('---'):
                    pos += 1
            result.append(GitDiff(filename=file.filename, diff=diff, positions=positions))

        return result

    def comment(self, pr: PullRequest, body: str, filename: str, position: int):
        assert len(body), 'Blank github comment body provided'
        assert len(filename), 'Blank filename'

        try:
            last_commit = pr.get_commits()[pr.commits - 1]
            if self.dry_run:
                logger.info(f"[dry-run] commented on file {filename} at position {position}")
            else:
                pr.create_comment(body, last_commit, filename, position)
                logger.info(f"commented on file {filename} at position {position}")
        except Exception as e:
            logger.error(f"failed to comment on file {filename} at position {position}, {e}")

    def __should_exclude(self, filename: str, patterns: set[str]) -> bool:
        return any(fnmatch.fnmatch(filename, pat) for pat in patterns)

if __name__ == '__main__':
    token = assert_env_variable('GITHUB_TOKEN')
    exclude_patterns =  get_files_from_gitignore('.gitignore')
    client = GithubClient(token, dry_run = True)
    pr = client.get_pull_request('ablil/gemini-code-review', 5)
    diffs = client.extract_diffs(pr, exclude_patterns)
