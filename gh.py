#!/usr/bin/env python
import dataclasses
import os
from functools import cache
from typing import List

import requests
from github import Github, Repository, PullRequest
from github import Auth
import logging

logging.basicConfig(level=logging.DEBUG)

@dataclasses.dataclass
class GitDiff:
    filename: str
    diff: str

@cache
def __get_client(token: str) -> Github:
    logging.debug("creating client ...")
    return Github(auth=Auth.Token(token))

def get_pull_request(repo: str, pr_no: int) -> PullRequest:
    client = __get_client(os.environ['GITHUB_TOKEN'])
    return  client.get_repo(repo).get_pull(pr_no)

def extract_git_diff_from_pull_request(pr: PullRequest) -> List[GitDiff]:
    files = list(pr.get_files())
    return [GitDiff(filename=file.filename, diff=file.raw_data['patch']) for file in files]

def write_comment(pr: PullRequest, body: str, filename: str):
    last_commit = pr.get_commits()[pr.commits - 1]
    pr.create_comment(body, last_commit, filename, 1)
    logging.debug(f"commented on file {filename} with {body}")

if __name__ == '__main__':
    assert 'GITHUB_TOKEN' in os.environ
    repo = 'ablil/spring-playground'
    pr_no = 80
    pr = get_pull_request(repo, pr_no)