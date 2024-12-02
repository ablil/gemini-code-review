#!usr/bin/env python3

import ai
import gh
import os
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    assert 'GITHUB_TOKEN' in os.environ
    assert 'GEMINI_API_KEY' in os.environ and len(os.environ['GEMINI_API_KEY'])
    assert 'GITHUB_REPOSITORY' in os.environ
    assert 'GITHUB_REF_NAME' in os.environ and os.environ['GITHUB_REF_NAME'].endswith('/merge')

    repo = os.environ['GITHUB_REPOSITORY']
    pr_no = int(os.environ['GITHUB_REF_NAME'].split('/')[0])

    pr = gh.get_pull_request(repo, pr_no)
    diffs = gh.extract_git_diff_from_pull_request(pr)
    ai.configure_credentials(os.environ['GEMINI_API_KEY'])
    for diff in diffs:
        try:
            review = ai.ask(diff.diff)
            gh.write_comment(pr, review, diff.filename)
        except Exception as e:
            logging.error(e)
