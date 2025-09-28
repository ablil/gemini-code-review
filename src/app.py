#!usr/bin/env python3

import logging


from ai import Gemini
from gh import GithubClient
from utils import assert_env_variable, get_files_from_gitignore, get_env_variable_or_default, create_logger, get_extra_prompt, DEFAULT_EXCLUDED_FILES
from review_state import hash_diff
from pr_state import get_state_comment, upsert_state_comment

logger = create_logger(__name__)

logging.getLogger('urllib3').setLevel(logging.WARN)


def main(github_client: GithubClient, gemini_client: Gemini, repo: str, pr_no: int):
    pull_request = github.get_pull_request(repository_name, pr_no)

    excluded_filenames = get_env_variable_or_default('EXCLUDE_FILENAMES', '').split(',')
    excluded_filenames.extend(DEFAULT_EXCLUDED_FILES)

    # Load PR state (reviewed_hashes and last_reviewed_sha)
    _, state = get_state_comment(pull_request)
    reviewed_hashes = state.get("reviewed_hashes", {})
    last_reviewed_sha = state.get("last_reviewed_sha")

    # Determine base and head SHAs
    base_sha = last_reviewed_sha or pull_request.base.sha
    head_sha = pull_request.head.sha

    # Only review new commits if last_reviewed_sha exists, else review all
    if last_reviewed_sha and last_reviewed_sha != head_sha:
        logger.info(f"Reviewing only new commits: {base_sha}..{head_sha}")
        # Optionally, you may want to use a method to get only the diff for these commits
        # For now, extract_diffs will still get all changed files, but you can filter diffs by commit range if needed
    else:
        logger.info(f"Reviewing all changes: {base_sha}..{head_sha}")

    diffs = github.extract_diffs(pull_request, excluded_filenames)
    updated_hashes = dict(reviewed_hashes)
    for diff in diffs:
        diff_hash = hash_diff(diff.diff)
        if reviewed_hashes.get(diff.filename) == diff_hash:
            logger.info(f"Skipping {diff.filename}, diff unchanged.")
            continue
        try:
            github.comment(pull_request, gemini.review(diff.diff), diff.filename, diff.linenumber)
            updated_hashes[diff.filename] = diff_hash
        except Exception as e:
            logger.error(e)
    # Update PR state with new hashes and last reviewed SHA
    upsert_state_comment(pull_request, {"reviewed_hashes": updated_hashes, "last_reviewed_sha": head_sha})

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
